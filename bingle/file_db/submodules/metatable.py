from typing import List
from dataclasses import fields, make_dataclass
from bingle.utils.file_processor import FileProcessor
from .table import Table


class MetaTable(Table):
    def __init__(self, table_path: str, meta_path: str):
        """
        Initialize the MetaTable.
        """
        self.table_path = table_path
        self.meta_path = meta_path

        self.metadata = FileProcessor.load_file(filepath=self.meta_path)
        super().__init__(file_path=self.table_path, primary_keys=self.metadata["primary_keys"])
        self.row_class = self._generate_row_class()

    def select(self, condition: dict) -> List:
        """
        Retrieve records matching a condition as dataclass instances.
        """
        dict_records = super().select(condition)
        return [self._dict_to_dataclass(record) for record in dict_records]

    def insert(self, records: List):
        """
        Insert dataclass instances or dictionaries into the table.
        Automatically converts dictionaries to dataclass instances.
        """
        dataclass_records = [
            self._dict_to_dataclass(record) if isinstance(record, dict) else record
            for record in records
        ]
        dict_records = [self._dataclass_to_dict(record) for record in dataclass_records]
        super().insert(dict_records)

    def delete(self, condition: dict):
        super().delete(condition)

    def select_all(self) -> List:
        """
        Retrieve all records as dataclass instances.
        """
        dict_records = super().select_all()
        return [self._dict_to_dataclass(record) for record in dict_records]

    def insert_one(self, record):
        self.insert(records=[record])

    def _generate_row_class(self):
        """
        Generate a dataclass dynamically based on the metadata.
        """
        if not self.metadata:
            raise ValueError("Metadata not found or invalid. Cannot generate row_class.")

        fields = [
            (field["name"], eval(field["type"])) for field in self.metadata.get("fields", [])
        ]
        return make_dataclass("Row", fields)

    def _dict_to_dataclass(self, record: dict):
        """
        Convert a dictionary to a dataclass instance.
        """
        return self.row_class(**record)

    def _dataclass_to_dict(self, instance):
        """
        Convert a dataclass instance to a dictionary.
        """
        return {field.name: getattr(instance, field.name) for field in fields(self.row_class)}
