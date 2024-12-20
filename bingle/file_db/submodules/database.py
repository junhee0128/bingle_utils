import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import os
import shutil
from typing import Type, List
from dataclasses import fields
from datetime import datetime
from . import MetaTable
from bingle.utils import FileProcessor


class Database:
    def __init__(self, name: str, base_dir: str = "./", trash_dir: str = None):
        """
        Initialize the database with a directory name.
        """
        self.name = name
        self.db_path = os.path.join(base_dir, self.name)
        self.trash_dir = trash_dir

    def create_table(self, name: str, row_class: Type, primary_keys: List[str] = None):
        """
        Create a new table with the specified schema.
        """
        if self._is_exist(name):
            FileExistsError(f"Table '{name}' already exists.")
        else:
            schema = self._generate_schema(row_class)
            empty_df = pd.DataFrame(columns=schema.names)
            pa_table = pa.Table.from_pandas(df=empty_df, schema=schema)
            pq.write_table(pa_table, self._get_table_path(name=name))
            metadata = self._generate_metadata(row_class=row_class, primary_keys=primary_keys)
            FileProcessor.save_json(filepath=self._get_table_meta_path(name=name), obj=metadata)
            print(f"Table '{name}' created successfully.")

    def show_tables(self):
        """
        Prints all table names under the self.db_path directory.
        """
        tables = [file.replace('.parquet', '') for file in os.listdir(self.db_path) if file.endswith('.parquet')]
        if tables:
            print(f"- Table list: {', '.join(tables)}")
        else:
            print("- No table exists.")

    def rename_table(self, old_name: str, new_name: str):
        """
        Rename an existing table.
        """
        old_data_path = self._get_table_path(name=old_name)
        new_data_path = self._get_table_path(name=new_name)
        old_meta_path = self._get_table_meta_path(name=old_name)
        new_meta_path = self._get_table_meta_path(name=new_name)
        if self._is_exist(old_name):
            if not self._is_exist(new_name):
                os.rename(old_data_path, new_data_path)
                os.rename(old_meta_path, new_meta_path)
                print(f"Table '{old_name}' renamed to '{new_name}'.")
            else:
                FileExistsError(f"Table '{new_name} already exists.'")
        else:
            FileNotFoundError(f"Table '{old_name}' does not exist.")

    def load_table(self, name: str) -> MetaTable:
        """
        Load a table and return a Table instance.
        """
        table_path = self._get_table_path(name=name)
        meta_path = self._get_table_meta_path(name=name)
        if self._is_exist(name=name):
            return MetaTable(table_path=table_path, meta_path=meta_path)
        else:
            raise FileNotFoundError(f"Table '{name}' does not exist.")

    def drop_table(self, name: str):
        """
        Delete a table file.
        """
        if self._is_exist(name=name):
            table_path = self._get_table_path(name)
            meta_path = self._get_table_meta_path(name)
            if self.trash_dir is None:
                os.remove(table_path)
                print(f"Table '{name}' dropped successfully.")
            else:
                trash_path = os.path.join(self.trash_dir, f"{self.name}_{self._get_datetime_now()}")
                os.makedirs(trash_path)
                shutil.move(table_path, trash_path)
                shutil.move(meta_path, trash_path)
        else:
            FileNotFoundError(f"Table '{name}' does not exist.")

    @staticmethod
    def _generate_schema(row_class: Type) -> pa.Schema:
        """
        Generate a PyArrow schema based on the dataclass fields.
        """
        field_types = {
            int: pa.int64(),
            float: pa.float64(),
            str: pa.string(),
            bool: pa.bool_()
        }
        schema_fields = [
            (f.name, field_types.get(f.type, pa.string()))  # Default to string if type is not in field_types
            for f in fields(row_class)
        ]
        return pa.schema(schema_fields)

    def _get_table_path(self, name: str) -> str:
        """
        Get the full path for a table file.
        """
        return os.path.join(self.db_path, f"{name}.parquet")

    def _get_table_meta_path(self, name: str) -> str:
        """
        Get the full path for a table meta file.
        """
        return os.path.join(self.db_path, f"{name}.meta.json")

    @staticmethod
    def _generate_metadata(row_class: Type, primary_keys: List[str]):
        if primary_keys:
            row_variables = [f.name for f in fields(row_class)]
            for pk in primary_keys:
                if pk not in row_variables:
                    raise KeyError(f"{pk} is not a variable of {row_class.__name__}")

        metadata = {
            "primary_keys": primary_keys if primary_keys else list(),
            "fields": [
                {"name": f.name, "type": f.type.__name__} for f in fields(row_class)
            ]
        }
        return metadata

    def _is_exist(self, name: str) -> bool:
        return os.path.exists(self._get_table_path(name=name)) and os.path.exists(self._get_table_meta_path(name=name))

    @staticmethod
    def _get_datetime_now(expression: str = "%y%m%d_%H%M%S_%f"):
        return datetime.now().strftime(expression)
