import unittest
from unittest.mock import patch
import sys
import os

# Add parent directory to path to import zid_name
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zid_name import process_string

class TestExtensions(unittest.TestCase):
    """
    Tests for extension nesting and slug preservation options.
    """

    @patch('zid_name.get_config')
    def test_extension_nesting(self, mock_get_config):
        # Base config settings
        base_config = {
            'slug_word_count': 10,
            'process_non_zid_lines': False,
            'preserve_extension_depth': 0,
            'slugify_extension_depth': 0,
            'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
            'lowercase': True,
            'separator': '-',
            'replacements': {
                 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
                 'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '.': '-'
            }
        }
        
        input_str = "file Name.1.ru.mp4"
        
        # Level 0 (Default)
        config_0 = base_config.copy()
        config_0['preserve_extension_depth'] = 0
        mock_get_config.return_value = config_0
        self.assertEqual(process_string(input_str), "file-name-1-ru-mp4")
        
        # Level 1
        config_1 = base_config.copy()
        config_1['preserve_extension_depth'] = 1
        mock_get_config.return_value = config_1
        self.assertEqual(process_string(input_str), "file-name-1-ru.mp4")
        
        # Level 2
        config_2 = base_config.copy()
        config_2['preserve_extension_depth'] = 2
        mock_get_config.return_value = config_2
        self.assertEqual(process_string(input_str), "file-name-1.ru.mp4")
        
        # Level 4 (Oversized fallback)
        config_4 = base_config.copy()
        config_4['preserve_extension_depth'] = 4
        mock_get_config.return_value = config_4
        self.assertEqual(process_string(input_str), "file-name.1.ru.mp4")


    @patch('zid_name.get_config')
    def test_extension_nesting_fallback(self, mock_get_config):
        base_config = {
            'slug_word_count': 10,
            'process_non_zid_lines': False,
            'preserve_extension_depth': 2,
            'slugify_extension_depth': 0,
            'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
            'lowercase': True,
            'separator': '-',
            'replacements': {
                 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
                 'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '.': '-'
            }
        }
        mock_get_config.return_value = base_config
        
        # Scenario 1: Fallback (Requested 2, got 1)
        input_str = "20251019150118 33716113-5cdf-4b25-b357-b30900efd993.avif"
        expected = "20251019150118-33716113-5cdf-4b25-b357-b30900efd993.avif"
        self.assertEqual(process_string(input_str), expected)
        
        # Scenario 2: Simple file
        self.assertEqual(process_string("Image.png"), "image.png")
        
        # Scenario 3: Exact match
        self.assertEqual(process_string("Archive.tar.gz"), "archive.tar.gz")

    @patch('zid_name.get_config')
    def test_add_extension_to_slug(self, mock_get_config):
        base_config = {
            'slug_word_count': 4,
            'process_non_zid_lines': False,
            'preserve_extension_depth': 0, 
            'slugify_extension_depth': 1,
            'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
            'lowercase': True,
            'separator': '-',
            'replacements': {
                 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
                 'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '.': '-'
            }
        }
        mock_get_config.return_value = base_config
        
        input_str = "20251114155621 IT Projektleiter _ Projektmanager (m_w_d) bei HENRICHSEN AG _ softgarden.pdf"
        expected = "20251114155621-it-projektleiter-projektmanager-pdf"
        self.assertEqual(process_string(input_str), expected)
        
        self.assertEqual(process_string("File.png"), "file-png")

if __name__ == '__main__':
    unittest.main()
