from dataclasses import dataclass
from bingle.file_db import FileDBManager


def test_file_db(db_dir: str):
    @dataclass
    class MyRow:
        key: str
        name: str
        age: int

    db_name = "my_database"
    tb_name = "my_table"
    tb_new_name = "my_new_table"

    dbm = FileDBManager(base_dir=db_dir)

    # DB 생성 테스트.
    dbm.show_dbs()
    dbm.create_db(name=db_name)

    try:
        dbm.create_db(name=db_name)
    except Exception as e:
        print(e)

    dbm.show_dbs()

    # 생성된 DB 조회.
    db = dbm.load_db(name=db_name)

    # 테이블 생성 및 명명 테스트.
    db.show_tables()
    db.create_table(name=tb_name, row_class=MyRow)
    db.show_tables()
    db.rename_table(old_name=tb_name, new_name=tb_new_name)
    db.show_tables()

    # 생성된 테이블 조회.
    tb = db.load_table(name=tb_new_name)

    # 데이터 삽입 및 조회 테스트.
    tb.insert([
        MyRow(key="1", name="Alice", age=30),
        MyRow(key="2", name="Bob", age=25),
        MyRow(key="1", name="Alice", age=30)
    ])

    rows = tb.select(condition={"name": "Alice"})
    print(rows)

    tb.insert_one({"key": "4", "name": "James", "age": 22})
    tb.insert_one(MyRow(key="5", name="John", age=24))

    rows = tb.select_all()
    print(rows)

    # DB 스냅샷 테스트.
    dbm.take_db_snapshot(name=db_name)

    # 데이터 삭제 테스트.
    tb.delete(condition={"age": 25})
    rows = tb.select_all()
    print(rows)

    # 테이블 삭제 테스트.
    db.drop_table(name=tb_new_name)
    db.show_tables()

    # 중복키 데이터 삽입 테스트.
    db.create_table(name=tb_new_name, row_class=MyRow, primary_keys=["key", "name"])
    tb = db.load_table(name=tb_new_name)
    tb.insert([MyRow(key="1", name="Alice", age=30)])
    try:
        tb.insert([MyRow(key="1", name="Alice", age=40)])
        db.drop_table(name=tb_new_name)
    except Exception as e:
        print(e)

    # DB 삭제 테스트.
    dbm.drop_db(name=db_name)

    # 휴지통 및 스냅샷 삭제 테스트.
    dbm.clear_trash()
    dbm.clear_snapshot()

    dbm.show_dbs()


if __name__ == "__main__":
    test_file_db(db_dir="../")
