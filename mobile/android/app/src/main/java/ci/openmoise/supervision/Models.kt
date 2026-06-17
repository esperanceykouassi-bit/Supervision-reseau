package ci.openmoise.supervision

/**
 * Modèles de données — correspondent au JSON renvoyé par l'API Flask
 * (/api/statistiques, /api/equipements, /api/alertes).
 */

data class Statistiques(
    val total_equipements: Int = 0,
    val equipements_up: Int = 0,
    val equipements_down: Int = 0,
    val alertes_actives: Int = 0,
    val taux_disponibilite: Double = 0.0,
    val latence_moyenne: Double = 0.0
)

data class Equipement(
    val id: Int = 0,
    val nom: String = "",
    val adresse_ip: String = "",
    val type_equipement: String? = null,
    val statut: String = "INCONNU",
    val latence_ms: Double? = null,
    val derniere_verification: String? = null
)

data class Alerte(
    val id: Int = 0,
    val nom: String = "",
    val adresse_ip: String = "",
    val type_alerte: String = "",
    val severite: String = "",
    val message: String? = null,
    val date_alerte: String? = null
)
