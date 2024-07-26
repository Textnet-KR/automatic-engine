"""
Markdown Table Converter의 그래픽 사용자 인터페이스(GUI)를 제공하는 모듈입니다.

이 모듈은 PyQt5를 사용하여 사용자 친화적인 인터페이스를 구현하며,
사용자가 입력 파일을 선택하고 변환 작업을 수행할 수 있게 합니다.
"""

import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QFileDialog, QLabel, QMessageBox, QComboBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from markdown_table_converter import MarkdownTableConverter
import logging
import pandas as pd


class ConverterApp(QWidget):
    """
    Markdown Table Converter의 그래픽 사용자 인터페이스를 구현하는 클래스입니다.
    """
    def __init__(self):
        """
        ConverterApp 클래스의 생성자입니다.
        GUI 컴포넌트를 초기화하고 기본 출력 디렉토리를 설정합니다.
        """
        super().__init__()
        self.output_dir = os.path.expanduser("~/Documents/MarkdownConverter")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        logging.info(f"출력 디렉토리: {self.output_dir}")
        self.initUI()

    def initUI(self):
        """
        사용자 인터페이스를 초기화하고 구성합니다.
        """
        self.setWindowTitle('Markdown Table Converter')
        self.setGeometry(300, 300, 600, 250)
        self.setWindowIcon(QIcon('icon.png'))

        layout = QVBoxLayout()

        # 입력 파일 선택
        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('입력 파일 선택...')
        input_button = QPushButton('찾아보기')
        input_button.clicked.connect(self.select_input_file)
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(input_button)

        # 열 선택
        self.column_combo = QComboBox()
        self.column_combo.setEnabled(False)
        self.column_combo.setMinimumWidth(500)  # 콤보 박스의 최소 너비를 크게 설정
        self.column_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)  # 내용에 맞게 크기 조정

        # 변환 버튼
        convert_button = QPushButton('변환')
        convert_button.clicked.connect(self.convert)
        convert_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout.addLayout(input_layout)
        layout.addWidget(QLabel('변환할 열:'))
        layout.addWidget(self.column_combo)
        layout.addWidget(convert_button)

        self.setLayout(layout)

    def select_input_file(self):
        """
        입력 파일 선택 대화상자를 열고 선택된 파일의 경로를 설정합니다.
        선택된 파일의 열 목록을 로드합니다.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "엑셀 파일 선택", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_path:
            self.input_edit.setText(file_path)
            self.load_columns(file_path)

    def load_columns(self, file_path):
        """
        선택된 엑셀 파일의 열 목록을 로드하여 콤보 박스에 표시합니다.

        Args:
            file_path (str): 선택된 엑셀 파일의 경로
        """
        try:
            df = pd.read_excel(file_path)
            self.column_combo.clear()
            self.column_combo.addItems(df.columns.tolist())
            self.column_combo.setEnabled(True)
        except Exception as e:
            logging.error(f"Error loading columns: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load columns: {str(e)}")

    def convert(self):
        """
        선택된 파일과 열에 대해 변환 작업을 수행합니다.
        변환 결과를 저장할 위치를 선택하고 변환을 실행합니다.
        """
        input_path = self.input_edit.text()
        selected_column = self.column_combo.currentText()
        if not input_path or not selected_column:
            QMessageBox.warning(self, "Warning", "파일과 열을 선택해 주세요.")
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "저장할 위치 선택", "", "Excel Files (*.xlsx);;All Files (*)")
        if not output_path:
            return

        try:
            converter = MarkdownTableConverter(input_path, output_path, selected_column)
            converter.run()
            QMessageBox.information(self, "성공", "변환이 완료되었습니다.")
        except Exception as e:
            logging.error(f"Error during conversion: {str(e)}")
            QMessageBox.critical(self, "Error", f"변환 중 오류가 발생했습니다: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConverterApp()
    ex.show()
    sys.exit(app.exec_())