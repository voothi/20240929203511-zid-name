import unittest
from unittest.mock import patch
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

    def test_sentence_boundary(self):
        input_str = "Title. Description"
        expected = "title-description"
        self.assertEqual(process_string(input_str), expected)

    def test_no_wikilinks(self):
        # Explicit verify that we do NOT get [[...]]
        input_str = "20260105120000 Simple Task"
        output = process_string(input_str)
        self.assertNotIn("[[", output)
        self.assertNotIn("]]", output)
        self.assertEqual(output, "20260105120000-simple-task")

    def test_user_complex_scenario(self):
        # Specific user requested case
        input_str = """- [ ] 20260105120000 Task One
- [x] 20260105120001 Task Two - 
Just some comment
20260105122633 Just some comment
  * 20260105120002 Indented Task"""
        
        expected = """- [ ] 20260105120000-task-one
- [x] 20260105120001-task-two
Just some comment
20260105122633-just-some-comment
  * 20260105120002-indented-task"""
        
        self.assertEqual(process_string(input_str), expected)

    @patch('zid_name.get_config')
    def test_process_non_zid_lines_false(self, mock_get_config):
        # MOCK config: process_non_zid_lines = False
        mock_get_config.return_value = {
            'slug_word_count': 4,
            'process_non_zid_lines': False,
            'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
            'lowercase': True,
            'separator': '-',
            'replacements': {
                 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
                 'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '.': '-'
            }
        }
        
        # Test input with NO ZID (Single Line)
        input_str = "Simple Title"
        # Smart logic: Single lines are always sanitized (legacy/substring support)
        # even if process_non_zid_lines is False.
        expected = "simple-title"
        self.assertEqual(process_string(input_str), expected)
        
        # Mixed content
        input_str = """20260105120000 Task One
Simple Title"""
        expected = """20260105120000-task-one
Simple Title"""
        self.assertEqual(process_string(input_str), expected)

    @patch('zid_name.get_config')
    def test_process_non_zid_lines_true(self, mock_get_config):
        # MOCK config: process_non_zid_lines = True
        mock_get_config.return_value = {
            'slug_word_count': 4,
            'process_non_zid_lines': True, # ENABLED
            'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
            'lowercase': True,
            'separator': '-',
            'replacements': {
                 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
                 'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '.': '-'
            }
        }
        
        # Test input with mixed content
        input_str = """20260105120000 Task One
# This is a heading
Simple Title
- [ ] Task without ZID
  1. Numbered Task"""
        
        # Heading with ZID should be processed
        # Ordinary line should stay since process_non_zid_lines=True (mocked)
        # But we previously had # This is a heading as preservation. Now it should be sanitized if True.
        expected = """20260105120000-task-one
# this-is-a-heading
simple-title
- [ ] task-without-zid
  1. numbered-task"""
        
        self.assertEqual(process_string(input_str), expected)

    def test_heading_with_zid(self):
        input_str = "## 20260105131245 Just some notes here."
        expected = "## 20260105131245-just-some-notes-here"
        self.assertEqual(process_string(input_str), expected)

    def test_heading_preservation_single_line(self):
        # Even if it's a heading, if it's a SINGLE line selection, 
        # we still sanitize it (for filename creation from heading).
        input_str = "# My Header"
        expected = "my-header"
        self.assertEqual(process_string(input_str), expected)

    @patch('zid_name.get_config')
    def test_extension_nesting(self, mock_get_config):
        # Base config settings
        base_config = {
            'slug_word_count': 10, # Large count to keep all words for this test
            'process_non_zid_lines': False,
            'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
            'lowercase': True,
            'separator': '-',
            'replacements': {
                 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
                 'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '.': '-'
            }
        }
        
        input_str = "file Name.1.ru.mp4"
        
        # Level 0 (Default config) - should be file-name-1-ru-mp4
        config_0 = base_config.copy()
        config_0['extension_nesting_level'] = 0
        mock_get_config.return_value = config_0
        self.assertEqual(process_string(input_str), "file-name-1-ru-mp4")
        
        # Level 1 - should be file-name-1-ru.mp4
        config_1 = base_config.copy()
        config_1['extension_nesting_level'] = 1
        mock_get_config.return_value = config_1
        self.assertEqual(process_string(input_str), "file-name-1-ru.mp4")
        
        # Level 2 - should be file-name-1.ru.mp4
        config_2 = base_config.copy()
        config_2['extension_nesting_level'] = 2
        mock_get_config.return_value = config_2
        self.assertEqual(process_string(input_str), "file-name-1.ru.mp4")
        
        # Level 3 - should be file-name.1.ru.mp4
        config_3 = base_config.copy()
        config_3['extension_nesting_level'] = 3
        mock_get_config.return_value = config_3
        self.assertEqual(process_string(input_str), "file-name.1.ru.mp4")
        
        # Level 10 (High level) - should be just extension parts if too many?
        # New "Up to" logic: min(level, len(parts)-1).
        # "file Name.1.ru.mp4" (4 parts). len-1 = 3.
        # Level 4 implies we want up to 4 extensions. We have 3.
        # So we preserve 3.
        
        config_4 = base_config.copy()
        config_4['extension_nesting_level'] = 4
        mock_get_config.return_value = config_4
        self.assertEqual(process_string(input_str), "file-name.1.ru.mp4")


    @patch('zid_name.get_config')
    def test_extension_nesting_fallback(self, mock_get_config):
        # Case specific to user report:
        # File "file.avif" (single extension) BUT level set to 2.
        # Should gracefully fallback to level 1 for this file.
        
        base_config = {
            'slug_word_count': 10,
            'process_non_zid_lines': False,
            'extension_nesting_level': 2, # Requesting 2 levels
            'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
            'lowercase': True,
            'separator': '-',
            'replacements': {
                 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
                 'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '.': '-'
            }
        }
        mock_get_config.return_value = base_config
        
        # Scenario 1: Actual ZID line from user report
        # "20251019150118 33716113-5cdf-4b25-b357-b30900efd993.avif"
        # Expectation: ZID preserved, stem sanitized (already clean), extension ".avif" preserved.
        input_str = "20251019150118 33716113-5cdf-4b25-b357-b30900efd993.avif"
        expected = "20251019150118-33716113-5cdf-4b25-b357-b30900efd993.avif"
        self.assertEqual(process_string(input_str), expected)
        
        # Scenario 2: Simple file "image.png" with level 2
        input_str = "Image.png"
        expected = "image.png"
        self.assertEqual(process_string(input_str), expected)
        
        # Scenario 3: "archive.tar.gz" with level 2 (Exact match)
        input_str = "Archive.tar.gz"
        expected = "archive.tar.gz"
        self.assertEqual(process_string(input_str), expected)
        
        # Scenario 4: "my.archive.tar.gz" with level 2
        input_str = "My.Archive.tar.gz"
        expected = "my-archive.tar.gz" # Stem: "My.Archive" -> "my-archive", Ext: ".tar.gz"
        self.assertEqual(process_string(input_str), expected)

    def test_separator_deduplication(self):
        # Test that double separators are collapsed
        # Case: "foo. bar" -> with repls {'.': '-'} -> "foo- bar" -> "foo--bar" -> "foo-bar"
        input_str = "foo. bar"
        expected = "foo-bar"
        # Since we use default config in unit tests (where main gets used), we need to ensure config is right.
        # But wait, unit tests use process_string which uses get_config. 
        # test utils normally rely on the file config OR mocked config.
        # Let's rely on default mock if we can, or just mock it here to be safe.
        
        # We can reuse the pattern from other tests if we want specific config, 
        # but let's see if we can just pass a string that generates double separator naturally via split/join.
        # "Word One  Word Two" -> "word-one--word-two" (if split preserves empty strings? no split() consumes multiple spaces)
        # "Word One - Word Two" -> "word-one---word-two" (dash is repl?)
        # Let's use specific chars.
        
        # Config has {'.': '-'} by default.
        # Input: "A. B" -> "A- B" -> split -> "A-", "B" -> join -> "A--B" -> collapse -> "A-B"
        self.assertEqual(process_string("A. B"), "a-b")
        
        # Input: "Header - Subheader" -> "Header - Subheader" -> split -> "Header", "-", "Subheader" -> join -> "header---subheader" -> "header-subheader"
        # Wait, allowed chars regex might strip loose dashes?
        # Default allowed: [^a-zA-Z... -] (dash included).
        # So "Header - Subheader".
        # split -> ["Header", "-", "Subheader"]
        # join with "-" -> "Header---Subheader"
        # collapse -> "Header-Subheader"
        self.assertEqual(process_string("Header - Subheader"), "header-subheader")

if __name__ == '__main__':
    print("Running zid_name logic tests...")
    unittest.main()
