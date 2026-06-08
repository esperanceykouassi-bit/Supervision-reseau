# Schéma d'architecture réseau

Ce schéma situe le **serveur de supervision** dans une topologie réseau
d'entreprise réaliste et illustre les **flux** de sondage et d'alerte.

## Topologie (diagramme Mermaid)

```mermaid
graph TB
    INTERNET((Internet))
    FW[Pare-feu / Firewall<br/>192.168.1.254]
    R[Routeur principal<br/>192.168.1.1]
    SW1[Switch Étage 1<br/>192.168.1.2]
    SW2[Switch Datacenter<br/>192.168.1.3]

    subgraph DATACENTER[Datacenter]
        SUP[/"🖥️ SERVEUR DE SUPERVISION<br/>Ubuntu + Python + MySQL + Flask<br/>192.168.1.100"/]
        WEB[Serveur Web<br/>192.168.1.10]
        BDD[Serveur BDD<br/>192.168.1.11]
        FIC[Serveur Fichiers<br/>192.168.1.12]
    end

    subgraph LAN[Réseau local - Utilisateurs]
        WIFI[Borne WiFi<br/>192.168.1.20]
        IMP[Imprimante<br/>192.168.1.30]
        PC[Postes de travail]
    end

    ADMIN[["👤 Administrateur<br/>(E-mail + Telegram)"]]

    INTERNET --- FW
    FW --- R
    R --- SW1
    R --- SW2
    SW1 --- WIFI
    SW1 --- IMP
    SW1 --- PC
    SW2 --- SUP
    SW2 --- WEB
    SW2 --- BDD
    SW2 --- FIC

    SUP -. "sondes ICMP / TCP" .-> WEB
    SUP -. "sondes" .-> BDD
    SUP -. "sondes" .-> FIC
    SUP -. "sondes" .-> WIFI
    SUP -. "sondes" .-> IMP
    SUP -. "sondes" .-> R
    SUP -. "sondes" .-> FW
    SUP ==> |"alertes E-mail + Telegram"| ADMIN

    classDef superviseur fill:#0d6efd,stroke:#fff,color:#fff,stroke-width:2px;
    class SUP superviseur;
```

## Lecture du schéma

- Le **serveur de supervision** (192.168.1.100) est placé dans le **datacenter**,
  au plus près des équipements critiques, mais il sonde l'ensemble du LAN à
  travers les switches et le routeur.
- Les **flux de sondage** (lignes pointillées) sont des paquets ICMP (ping) et
  des connexions TCP vers les ports de service — trafic très léger, sans impact
  notable sur la bande passante.
- Les **flux d'alerte** (flèche pleine) partent du serveur vers l'extérieur :
  e-mail via SMTP et notification Telegram via Internet (HTTPS), atteignant
  l'administrateur **où qu'il soit**, y compris hors du site.

## Recommandations de placement

1. Placer le serveur sur un **VLAN d'administration** dédié pour isoler le
   trafic de supervision.
2. Lui affecter une **adresse IP fixe** (essentiel : c'est un service permanent).
3. Autoriser dans le pare-feu les **flux sortants** SMTP (587) et HTTPS (443)
   pour les notifications.
4. Prévoir un **onduleur (UPS)** : un serveur de supervision doit rester en vie
   pendant les coupures qu'il est censé détecter.
