-- ============================================================
-- Supervision Réseau - Schéma MySQL
-- ============================================================

CREATE DATABASE IF NOT EXISTS supervision_reseau
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE supervision_reseau;

-- Création de l'utilisateur applicatif
CREATE USER IF NOT EXISTS 'supervisor'@'localhost' IDENTIFIED BY 'SuperPass2024!';
GRANT ALL PRIVILEGES ON supervision_reseau.* TO 'supervisor'@'localhost';
FLUSH PRIVILEGES;

-- ============================================================
-- Table 1 : equipements
-- ============================================================
CREATE TABLE IF NOT EXISTS equipements (
    id                    INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom                   VARCHAR(100)  NOT NULL,
    ip                    VARCHAR(45)   NOT NULL UNIQUE,
    type                  VARCHAR(50)   NOT NULL DEFAULT 'inconnu',
    localisation          VARCHAR(150)  NOT NULL DEFAULT '',
    statut                ENUM('actif','inactif','inconnu') NOT NULL DEFAULT 'inconnu',
    date_ajout            DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    derniere_verification DATETIME      NULL,
    INDEX idx_statut (statut),
    INDEX idx_ip     (ip)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table 2 : historique_statuts
-- ============================================================
CREATE TABLE IF NOT EXISTS historique_statuts (
    id             INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    equipement_id  INT UNSIGNED NOT NULL,
    statut_ancien  ENUM('actif','inactif','inconnu') NOT NULL,
    statut_nouveau ENUM('actif','inactif','inconnu') NOT NULL,
    timestamp      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipement_id) REFERENCES equipements(id) ON DELETE CASCADE,
    INDEX idx_equipement (equipement_id),
    INDEX idx_timestamp  (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table 3 : journaux
-- ============================================================
CREATE TABLE IF NOT EXISTS journaux (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    equipement_id INT UNSIGNED NULL,
    niveau        ENUM('INFO','WARNING','ERROR','CRITICAL') NOT NULL DEFAULT 'INFO',
    message       TEXT NOT NULL,
    timestamp     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipement_id) REFERENCES equipements(id) ON DELETE SET NULL,
    INDEX idx_equipement (equipement_id),
    INDEX idx_niveau     (niveau),
    INDEX idx_timestamp  (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table 4 : alertes
-- ============================================================
CREATE TABLE IF NOT EXISTS alertes (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    equipement_id INT UNSIGNED NULL,
    type_alerte   VARCHAR(50)  NOT NULL,
    message       TEXT         NOT NULL,
    envoye        TINYINT(1)   NOT NULL DEFAULT 0,
    timestamp     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipement_id) REFERENCES equipements(id) ON DELETE SET NULL,
    INDEX idx_envoye    (envoye),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table 5 : utilisateurs
-- ============================================================
CREATE TABLE IF NOT EXISTS utilisateurs (
    id           INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom          VARCHAR(100) NOT NULL,
    email        VARCHAR(150) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    role         ENUM('admin','lecteur') NOT NULL DEFAULT 'lecteur',
    actif        TINYINT(1)   NOT NULL DEFAULT 1,
    INDEX idx_email (email),
    INDEX idx_role  (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table 6 : rapports
-- ============================================================
CREATE TABLE IF NOT EXISTS rapports (
    id                    INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    periode_debut         DATETIME     NOT NULL,
    periode_fin           DATETIME     NOT NULL,
    nb_equipements        INT UNSIGNED NOT NULL DEFAULT 0,
    disponibilite_moyenne FLOAT        NOT NULL DEFAULT 0.0,
    nb_alertes            INT UNSIGNED NOT NULL DEFAULT 0,
    genere_le             DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_genere_le (genere_le)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Données initiales
-- ============================================================

-- Administrateur par défaut : admin / admin123
-- Mot de passe hashé avec werkzeug generate_password_hash('admin123')
INSERT INTO utilisateurs (nom, email, mot_de_passe, role, actif)
VALUES (
    'Administrateur',
    'admin@supervision.local',
    'pbkdf2:sha256:600000$rKk8cJfQ7mNpLxYz$4a2b8e1d5f3c9a6e2b7d4f1c8a5e9b2d6f3c0a7e4b1d8f5c2a9e6b3d0f7c4a1',
    'admin',
    1
)
ON DUPLICATE KEY UPDATE nom = VALUES(nom);

-- Équipement exemple : passerelle réseau
INSERT INTO equipements (nom, ip, type, localisation, statut)
VALUES ('Passerelle principale', '192.168.1.1', 'routeur', 'Salle serveurs', 'inconnu')
ON DUPLICATE KEY UPDATE nom = VALUES(nom);
