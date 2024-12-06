from bingle.file_db import FileDBManager, MetaTable
from bingle.ai_caller import AICallError, AICallSummary, AICallPrompt, AICallCompletion
from . import AICallDatabase


class AICallDBManager(FileDBManager):
    db_name: str = "gas"
    tb_name_summ: str = "ai_call_summary"
    tb_name_err: str = "ai_call_error"
    tb_name_prompt: str = "ai_call_prompt"
    tb_name_competion: str = "ai_call_completion"

    def __init__(self, base_dir: str = "./"):
        FileDBManager.__init__(self, base_dir=base_dir)

    def create(self, force: bool = False):
        if self._is_exist(name=self.db_name):
            if force:
                self._clear_folder(self.root_dir)
            else:
                print(FileExistsError("DB already exists."))

        if not self._is_exist(name=self.db_name):
            self.create_db(self.db_name)
            db = self.load_db(self.db_name)

            db.create_table(name=self.tb_name_err, row_class=AICallError, primary_keys=['call_id'])
            db.create_table(name=self.tb_name_summ, row_class=AICallSummary, primary_keys=['call_id'])
            db.create_table(name=self.tb_name_prompt, row_class=AICallPrompt,
                            primary_keys=['call_id', 'message_idx', 'content_idx'])
            db.create_table(name=self.tb_name_competion, row_class=AICallCompletion, primary_keys=['call_id', 'index'])

    def load_tables(self) -> AICallDatabase:
        return AICallDatabase(tb_error=self._load_table(name=self.tb_name_err),
                              tb_summary=self._load_table(name=self.tb_name_summ),
                              tb_prompt=self._load_table(name=self.tb_name_prompt),
                              tb_completion=self._load_table(name=self.tb_name_competion))

    def _load_table(self, name: str) -> MetaTable:
        db = self.load_db(self.db_name)
        tb = db.load_table(name=name)
        return tb
