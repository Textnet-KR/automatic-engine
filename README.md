# Markdown Table Converter

이 프로젝트는 엑셀 파일 내의 마크다운 테이블을 HTML 테이블로 변환하는 파이썬 스크립트입니다.

## 기능

- 엑셀 파일에서 마크다운 테이블 식별
- 마크다운 테이블을 HTML로 변환
- HTML5 표준을 준수하는 테이블 생성
- CSS 스타일 적용

## 설치

1. 이 저장소를 클론합니다:    
git clone https://github.com/Textnet-KR/automatic-engine.git    
cd automatic-engine
2. 필요한 패키지를 설치합니다:    
pip install pandas openpyxl markdown numpy
## 사용법

1. 명령줄에서 다음과 같이 스크립트를 실행합니다:    
python main.py input.xlsx output.xlsx    
여기서 `input.xlsx`는 변환할 마크다운 테이블이 포함된 입력 파일이고, `output.xlsx`는 결과가 저장될 출력 파일입니다.

2. 스크립트는 입력 파일을 처리하고 결과를 출력 파일에 저장합니다.    
현재는 첫 번째 열의 데이터들만 처리합니다.

3. 로그 파일 `converter.log`가 생성되며, 여기에 실행 과정의 세부 정보가 기록됩니다.

## 테스트

단위 테스트를 실행하려면 다음 명령을 사용하세요:    
python test_markdown_table_converter.py

## 프로젝트 구조

- `markdown_table_converter.py`: 주요 변환 로직을 포함하는 클래스
- `main.py`: 명령줄 인터페이스 및 실행 스크립트
- `test_markdown_table_converter.py`: 단위 테스트

## 기여

버그 리포트, 기능 제안, 풀 리퀘스트는 언제나 환영합니다. 큰 변경사항의 경우, 먼저 이슈를 열어 논의해 주세요.

## 라이선스

이 프로젝트는 TEXTNET 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
