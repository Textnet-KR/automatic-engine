# Markdown Table Converter

이 프로젝트는 엑셀 파일 내의 마크다운 테이블을 HTML 테이블로 변환하는 파이썬 애플리케이션입니다. 명령줄 인터페이스(CLI)와 그래픽 사용자 인터페이스(GUI)를 모두 제공합니다.

## 기능

- 엑셀 파일에서 마크다운 테이블 식별
- 마크다운 테이블을 HTML로 변환
- HTML5 표준을 준수하는 테이블 생성
- CSS 스타일 적용
- 사용자가 선택한 특정 열만 처리 가능
- GUI를 통한 사용자 친화적 인터페이스

## 설치

1. 이 저장소를 클론합니다:    
```bash
git clone https://github.com/Textnet-KR/automatic-engine.git
cd automatic-engine
```
2. 필요한 패키지를 설치합니다:
```bash
pip install pandas openpyxl markdown numpy PyQt5
```
## 사용법

### 명령줄 인터페이스 (CLI)

1. 다음과 같이 스크립트를 실행합니다:
```bash
python main.py input.xlsx output.xlsx
```
여기서 `input.xlsx`는 변환할 마크다운 테이블이 포함된 입력 파일이고, `output.xlsx`는 결과가 저장될 출력 파일입니다.

2. 스크립트는 입력 파일을 처리하고 결과를 출력 파일에 저장합니다.

### 그래픽 사용자 인터페이스 (GUI)

1. 다음 명령으로 GUI 애플리케이션을 실행합니다:
```bash
python gui_app.py
```
2. 애플리케이션 창에서 '찾아보기' 버튼을 클릭하여 입력 파일을 선택합니다.

3. 드롭다운 메뉴에서 처리할 열을 선택합니다.

4. '변환' 버튼을 클릭하고 출력 파일 위치를 선택합니다.

5. 변환이 완료되면 성공 메시지가 표시됩니다.

## 로깅

- 로그 파일 `converter.log`가 생성되며, 여기에 실행 과정의 세부 정보가 기록됩니다.

## 테스트

단위 테스트를 실행하려면 다음 명령을 사용하세요:
```bash
python test_markdown_table_converter.py
```
## 프로젝트 구조

- `markdown_table_converter.py`: 주요 변환 로직을 포함하는 클래스
- `main.py`: 명령줄 인터페이스 및 실행 스크립트
- `gui_app.py`: 그래픽 사용자 인터페이스 애플리케이션
- `test_markdown_table_converter.py`: 단위 테스트

## 기여

버그 리포트, 기능 제안, 풀 리퀘스트는 언제나 환영합니다. 큰 변경사항의 경우, 먼저 이슈를 열어 논의해 주세요.

## 라이선스

이 프로젝트는 TEXTNET 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
