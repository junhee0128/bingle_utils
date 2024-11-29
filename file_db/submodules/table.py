import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import os
from typing import List


class Table:
    def __init__(self, file_path: str, primary_keys: List[str]):
        """
        Initialize the Table.
        :param file_path: Path to the Parquet file.
        """
        self.file_path = file_path
        assert isinstance(primary_keys, list)
        self.primary_keys = primary_keys
        self.table = self._load_table()

    def select(self, condition: dict) -> List[dict]:
        """Select records matching the condition."""
        df = self.table.to_pandas()
        for col, value in condition.items():
            df = df[df[col] == value]
        return df.to_dict(orient='records')

    def insert(self, records: List[dict]):
        """Insert new records."""
        concatenated_df = pd.concat([pd.DataFrame(records), self.table.to_pandas()], ignore_index=True)
        if len(concatenated_df[self.primary_keys]) != len(concatenated_df[self.primary_keys].drop_duplicates()):
            raise KeyError(f"Some data have duplicate keys.")

        self.table = pa.Table.from_pandas(concatenated_df)

        self._save_table()

    def delete(self, condition: dict):
        """Delete records matching the condition."""
        df = self.table.to_pandas()
        for col, value in condition.items():
            df = df[df[col] != value]
        self.table = pa.Table.from_pandas(df)
        self._save_table()

    def select_all(self) -> List[dict]:
        """Select all records."""
        return self.table.to_pandas().to_dict(orient='records')

    def to_pandas(self) -> pd.DataFrame:
        """Convert the table to a Pandas DataFrame."""
        return self.table.to_pandas()

    def _load_table(self) -> pa.Table:
        """Load the Parquet file into a PyArrow Table. Return None if the file doesn't exist."""
        if os.path.exists(self.file_path):
            return pq.read_table(self.file_path)
        else:
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")

    def _save_table(self):
        """Save the PyArrow Table to the Parquet file."""
        if self.table is not None:
            pq.write_table(self.table, self.file_path)
