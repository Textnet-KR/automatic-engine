import argparse
from markdown_table_converter import MarkdownTableConverter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markdown Table Converter')
    parser.add_argument('input_file', help='Input Excel file path')
    parser.add_argument('output_file', help='Output Excel file path')
    args = parser.parse_args()

    converter = MarkdownTableConverter(args.input_file, args.output_file)
    converter.run()