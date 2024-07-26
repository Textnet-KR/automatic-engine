import unittest
from markdown_table_converter import MarkdownTableConverter

class TestMarkdownTableConverter(unittest.TestCase):
    def setUp(self):
        self.converter = MarkdownTableConverter('test_input.xlsx', 'test_output.xlsx')

    def test_is_markdown_table_row(self):
        self.assertTrue(self.converter._is_markdown_table_row("| Column1 | Column2 |"))
        self.assertFalse(self.converter._is_markdown_table_row("Normal text"))

    def test_convert_md_to_html(self):
        md_table = "| Header1 | Header2 |\n|---------|----------|\n| Value1  | Value2  |"
        html_table = self.converter._convert_md_to_html(md_table)
        self.assertIn('<table class="markdown-table">', html_table)

if __name__ == '__main__':
    unittest.main()