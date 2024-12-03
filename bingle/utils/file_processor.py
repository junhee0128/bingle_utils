import os
import json
import pandas as pd


class FileProcessor:
    @staticmethod
    def is_exist(filepath: str) -> bool:
        return filepath is not None and os.path.exists(filepath)

    @staticmethod
    def load_txt(filepath: str, how: str = "whole") -> str:
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

    @staticmethod
    def save_txt(filepath: str, obj: str, mode: str = "w", encoding: str = "utf-8"):
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if encoding is not None:
            with open(filepath, mode, encoding=encoding) as f:
                f.write(obj)
        else:
            with open(filepath, mode) as f:
                f.write(obj)

    @staticmethod
    def load_json(filepath: str) -> dict:
        with open(filepath, 'r') as f:
            contents = json.load(f)
        return contents

    @staticmethod
    def save_json(filepath: str, obj: dict):
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(obj, f)

    @staticmethod
    def load_parquet(filepath: str) -> pd.DataFrame:
        return pd.read_parquet(filepath, engine="fastparquet")

    @staticmethod
    def save_parquet(obj: pd.DataFrame, filepath: str):
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        obj.to_parquet(filepath)

    @staticmethod
    def load_mp3(filepath: str):
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

    # filenamer의 배치 버전.
    def filenamer_batch(self, original_names: list, extension: str = "pdf") -> list:
        filenames = list()
        for name in original_names:
            filename = self.filenamer(original_name=name, extension=extension)
            filenames.append(filename)
        return filenames
