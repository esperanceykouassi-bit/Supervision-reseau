package ci.openmoise.supervision

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

/**
 * Application mobile « SupervisionNet » : tableau de bord Android natif qui
 * consomme l'API REST du système de supervision réseau (OPEN MOISE / Awali).
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(colorScheme = lightColorScheme(primary = Navy)) {
                DashboardApp()
            }
        }
    }
}

private val Navy = Color(0xFF1B3A5C)
private val Cyan = Color(0xFF00B4D8)
private val Green = Color(0xFF198754)
private val Red = Color(0xFFDC3545)
private val Amber = Color(0xFFF0A500)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardApp() {
    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences("config", Context.MODE_PRIVATE) }
    val scope = rememberCoroutineScope()

    var baseUrl by remember { mutableStateOf(prefs.getString("baseUrl", "http://192.168.1.50:5000") ?: "") }
    var apiKey by remember { mutableStateOf(prefs.getString("apiKey", "") ?: "") }
    var configVisible by remember { mutableStateOf(apiKey.isEmpty()) }

    var stats by remember { mutableStateOf<Statistiques?>(null) }
    var equipements by remember { mutableStateOf<List<Equipement>>(emptyList()) }
    var alertes by remember { mutableStateOf<List<Alerte>>(emptyList()) }
    var erreur by remember { mutableStateOf<String?>(null) }
    var chargement by remember { mutableStateOf(false) }

    suspend fun rafraichir() {
        if (apiKey.isBlank()) return
        chargement = true
        erreur = null
        try {
            val api = ApiFactory.create(baseUrl, apiKey)
            stats = api.statistiques()
            equipements = api.equipements()
            alertes = api.alertes()
        } catch (e: Exception) {
            erreur = "Connexion impossible : ${e.message}"
        } finally {
            chargement = false
        }
    }

    // Rafraîchissement automatique toutes les 30 secondes.
    LaunchedEffect(baseUrl, apiKey) {
        while (true) {
            rafraichir()
            delay(30_000)
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("SupervisionNet", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Navy, titleContentColor = Color.White,
                    actionIconContentColor = Color.White
                ),
                actions = {
                    IconButton(onClick = { configVisible = !configVisible }) {
                        Icon(Icons.Filled.Settings, contentDescription = "Configuration")
                    }
                    IconButton(onClick = { scope.launch { rafraichir() } }) {
                        Icon(Icons.Filled.Refresh, contentDescription = "Rafraîchir")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            Modifier
                .padding(padding)
                .padding(12.dp)
                .verticalScroll(rememberScrollState())
        ) {
            if (configVisible) {
                ConfigCard(
                    baseUrl = baseUrl, apiKey = apiKey,
                    onSave = { url, key ->
                        baseUrl = url; apiKey = key
                        prefs.edit().putString("baseUrl", url).putString("apiKey", key).apply()
                        configVisible = false
                        scope.launch { rafraichir() }
                    }
                )
                Spacer(Modifier.height(12.dp))
            }

            if (chargement && stats == null) {
                Box(Modifier.fillMaxWidth().padding(24.dp), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = Cyan)
                }
            }

            erreur?.let {
                Card(colors = CardDefaults.cardColors(containerColor = Red.copy(alpha = 0.12f))) {
                    Text(it, Modifier.padding(12.dp), color = Red)
                }
                Spacer(Modifier.height(12.dp))
            }

            stats?.let { s ->
                KpiRow(s)
                Spacer(Modifier.height(8.dp))
                Text(
                    "Disponibilité globale : ${s.taux_disponibilite} %",
                    fontWeight = FontWeight.Bold, color = Navy, fontSize = 16.sp
                )
                Spacer(Modifier.height(12.dp))

                SectionTitle("Alertes actives (${alertes.size})")
                if (alertes.isEmpty()) {
                    Text("Aucune alerte active", color = Green, modifier = Modifier.padding(4.dp))
                } else {
                    alertes.take(20).forEach { AlerteRow(it) }
                }

                Spacer(Modifier.height(12.dp))
                SectionTitle("Équipements (${equipements.size})")
                equipements.take(50).forEach { EquipementRow(it) }
            }
        }
    }
}

@Composable
private fun ConfigCard(baseUrl: String, apiKey: String, onSave: (String, String) -> Unit) {
    var url by remember { mutableStateOf(baseUrl) }
    var key by remember { mutableStateOf(apiKey) }
    Card {
        Column(Modifier.padding(16.dp)) {
            Text("Configuration du serveur", fontWeight = FontWeight.Bold, color = Navy)
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = url, onValueChange = { url = it },
                label = { Text("Adresse du serveur (ex. http://192.168.1.50:5000)") },
                singleLine = true, modifier = Modifier.fillMaxWidth()
            )
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = key, onValueChange = { key = it },
                label = { Text("Clé d'API (X-API-Key)") },
                singleLine = true, visualTransformation = PasswordVisualTransformation(),
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(Modifier.height(12.dp))
            Button(
                onClick = { onSave(url.trim(), key.trim()) },
                colors = ButtonDefaults.buttonColors(containerColor = Cyan),
                modifier = Modifier.fillMaxWidth()
            ) { Text("Se connecter") }
        }
    }
}

@Composable
private fun KpiRow(s: Statistiques) {
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        KpiCard("Supervisés", s.total_equipements.toString(), Navy, Modifier.weight(1f))
        KpiCard("En ligne", s.equipements_up.toString(), Green, Modifier.weight(1f))
    }
    Spacer(Modifier.height(8.dp))
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        KpiCard("Hors ligne", s.equipements_down.toString(), Red, Modifier.weight(1f))
        KpiCard("Alertes", s.alertes_actives.toString(), Amber, Modifier.weight(1f))
    }
}

@Composable
private fun KpiCard(titre: String, valeur: String, couleur: Color, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(containerColor = couleur),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(Modifier.padding(14.dp)) {
            Text(titre, color = Color.White, fontSize = 13.sp)
            Text(valeur, color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
private fun SectionTitle(t: String) {
    Text(t, fontWeight = FontWeight.Bold, color = Navy, fontSize = 16.sp,
        modifier = Modifier.padding(vertical = 6.dp))
}

@Composable
private fun AlerteRow(a: Alerte) {
    val couleur = when (a.severite) {
        "CRITIQUE" -> Red
        "AVERTISSEMENT" -> Amber
        else -> Cyan
    }
    Card(Modifier.fillMaxWidth().padding(vertical = 3.dp)) {
        Row(Modifier.padding(10.dp), verticalAlignment = Alignment.CenterVertically) {
            Badge(containerColor = couleur, contentColor = Color.White) { Text(a.severite.take(4)) }
            Spacer(Modifier.width(10.dp))
            Column {
                Text("${a.nom}  (${a.adresse_ip})", fontWeight = FontWeight.Bold, color = Navy)
                Text("${a.type_alerte} — ${a.message ?: ""}", fontSize = 12.sp, color = Color.DarkGray)
            }
        }
    }
}

@Composable
private fun EquipementRow(e: Equipement) {
    val up = e.statut == "UP"
    Card(Modifier.fillMaxWidth().padding(vertical = 3.dp)) {
        Row(Modifier.padding(10.dp), verticalAlignment = Alignment.CenterVertically) {
            Badge(
                containerColor = if (up) Green else Red, contentColor = Color.White
            ) { Text(e.statut) }
            Spacer(Modifier.width(10.dp))
            Column(Modifier.weight(1f)) {
                Text(e.nom, fontWeight = FontWeight.Bold, color = Navy)
                Text(e.adresse_ip, fontSize = 12.sp, color = Color.DarkGray)
            }
            Text(
                if (e.latence_ms != null) "${e.latence_ms} ms" else "—",
                fontSize = 12.sp, color = Color.Gray
            )
        }
    }
}
