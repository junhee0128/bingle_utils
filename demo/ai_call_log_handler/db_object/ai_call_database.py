from dataclasses import dataclass
from bingle.file_db import MetaTable


@dataclass
class AICallDatabase:
    tb_summary: MetaTable
    tb_usage: MetaTable
    tb_prompt: MetaTable
    tb_completion: MetaTable
