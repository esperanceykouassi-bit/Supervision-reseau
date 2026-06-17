# SupervisionNet — Application mobile Android (Kotlin)

Application Android **native** (Kotlin + Jetpack Compose) qui consomme l'**API
REST** du système de supervision réseau (OPEN MOISE / Awali) pour afficher, sur
smartphone, le tableau de bord temps réel : indicateurs, taux de disponibilité,
alertes actives et état des équipements.

L'appli est **découplée** du serveur : elle ne fait qu'interroger les routes
`/api/statistiques`, `/api/equipements` et `/api/alertes` exposées par Flask.

---

## 1. Prérequis serveur (à faire une fois)

L'API est protégée par une **clé d'API**. Sur la VM, ajoute une clé dans le
`.env` puis redémarre le tableau de bord :

```bash
cd ~/supervision/src
echo "API_KEY=ChoisisUneCleApiLongueEtAleatoire2026" >> .env
pkill -f app.py
nohup venv/bin/python app.py > logs/app.log 2>&1 &
```

Vérifie que l'API répond avec la clé (depuis la VM ou un PC du réseau) :

```bash
curl -H "X-API-Key: ChoisisUneCleApiLongueEtAleatoire2026" http://192.168.1.50:5000/api/statistiques
```
→ doit renvoyer un JSON (et non une page de connexion).

## 2. Prérequis poste de développement

- **Android Studio** (version récente, Hedgehog ou plus) installé sur ton PC.
- Un **smartphone Android 7.0+** (minSdk 24) **sur le même réseau Wi-Fi** que la
  VM (réseau `192.168.1.x`), avec le **débogage USB** activé — ou un émulateur.

## 3. Ouvrir et compiler le projet

1. Dans Android Studio : **File ▸ Open** → sélectionne le dossier
   `mobile/android`.
2. Laisse Android Studio **synchroniser** (il télécharge le SDK et génère
   automatiquement le *Gradle wrapper* — accepte si une fenêtre le propose).
   > Si la synchro réclame le wrapper : `Tools ▸ … ` ou exécute dans un terminal
   > du dossier `mobile/android` : `gradle wrapper --gradle-version 8.7`.
3. Branche ton téléphone (ou démarre un émulateur), puis clique sur **Run ▶**.

L'APK s'installe et se lance.

## 4. Configurer l'application (au 1er lancement)

L'écran de configuration s'ouvre automatiquement. Saisis :

- **Adresse du serveur** : `http://192.168.1.50:5000`
- **Clé d'API** : la même que dans le `.env` (`API_KEY`)

Touche **Se connecter** → le tableau de bord s'affiche et se **rafraîchit
automatiquement toutes les 30 secondes**. L'icône ⚙️ permet de revenir à la
configuration ; l'icône ↻ force un rafraîchissement.

## 5. Générer un APK partageable

**Build ▸ Build Bundle(s) / APK(s) ▸ Build APK(s)** → l'APK est créé dans
`app/build/outputs/apk/debug/`. Tu peux l'installer sur n'importe quel téléphone
du réseau.

---

## 6. Notifications push (évolution : Firebase Cloud Messaging)

L'appli affiche les alertes **quand elle est ouverte** (rafraîchissement 30 s).
Pour de vraies **notifications push en arrière-plan**, deux pistes :

- **Simple (déjà en place)** : les alertes Telegram du serveur jouent déjà ce
  rôle de notification mobile.
- **Natif (FCM)** : pour pousser les alertes dans la barre de notifications
  Android, il faut :
  1. créer un projet **Firebase** et ajouter `google-services.json` à `app/` ;
  2. ajouter les dépendances `firebase-messaging` ;
  3. l'appli s'enregistre et envoie son **token** au serveur ;
  4. côté serveur, un petit module envoie l'alerte à l'API FCM (en plus de
     Telegram/e-mail), comme un canal supplémentaire dans `modules/alertes/`.

Cette évolution est documentée comme **perspective** : l'architecture (canaux
d'alerte modulaires + API REST) est déjà prête à l'accueillir.

---

## Architecture du module mobile

```
mobile/android/
├── settings.gradle.kts / build.gradle.kts / gradle.properties
└── app/
    ├── build.gradle.kts            # dépendances (Compose, Retrofit, Coroutines)
    └── src/main/
        ├── AndroidManifest.xml     # permission INTERNET + HTTP en clair (LAN)
        ├── res/values/             # nom de l'appli, thème
        └── java/ci/openmoise/supervision/
            ├── Models.kt           # modèles JSON (Statistiques, Equipement, Alerte)
            ├── Api.kt              # client Retrofit + clé d'API (X-API-Key)
            └── MainActivity.kt     # interface Compose (config + tableau de bord)
```
