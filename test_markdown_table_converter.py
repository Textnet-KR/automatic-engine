"""
MarkdownTableConverter 클래스의 단위 테스트를 위한 모듈입니다.

이 모듈은 unittest 프레임워크를 사용하여 MarkdownTableConverter 클래스의
주요 메서드들을 테스트합니다.
"""

import unittest
from markdown_table_converter import MarkdownTableConverter

class TestMarkdownTableConverter(unittest.TestCase):
    """MarkdownTableConverter 클래스의 메서드를 테스트하는 클래스입니다."""

    def setUp(self):
        """
        각 테스트 메서드 실행 전에 호출되는 설정 메서드입니다.
        MarkdownTableConverter 인스턴스를 생성합니다.
        """
        self.converter = MarkdownTableConverter('test_input.xlsx', 'test_output.xlsx')

    def test_is_markdown_table_row(self):
        """
        _is_markdown_table_row 메서드를 테스트합니다.
        마크다운 테이블 행을 올바르게 식별하는지 확인합니다.
        """
        self.assertTrue(self.converter._is_markdown_table_row("| Column1 | Column2 |"))
        self.assertFalse(self.converter._is_markdown_table_row("Normal text"))

    def test_convert_md_to_html(self):
        """
        _convert_md_to_html 메서드를 테스트합니다.
        마크다운 테이블이 올바르게 HTML로 변환되는지 확인합니다.
        """
        md_table = "| Header1 | Header2 |\n|---------|----------|\n| Value1  | Value2  |"
        html_table = self.converter._convert_md_to_html(md_table)
        self.assertIn('<table class="markdown-table">', html_table)

if __name__ == '__main__':
    unittest.main()
