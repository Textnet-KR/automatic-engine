import pandas as pd
import markdown
import re
from typing import Tuple
import logging
import numpy as np

class MarkdownTableConverter:
    """
    엑셀 파일에서 마크다운 테이블을 HTML 테이블로 변환하는 클래스.
    """

    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None

        # 로깅 설정
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('converter.log')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def _load_excel(self) -> bool:
        """
        엑셀 파일을 로드하고 컬럼 이름을 설정.

        Returns:
            bool: 성공적으로 로드되면 True, 그렇지 않으면 False
        """
        try:
            self.df = pd.read_excel(self.input_path, header=None)
            self.df.columns = ["Original_Text"]
            self.logger.info("엑셀 파일 로드 완료. 컬럼: %s", self.df.columns)
            return True
        except Exception as e:
            self.logger.error("엑셀 파일 로드 실패: %s", str(e), exc_info=True)
            return False

    @staticmethod
    def _is_markdown_table_row(line: str) -> bool:
        """
        주어진 문자열이 마크다운 테이블의 행인지 확인.

        Args:
            line (str): 확인할 문자열

        Returns:
            bool: 마크다운 테이블 행이면 True, 그렇지 않으면 False
        """
        return bool(re.match(r"^\s*\|(.+\|)+\s*$", line))

    @staticmethod
    def _is_markdown_table_separator(line: str) -> bool:
        """
        주어진 문자열이 마크다운 테이블의 구분자 행인지 확인.

        Args:
            line (str): 확인할 문자열

        Returns:
            bool: 마크다운 테이블 구분자 행이면 True, 그렇지 않으면 False
        """
        return bool(re.match(r"^\s*\|(\s*:?-+:?\s*\|)+\s*$", line))

    def _find_markdown_table(self, text: str) -> Tuple[str, str, str]:
        """
        텍스트에서 마크다운 테이블을 찾아 분리.

        Args:
            text (str): 입력 텍스트

        Returns:
            Tuple[str, str, str]: 테이블 이전 텍스트, 마크다운 테이블, 테이블 이후 텍스트
        """
        lines = text.split("\n")
        table_start, table_end = -1, -1

        for i, line in enumerate(lines):
            if table_start == -1:
                if (self._is_markdown_table_row(line) and
                        i + 1 < len(lines) and
                        self._is_markdown_table_separator(lines[i + 1])):
                    table_start = i
            elif not self._is_markdown_table_row(line):
                table_end = i
                break

        if table_start != -1 and table_end == -1:
            table_end = len(lines)

        if table_start != -1 and table_end != -1:
            return (
                "\n".join(lines[:table_start]),
                "\n".join(lines[table_start:table_end]),
                "\n".join(lines[table_end:]),
            )

        return text, "", ""

    @staticmethod
    def _convert_md_to_html(md_table: str) -> str:
        """
        마크다운 테이블을 HTML로 변환하고, 스타일 정보를 유지하면서 HTML5 표준을 준수.

        Args:
            md_table (str): 마크다운 테이블 문자열

        Returns:
            str: HTML 테이블 문자열
        """
        html = markdown.markdown(md_table, extensions=["tables"])
        html = re.sub(
            r'style="text-align:\s*(left|center|right);"',
            r'data-style="text-align: \1;"',
            html,
        )
        html = html.replace("<table>", '<table class="markdown-table">')
        return html

    @staticmethod
    def _generate_css() -> str:
        """
        마크다운 테이블 스타일을 위한 CSS 생성.

        Returns:
            str: CSS 문자열
        """
        return """
        <style>
        .markdown-table {
            border-collapse: collapse;
            width: 100%;
        }
        .markdown-table th, .markdown-table td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .markdown-table th[data-style*="text-align: left"],
        .markdown-table td[data-style*="text-align: left"] {
            text-align: left;
        }
        .markdown-table th[data-style*="text-align: center"],
        .markdown-table td[data-style*="text-align: center"] {
            text-align: center;
        }
        .markdown-table th[data-style*="text-align: right"],
        .markdown-table td[data-style*="text-align: right"] {
            text-align: right;
        }
        </style>
        """

    def _process_text(self, text: str) -> Tuple[str, str, str, str, str, str]:
        """
        텍스트를 처리하여 필요한 컬럼 데이터 생성.

        Args:
            text (str): 처리할 텍스트

        Returns:
            Tuple[str, str, str, str, str, str]: 변환된 텍스트, 마크다운 테이블, HTML 테이블, CSS, HTML5 준수 텍스트, 최종 HTML (CSS 포함)
        """
        text_before, md_table, text_after = self._find_markdown_table(text)
        if md_table:
            html_table = self._convert_md_to_html(md_table)
            css = self._generate_css()
            html5_compliant = f"{text_before}\n{html_table}\n{text_after}"
            return (
                text_before + text_after,
                md_table,
                html_table,
                css,
                html5_compliant,
                f"{text_before}\n{css}\n{html_table}\n{text_after}",
            )
        return text, "", "", "", text, text

    def _process_dataframe(self):
        """데이터프레임의 각 행을 처리."""
        if self.df is None:
            self.logger.error("데이터프레임이 로드되지 않았습니다.")
            return

        self.logger.info("데이터프레임 처리 시작")
        try:
            # 벡터화된 함수 정의
            vectorized_process = np.vectorize(self._process_text, otypes=[object] * 6)

            # 벡터화된 연산 적용
            results = vectorized_process(self.df['Original_Text'])

            # 결과를 데이터프레임에 할당
            self.df['Text_Without_Table'], self.df['Markdown_Table'], self.df['HTML_Table'], \
                self.df['CSS'], self.df['HTML5_Compliant'], self.df['Final_HTML_with_CSS'] = results

            self.logger.info("데이터프레임 처리 완료")
        except Exception as e:
            self.logger.error("데이터프레임 처리 중 오류 발생: %s", str(e), exc_info=True)

    def _save_excel(self):
        """데이터프레임을 엑셀 파일로 저장."""
        if self.df is None:
            self.logger.error("저장할 데이터프레임이 없습니다.")
            return

        try:
            self.df.to_excel(self.output_path, index=False, engine="openpyxl")
            self.logger.info(f"처리가 완료되었습니다. 출력 파일은 '{self.output_path}'로 저장되었습니다.")
        except Exception as e:
            self.logger.error(f"엑셀 파일 저장 실패: %s", str(e), exc_info=True)

    def run(self):
        """전체 프로세스 실행."""
        self.logger.info("프로그램 시작")
        if self._load_excel():
            self._process_dataframe()
            self._save_excel()
        self.logger.info("프로그램 종료")

    def run(self):
        """전체 프로세스 실행."""
        self.logger.info("프로그램 시작")
        if self._load_excel():
            self._process_dataframe()
            self._save_excel()
        self.logger.info("프로그램 종료")