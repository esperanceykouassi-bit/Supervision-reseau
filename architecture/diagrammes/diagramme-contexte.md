# Diagramme de contexte

Le **diagramme de contexte** présente le système comme une « boîte noire »
unique et identifie les **acteurs externes** qui interagissent avec lui ainsi
que les **flux** entrants/sortants. Il fixe le périmètre du projet.

```mermaid
graph LR
    ADMIN["👤 Administrateur réseau"]
    EQUIP["🖧 Équipements réseau<br/>(routeurs, switches, serveurs…)"]
    MAIL["📧 Serveur SMTP"]
    TELEGRAM["📱 Service Telegram"]

    SYS(("SYSTÈME DE<br/>SUPERVISION<br/>RÉSEAU AUTOMATISÉE"))

    ADMIN -->|"Consulte le tableau de bord<br/>Gère les équipements<br/>Acquitte les alertes"| SYS
    SYS -->|"Affiche état, statistiques, rapports"| ADMIN
    SYS -->|"Sondes ICMP / TCP"| EQUIP
    EQUIP -->|"Réponses (UP/DOWN, latence)"| SYS
    SYS -->|"Envoie e-mails d'alerte"| MAIL
    SYS -->|"Envoie notifications push"| TELEGRAM
    MAIL -->|"Délivre à l'admin"| ADMIN
    TELEGRAM -->|"Notifie sur smartphone"| ADMIN

    classDef sys fill:#0d6efd,stroke:#003,color:#fff,stroke-width:3px;
    class SYS sys;
```

## Acteurs identifiés

| Acteur | Rôle |
|--------|------|
| **Administrateur réseau** | Acteur principal : configure les équipements, consulte le tableau de bord et traite les alertes. |
| **Équipements réseau** | Acteurs supervisés : cibles passives des sondes. |
| **Serveur SMTP** | Acteur secondaire : relaie les alertes par e-mail. |
| **Service Telegram** | Acteur secondaire : délivre les notifications instantanées. |
