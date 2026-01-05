import unittest
from unittest.mock import patch
import sys
import os

# Add parent directory to path to import zid_name
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zid_name import process_string

class TestZidLogic(unittest.TestCase):
    """
    Tests for ZID detection, batch processing, and prefix handling.
    """

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
            'extension_nesting_level': 0,
            'add_extension_to_slug': False,
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
            'extension_nesting_level': 0,
            'add_extension_to_slug': False,
            'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
            'lowercase': True,
            'separator': '-',
            'replacements': {
                 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
                 'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '.': '-'
            }
        }
        
        input_str = """20260105120000 Task One
# This is a heading
Simple Title
- [ ] Task without ZID
  1. Numbered Task"""
        
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
        input_str = "# My Header"
        expected = "my-header"
        self.assertEqual(process_string(input_str), expected)

if __name__ == '__main__':
    unittest.main()
