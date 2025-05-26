import os
import json
import csv
import pickle
import logging
import pandas as pd
from typing import Any, Union, Dict, List
from pathlib import Path
import xml.etree.ElementTree as ET
from docx import Document

PathLike = Union[str, Path]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FileProcessor:
    @staticmethod
    def is_exist(filepath: PathLike) -> bool:
        return filepath is not None and os.path.exists(filepath)

    @staticmethod
    def load_file(filepath: PathLike) -> Union[str, dict, pd.DataFrame, None]:
        try:
            if not os.path.exists(filepath):
                print(f"File does not exist: {filepath}")
                return None

            _, file_ext = os.path.splitext(filepath)

            for encoding in ["utf-8", "cp949", "utf-16", "unicode"]:
                try:
                    if file_ext in (".txt", ".log", ".md"):
                        with open(filepath, "r", encoding=encoding) as f:
                            return f.read()
                    elif file_ext == ".json":
                        with open(filepath, "r", encoding=encoding) as f:
                            return json.load(f)
                            # return json.dumps(json.load(f), indent=4, ensure_ascii=False)
                    elif file_ext == ".pkl":
                        with open(filepath, "rb") as f:
                            return pickle.load(f)
                    elif file_ext == ".xml":
                        tree = ET.parse(filepath)
                        return ET.tostring(tree.getroot(), encoding="unicode")
                    elif file_ext in (".csv", ".tsv"):
                        delimiter = "," if file_ext == ".csv" else "\t"
                        with open(filepath, "r", encoding=encoding) as f:
                            reader = csv.reader(f, delimiter=delimiter)
                            return "\n".join([delimiter.join(row) for row in reader])
                    else:
                        pass
                except Exception as e:
                    pass

            if file_ext in (".docx", ".doc"):
                return "\n".join([p.text for p in Document(filepath).paragraphs])
            elif file_ext == ".parquet":
                return pd.read_parquet(filepath, engine="fastparquet")
            else:
                raise Exception(f"Unsupported file format: {file_ext}")
        except Exception as e:
            raise e

    @staticmethod
    def save_txt(filepath: PathLike, obj: str, mode: str = "w", encoding: str = "utf-8"):
        if os.path.dirname(filepath) and not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if encoding is not None:
            with open(filepath, mode, encoding=encoding) as f:
                f.write(obj)
        else:
            with open(filepath, mode) as f:
                f.write(obj)

    @staticmethod
    def save_json(filepath: PathLike, obj: dict, mode: str = "w", encoding: str = 'utf-8'):
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, mode, encoding=encoding) as f:
            json.dump(obj, f, ensure_ascii=False)

    @staticmethod
    def save_pickle(filepath: PathLike, data: Any):
        with open(filepath, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def save_parquet(filepath: PathLike, obj: pd.DataFrame):
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        obj.to_parquet(filepath)

    @staticmethod
    def load_mp3(filepath: PathLike):
        with open(filepath, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        return audio_bytes

    @staticmethod
    def clear_files(dir: str, extension: str):
        if os.path.exists(dir):
            files_to_remove = [os.path.join(dir, e) for e in os.listdir(dir) if
                               os.path.splitext(e)[-1] == f".{extension}"]
            for fpath in files_to_remove:
                os.remove(fpath)

    # original_name 에서 알파벳 캐릭터만 소문자로 남기고 나머지는 모두 _로 변환함. 단, _가 연속으로 있을 경우 한 개만 남김.
    @staticmethod
    def filenamer(original_name: list, extension: str) -> str:
        filename = "".join([char if char.isalpha() else "_" for char in original_name]).lower()
        while "__" in filename:
            filename = filename.replace("__", "_")
        filename = f"{filename}.{extension}"
        return filename

    @staticmethod
    def load_json(filepath: PathLike) -> dict:
        logger.warning("This method will be deprecated.")
        with open(filepath, 'r') as f:
            contents = json.load(f)
        return contents

    @staticmethod
    def load_pickle(filepath: PathLike):
        logger.warning("This method will be deprecated.")
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        return data

    @staticmethod
    def load_parquet(filepath: PathLike) -> pd.DataFrame:
        logger.warning("This method will be deprecated.")
        return pd.read_parquet(filepath, engine="fastparquet")

    @staticmethod
    def load_txt(filepath: PathLike, how: str = "whole") -> str:
        logger.warning("This method will be deprecated.")
        content = None
        for encoding in ["cp949", "utf-16", "utf-8"]:
            try:
                with open(filepath, "r", encoding=encoding) as f:
                    if how == "whole":
                        content = f.read()
                        break
                    elif how == "linebyline":
                        content_list = f.readlines()
                        if isinstance(content_list, list):
                            content = "\n".join(content_list)
                        break
                    else:
                        raise NotImplementedError
            except Exception as e:
                pass

        if content is None:
            raise FileNotFoundError(f"Failed to read '{filepath}'.")

        return content
