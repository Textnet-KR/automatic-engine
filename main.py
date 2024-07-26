"""
Markdown Table Converter의 명령줄 인터페이스를 제공하는 메인 스크립트입니다.

이 스크립트는 입력 및 출력 파일 경로를 명령줄 인자로 받아
MarkdownTableConverter 클래스를 실행합니다.
"""

import argparse
from markdown_table_converter import MarkdownTableConverter

if __name__ == "__main__":
    # 명령줄 인자 파서 생성
    parser = argparse.ArgumentParser(description='Markdown Table Converter')

    # 입력 파일 경로 인자 추가
    parser.add_argument('input_file', help='Input Excel file path')

    # 출력 파일 경로 인자 추가
    parser.add_argument('output_file', help='Output Excel file path')

    # 명령줄 인자 파싱
    args = parser.parse_args()

    # MarkdownTableConverter 인스턴스 생성 및 실행
    converter = MarkdownTableConverter(args.input_file, args.output_file)
    converter.run()
