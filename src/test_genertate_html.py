import unittest

from generate_html import extract_title


class TestHelperFunctions(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Welcome to the blog"
        result = extract_title(markdown)
        self.assertEqual(result, "Welcome to the blog")

    def test_no_title(self):
        markdown = "Welcome to the blog"

        with self.assertRaises(Exception):
            extract_title(markdown)
