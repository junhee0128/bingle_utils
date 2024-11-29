import os
import shutil
from datetime import datetime
from .submodules.database import Database


class FileDBManager:
    def __init__(self, base_dir: str):
        self.root_dir = os.path.join(os.path.abspath(base_dir), "file_db_data")
        self.snapshot_dir = os.path.join(self.root_dir, ".snapshot")
        self.trash_dir = os.path.join(self.root_dir, ".trash")
        self.db_dir = os.path.join(self.root_dir, "databases")

        # Ensure directories exist
        os.makedirs(self.snapshot_dir, exist_ok=True)
        os.makedirs(self.trash_dir, exist_ok=True)
        os.makedirs(self.db_dir, exist_ok=True)

    def create_db(self, name: str):
        """
        Creates a folder with the specified name under the self.db_dir directory.
        """
        if not self._is_exist(name=name):
            os.makedirs(self._get_db_path(name=name))
        else:
            raise FileExistsError(f"Database '{name}' already exists.")

    def load_db(self, name: str) -> Database:
        """
        Loads the database corresponding to the specified name.
        """
        if self._is_exist(self._get_db_path(name=name)):
            return Database(name=name, base_dir=self.db_dir, trash_dir=self.trash_dir)
        else:
            raise FileNotFoundError(f"Database '{name}' does not exist.")

    def drop_db(self, name: str):
        """
        Checks if a folder with the specified name exists under the self.db_dir directory.
        If it exists, moves it to the self.trash_dir directory and deletes the original folder.
        """
        if self._is_exist(name):
            shutil.move(self._get_db_path(name=name),
                        os.path.join(self.trash_dir, f"{name}_{self._get_datetime_now()}"))
        else:
            raise FileNotFoundError(f"Database '{name}' does not exist.")

    def show_dbs(self):
        """
        Prints all database names under the self.db_dir directory.
        """
        dbs = [name for name in os.listdir(self.db_dir) if os.path.isdir(os.path.join(self.db_dir, name))]
        if dbs:
            print(f"- DB list: {', '.join(dbs)}")
        else:
            print("- No database exists.")

    def take_db_snapshot(self, name: str):
        """
        Checks if a folder with the specified name exists under the self.db_dir directory.
        If it exists, copies it to the self.snapshot_dir directory.
        """
        if self._is_exist(name):
            snapshot_path = os.path.join(self.snapshot_dir, f"{name}_{self._get_datetime_now()}")
            shutil.copytree(self._get_db_path(name=name), snapshot_path)
        else:
            raise FileNotFoundError(f"Database '{name}' does not exist.")

    def clear_trash(self):
        self._clear_folder(self.trash_dir)

    def clear_snapshot(self):
        self._clear_folder(self.snapshot_dir)

    @staticmethod
    def _clear_folder(path: str):
        if os.path.exists(path):

            # 삭제된 파일과 폴더 개수를 세기 위한 함수
            folder_count, file_count = 0, 0
            for root, dirs, files in os.walk(path):
                folder_count += len(dirs)
                file_count += len(files)

            shutil.rmtree(path)
            os.makedirs(path)

            print(f"- Deleted {folder_count} folders and {file_count} files from '{path}'.")

        else:
            raise FileNotFoundError(f"The directory '{path}' does not exist.")

    def _get_db_path(self, name: str):
        return os.path.join(self.db_dir, name)

    def _is_exist(self, name: str) -> bool:
        """
        Checks whether a folder with the specified name exists under the self.db_dir directory.
        """
        db_path = self._get_db_path(name=name)
        return os.path.exists(db_path) and os.path.isdir(db_path)

    @staticmethod
    def _get_datetime_now(expression: str = "%y%m%d_%H%M%S_%f"):
        return datetime.now().strftime(expression)
