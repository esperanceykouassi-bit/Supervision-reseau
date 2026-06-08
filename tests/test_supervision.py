# -*- coding: utf-8 -*-
"""
test_supervision.py
===================
Tests unitaires et fonctionnels du système de supervision.

Exécution :
    cd src && python -m pytest ../tests -v

Ces tests valident la logique métier indépendamment de la base de données et
du réseau réel grâce à l'utilisation de « mocks » (simulacres). C'est une
bonne pratique : un test unitaire doit être rapide, déterministe et isolé.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Permet d'importer les modules du dossier ../src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from modules.ping_monitor import _extraire_latence
from modules.service_monitor import PORTS_CONNUS, verifier_port


class TestExtractionLatence(unittest.TestCase):
    """Tests de l'analyse (parsing) de la sortie de la commande ping."""

    def test_format_linux(self):
        sortie = "rtt min/avg/max/mdev = 0.123/12.456/30.789/5.0 ms"
        self.assertAlmostEqual(_extraire_latence(sortie), 12.456, places=2)

    def test_format_windows_francais(self):
        sortie = "Minimum = 1ms, Maximum = 4ms, Moyenne = 2ms"
        self.assertEqual(_extraire_latence(sortie), 2.0)

    def test_format_windows_anglais(self):
        sortie = "Minimum = 1ms, Maximum = 4ms, Average = 3ms"
        self.assertEqual(_extraire_latence(sortie), 3.0)

    def test_aucune_latence(self):
        self.assertIsNone(_extraire_latence("Destination Host Unreachable"))


class TestSondeService(unittest.TestCase):
    """Tests de la sonde de services TCP."""

    def test_ports_connus(self):
        # Vérifie que les ports standards sont correctement définis.
        self.assertEqual(PORTS_CONNUS["HTTP"], 80)
        self.assertEqual(PORTS_CONNUS["SSH"], 22)
        self.assertEqual(PORTS_CONNUS["MYSQL"], 3306)

    @patch("modules.service_monitor.socket.socket")
    def test_port_ouvert(self, mock_socket):
        # On simule une connexion réussie (connect_ex retourne 0).
        instance = MagicMock()
        instance.connect_ex.return_value = 0
        mock_socket.return_value = instance

        ouvert, temps = verifier_port("192.168.1.1", 80)
        self.assertTrue(ouvert)
        self.assertIsNotNone(temps)

    @patch("modules.service_monitor.socket.socket")
    def test_port_ferme(self, mock_socket):
        # On simule un port fermé (connect_ex retourne un code non nul).
        instance = MagicMock()
        instance.connect_ex.return_value = 111  # Connection refused
        mock_socket.return_value = instance

        ouvert, temps = verifier_port("192.168.1.1", 80)
        self.assertFalse(ouvert)
        self.assertIsNone(temps)


class TestLogiqueAlerte(unittest.TestCase):
    """Test de la logique de comptage des échecs consécutifs."""

    @patch("supervisor.database.get_journaux")
    def test_seuil_echecs(self, mock_journaux):
        import supervisor
        # Simule 3 échecs consécutifs suivis d'un succès.
        mock_journaux.return_value = [
            {"statut": "DOWN"}, {"statut": "DOWN"}, {"statut": "DOWN"},
            {"statut": "UP"},
        ]
        self.assertEqual(supervisor._compter_echecs_consecutifs(1), 3)

    @patch("supervisor.database.get_journaux")
    def test_aucun_echec(self, mock_journaux):
        import supervisor
        mock_journaux.return_value = [{"statut": "UP"}, {"statut": "DOWN"}]
        self.assertEqual(supervisor._compter_echecs_consecutifs(1), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
