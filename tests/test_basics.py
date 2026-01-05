import unittest
from unittest.mock import patch
import sys
import os

# Add parent directory to path to import zid_name
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zid_name import process_string

class TestBasics(unittest.TestCase):
    """
    Tests for basic string processing, replacements, and formatting.
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
        
    def test_sentence_boundary(self):
        input_str = "Title. Description"
        expected = "title-description"
        self.assertEqual(process_string(input_str), expected)

    def test_separator_deduplication(self):
        # Test that double separators are collapsed
        self.assertEqual(process_string("A. B"), "a-b")
        self.assertEqual(process_string("Header - Subheader"), "header-subheader")

    def test_trailing_separator(self):
        # Ensure trailing separators are removed 
        input_str = "Task One - "
        expected = "task-one"
        self.assertEqual(process_string(input_str), expected)
        
    def test_no_wikilinks(self):
        input_str = "20260105120000 Simple Task"
        output = process_string(input_str)
        self.assertNotIn("[[", output)
        self.assertNotIn("]]", output)
        self.assertEqual(output, "20260105120000-simple-task")

if __name__ == '__main__':
    unittest.main()
