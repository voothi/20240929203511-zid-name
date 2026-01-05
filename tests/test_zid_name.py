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

    def test_batch_processing(self):
        # Multi-line input with mixed ZID and non-ZID lines
        input_str = """- [ ] 20260105120000 Task One
- [x] 20260105120001 Task Two
Just some comment
  * 20260105120002 Indented Task"""
        
        expected = """- [ ] 20260105120000-task-one
- [x] 20260105120001-task-two
Just some comment
  * 20260105120002-indented-task"""
        
        self.assertEqual(process_string(input_str), expected)

    def test_trailing_separator(self):
        # Ensure trailing separators are removed 
        # (e.g. "Task One - " should not become "task-one-")
        input_str = "Task One - "
        expected = "task-one"
        self.assertEqual(process_string(input_str), expected)
        
        # With ZID
        input_str = "- [ ] 20260105120000 Task One - "
        expected = "- [ ] 20260105120000-task-one"
        self.assertEqual(process_string(input_str), expected)

    def test_no_wikilinks(self):
        # Explicit verify that we do NOT get [[...]]
        input_str = "20260105120000 Simple Task"
        output = process_string(input_str)
        self.assertNotIn("[[", output)
        self.assertNotIn("]]", output)
        self.assertEqual(output, "20260105120000-simple-task")

if __name__ == '__main__':
    print("Running zid_name logic tests...")
    unittest.main()
