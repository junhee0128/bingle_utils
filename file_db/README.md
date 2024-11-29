# File DB Manager
* 설계 목적: 파일 형태로 테이블 데이터를 관리하는 데이터베이스 구축.
* 서브모듈
  * Database
    * 기능: 같은 어플리케이션을 구성하는 여러 테이블을 관리하는 모듈.
    * 함수 구성
      * create_table(name: str, row_class: Type, primary_keys: List[str] = None): 신규 테이블 생성.
      * show_tables(): Database 내 속한 모든 테이블 목록 조회. 
      * rename_table(old_name: str, new_name: str): 테이블 이름 명명.
      * load_table(name: str): 테이블 (MetaTable) 가져오기.
      * drop_table(name: str): 테이블 삭제.
  * Table
    * 기능: dict 포멧의 record로 구성된 데이터를 관리하는 모듈.
    * 데이터 구성: 테이블 데이터 (.parquet)로 구성.
    * 함수 구성
      * select(condition: dict) -> List[dict]: condition에 맞는 records 조회.
      * insert(records: List[dict]): records 삽입.
      * delete(condition: dict): condition에 맞는 records 삭제.
      * select_all() -> List[dict]: 모든 records 조회.
      * to_pandas() -> pd.DataFrame: pandas 데이터프레임으로 변형하여 리턴.
  * MetaTable
    * 기능: dataclass 타입의 record로 구성된 데이터를 관리하는 모듈.
    * 데이터 구성: 메타정보 (.meta.json)와 테이블 데이터 (.parquet)로 구성.
    * 함수 구성
      * select(condition: dict) -> List: condition에 맞는 records 조회.
      * insert(records: List): records 삽입.
      * delete(condition: dict): condition에 맞는 records 삭제.
      * select_all() -> List: 모든 records 조회.
      * insert_one(record): 단일 record 삽입.
