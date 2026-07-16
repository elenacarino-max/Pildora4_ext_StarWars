import unittest

from core.holocrons import HOLOCRONS
from core.missions import CHAMBERS, MISSIONS, ORIENTATIVE_RESULTS


class GameContentTests(unittest.TestCase):
    def test_expected_content_counts(self):
        self.assertEqual(len(CHAMBERS), 6)
        self.assertEqual(len(MISSIONS), 3)
        self.assertEqual(len(HOLOCRONS), 7)

    def test_all_missions_have_results(self):
        self.assertEqual({item["id"] for item in MISSIONS}, set(ORIENTATIVE_RESULTS))


if __name__ == "__main__":
    unittest.main()
