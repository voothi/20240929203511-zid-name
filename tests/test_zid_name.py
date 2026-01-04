import unittest
import sys
import os

# Add parent directory to path to import zid_name
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zid_name import process_string

class TestZidName(unittest.TestCase):
    """
    Tests for zid_name.py based on v1.1.0 logic.
    Note: These tests depend on the settings in config.ini (e.g., slug_word_count = 3).
    """

    def test_umlauts_and_eszett(self):
        # Häuser, Schlösser, Füße und Fußball -> haeuser-schloesser-fuesse-und
        input_str = "Häuser, Schlösser, Füße und Fußball sind schön"
        expected = "haeuser-schloesser-fuesse-und"
        self.assertEqual(process_string(input_str), expected)

    def test_capital_umlauts(self):
        # Äpfel Öfen Überraschung -> aepfel-oefen-ueberraschung
        input_str = "Äpfel Öfen Überraschung"
        expected = "aepfel-oefen-ueberraschung"
        self.assertEqual(process_string(input_str), expected)

    def test_capital_eszett(self):
        # STRASSE GROẞ -> strasse-gross
        input_str = "STRASSE GROẞ"
        expected = "strasse-gross"
        self.assertEqual(process_string(input_str), expected)

    def test_zid_with_prefix(self):
        # + 20260104223641 Übung macht den Meister -> + 20260104223641-uebung-macht-den-meister
        input_str = "+ 20260104223641 Übung macht den Meister"
        expected = "+ 20260104223641-uebung-macht-den-meister"
        self.assertEqual(process_string(input_str), expected)

    def test_zid_no_prefix(self):
        # 20260104222054 Große Straße in Berlin -> 20260104222054-grosse-strasse-in-berlin
        input_str = "20260104222054 Große Straße in Berlin"
        expected = "20260104222054-grosse-strasse-in-berlin"
        self.assertEqual(process_string(input_str), expected)

if __name__ == '__main__':
    print("Running zid_name logic tests...")
    unittest.main()
