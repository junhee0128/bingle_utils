# Utils
## File Processor
* 설계 목적: 자주 사용하는 유틸리티 모음.
* 서브모듈
  * FileProcessor
    * 목적: 자주 사용하는 파일 처리 함수 모음.
    * 함수 구성
      * load_json(filepath: str) -> dict: json 파일 읽기.
      * save_json(filepath: str, obj: dict): json 파일 쓰기.
