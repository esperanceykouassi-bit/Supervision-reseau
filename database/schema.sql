-- ====================================================================== --
--  SCRIPT SQL COMPLET — Base de données « supervision »                  --
--  Système d'automatisation de la supervision réseau                     --
--  SGBD : MySQL 8.x / MariaDB 10.x                                       --
--                                                                        --
--  Exécution :                                                           --
--    mysql -u root -p < schema.sql                                       --
-- ====================================================================== --

-- Création de la base avec un jeu de caractères Unicode complet (emojis ok).
CREATE DATABASE IF NOT EXISTS supervision
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE supervision;

-- Création d'un utilisateur applicatif dédié (principe du moindre privilège).
-- En production, restreindre l'hôte ('localhost') et les droits accordés.
CREATE USER IF NOT EXISTS 'supervisor'@'localhost' IDENTIFIED BY 'supervision_pass';
GRANT SELECT, INSERT, UPDATE, DELETE ON supervision.* TO 'supervisor'@'localhost';
FLUSH PRIVILEGES;

-- ---------------------------------------------------------------------- --
--  Table : utilisateurs                                                  --
--  Comptes d'accès au tableau de bord. Le mot de passe est stocké        --
--  uniquement sous forme de hachage (jamais en clair).                   --
-- ---------------------------------------------------------------------- --
CREATE TABLE IF NOT EXISTS utilisateurs (
    id                 INT AUTO_INCREMENT PRIMARY KEY,
    identifiant        VARCHAR(50)  NOT NULL UNIQUE,
    mot_de_passe_hash  VARCHAR(255) NOT NULL,
    nom_complet        VARCHAR(100),
    email              VARCHAR(120),
    role               ENUM('admin', 'operateur', 'lecteur') NOT NULL DEFAULT 'operateur',
    actif              TINYINT(1) NOT NULL DEFAULT 1,
    date_creation      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------- --
--  Table : equipements                                                   --
--  Inventaire des équipements supervisés et leur état courant.           --
-- ---------------------------------------------------------------------- --
CREATE TABLE IF NOT EXISTS equipements (
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    nom                   VARCHAR(100) NOT NULL,
    adresse_ip            VARCHAR(45)  NOT NULL,          -- IPv4/IPv6
    type_equipement       VARCHAR(50)  NOT NULL,          -- Routeur, Switch, Serveur...
    emplacement           VARCHAR(150),
    service_supervise     VARCHAR(20),                    -- HTTP, SSH, MYSQL... (optionnel)
    statut                ENUM('UP', 'DOWN', 'INCONNU') NOT NULL DEFAULT 'INCONNU',
    latence_ms            FLOAT,
    derniere_verification DATETIME,
    actif                 TINYINT(1) NOT NULL DEFAULT 1,
    date_ajout            DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_statut (statut),
    INDEX idx_actif (actif),
    UNIQUE KEY uniq_ip (adresse_ip)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------- --
--  Table : journaux                                                      --
--  Historique de CHAQUE vérification (base des statistiques de dispo).   --
-- ---------------------------------------------------------------------- --
CREATE TABLE IF NOT EXISTS journaux (
    id             BIGINT AUTO_INCREMENT PRIMARY KEY,
    equipement_id  INT NOT NULL,
    statut         ENUM('UP', 'DOWN') NOT NULL,
    latence_ms     FLOAT,
    message        VARCHAR(255),
    date_evenement DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_equip_date (equipement_id, date_evenement),
    CONSTRAINT fk_journal_equip FOREIGN KEY (equipement_id)
        REFERENCES equipements(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------- --
--  Table : alertes                                                       --
--  Alertes émises, leur canal de diffusion et leur acquittement.         --
-- ---------------------------------------------------------------------- --
CREATE TABLE IF NOT EXISTS alertes (
    id                 BIGINT AUTO_INCREMENT PRIMARY KEY,
    equipement_id      INT NOT NULL,
    type_alerte        VARCHAR(50) NOT NULL,    -- PANNE_RESEAU, SERVICE_INDISPONIBLE...
    severite           ENUM('CRITIQUE', 'AVERTISSEMENT', 'INFO') NOT NULL DEFAULT 'CRITIQUE',
    message            VARCHAR(255),
    canal              VARCHAR(50),             -- EMAIL+TELEGRAM
    acquittee          TINYINT(1) NOT NULL DEFAULT 0,
    acquittee_par      INT,                     -- utilisateur ayant acquitté l'alerte
    date_alerte        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_acquittement  DATETIME,
    INDEX idx_acquittee (acquittee),
    INDEX idx_equip (equipement_id),
    CONSTRAINT fk_alerte_equip FOREIGN KEY (equipement_id)
        REFERENCES equipements(id) ON DELETE CASCADE,
    -- Relation « UN UTILISATEUR acquitte PLUSIEURS alertes » (1,n).
    CONSTRAINT fk_alerte_user FOREIGN KEY (acquittee_par)
        REFERENCES utilisateurs(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------- --
--  Table : responsabilite (association UTILISATEUR <-> EQUIPEMENT)       --
--  Matérialise la relation « plusieurs-à-plusieurs » : un utilisateur    --
--  (technicien) SUPERVISE plusieurs équipements, et un équipement peut   --
--  être pris en charge par plusieurs utilisateurs.                       --
-- ---------------------------------------------------------------------- --
CREATE TABLE IF NOT EXISTS responsabilite (
    utilisateur_id   INT NOT NULL,
    equipement_id    INT NOT NULL,
    date_affectation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (utilisateur_id, equipement_id),     -- clé primaire composite
    CONSTRAINT fk_resp_user FOREIGN KEY (utilisateur_id)
        REFERENCES utilisateurs(id) ON DELETE CASCADE,
    CONSTRAINT fk_resp_equip FOREIGN KEY (equipement_id)
        REFERENCES equipements(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------- --
--  Table : statistiques                                                  --
--  Agrégats journaliers (instantanés) pour les rapports de tendance.     --
--  Alimentée par une tâche planifiée (ex. une fois par jour).            --
-- ---------------------------------------------------------------------- --
CREATE TABLE IF NOT EXISTS statistiques (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    date_stat           DATE NOT NULL,
    total_equipements   INT NOT NULL,
    equipements_up      INT NOT NULL,
    equipements_down    INT NOT NULL,
    taux_disponibilite  FLOAT NOT NULL,
    latence_moyenne     FLOAT,
    nombre_alertes      INT NOT NULL DEFAULT 0,
    UNIQUE KEY uniq_jour (date_stat)
) ENGINE=InnoDB;

-- ====================================================================== --
--  DONNÉES INITIALES (jeu de test / amorçage)                            --
-- ====================================================================== --

-- Compte administrateur par défaut.
-- Identifiant : admin   /   Mot de passe : admin123
-- Le hash ci-dessous est généré par Werkzeug (pbkdf2:sha256).
-- ⚠️ À CHANGER impérativement dès la première connexion en production.
INSERT INTO utilisateurs (identifiant, mot_de_passe_hash, nom_complet, email, role)
VALUES (
    'admin',
    'pbkdf2:sha256:600000$aB3xK9mQ2pL5nR7t$95cee5a607296113ba18e4dfcfad339ecce530c0c7b2fe99ac8fb76834f68aac',
    'Administrateur Système',
    'admin@exemple.com',
    'admin'
) ON DUPLICATE KEY UPDATE identifiant = identifiant;

-- Équipements d'exemple (topologie réaliste d'un petit réseau d'entreprise).
INSERT INTO equipements (nom, adresse_ip, type_equipement, emplacement, service_supervise, statut)
VALUES
    ('Routeur-Principal',   '192.168.1.1',   'Routeur',  'Salle technique',  NULL,    'INCONNU'),
    ('Switch-Etage1',       '192.168.1.2',   'Switch',   'Étage 1',          NULL,    'INCONNU'),
    ('Serveur-Web',         '192.168.1.10',  'Serveur',  'Datacenter',       'HTTP',  'INCONNU'),
    ('Serveur-BDD',         '192.168.1.11',  'Serveur',  'Datacenter',       'MYSQL', 'INCONNU'),
    ('Serveur-Fichiers',    '192.168.1.12',  'Serveur',  'Datacenter',       'SSH',   'INCONNU'),
    ('Point-Acces-WiFi',    '192.168.1.20',  'Borne',    'Hall accueil',     NULL,    'INCONNU'),
    ('Imprimante-RH',       '192.168.1.30',  'Imprimante','Bureau RH',       NULL,    'INCONNU'),
    ('Pare-feu',            '192.168.1.254', 'Firewall', 'Salle technique',  NULL,    'INCONNU')
ON DUPLICATE KEY UPDATE nom = VALUES(nom);

-- Affectations d'exemple (relation « supervise ») : l'administrateur est
-- responsable de quelques équipements. On résout les identifiants par sous-requête
-- pour ne pas dépendre de l'ordre d'auto-incrémentation.
INSERT IGNORE INTO responsabilite (utilisateur_id, equipement_id)
SELECT u.id, e.id
FROM utilisateurs u
JOIN equipements e ON e.adresse_ip IN ('192.168.1.1', '192.168.1.10', '192.168.1.11')
WHERE u.identifiant = 'admin';
