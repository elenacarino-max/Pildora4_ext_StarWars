import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp.name) / "game.db"
        self.patcher = patch.object(database, "GAME_DB", self.db_path)
        self.patcher.start()
        database.init_db()

    def tearDown(self):
        self.patcher.stop()
        self.temp.cleanup()

    def test_session_team_and_progress(self):
        session = database.create_session()
        team = database.join_team(session["code"], "Guardianes de Naboo")
        self.assertEqual(team["chamber_index"], 0)
        team = database.complete_chamber(team["id"], 0)
        self.assertEqual(team["chamber_index"], 1)
        self.assertEqual(team["score"], 20)

    def test_defense_rejects_same_run(self):
        session = database.create_session()
        team = database.join_team(session["code"], "Orden de Dagobah")
        payload = {"selected_run":"Tatooine","evidence":"F1","artifact":"matriz",
                   "discarded_run":"Tatooine","discard_reason":"coste",
                   "limitation":"sesgo","recommendation":"revisar"}
        with self.assertRaises(ValueError):
            database.save_defense(team["id"], payload)


if __name__ == "__main__":
    unittest.main()
