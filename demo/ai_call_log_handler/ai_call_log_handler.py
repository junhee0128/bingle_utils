import pandas as pd
from datetime import datetime
from bingle.ai_caller import AICall, AICallSummary, AICallUsage, AICallPrompt, AICallCompletion
from . import AICallDBManager


class AICallLogHandler(AICallDBManager):
    def __init__(self, base_dir: str):
        AICallDBManager.__init__(self, base_dir=base_dir)
        self.create(force=False)

    def log_to_db(self, call_summary: AICallSummary):
        ai_call = AICall()
        ai_call.reset_from_summary(summary=call_summary)

        call_db = self.load_tables()

        if ai_call.summary is not None:
            call_db.tb_summary.insert(records=[ai_call.summary])
        if ai_call.usage is not None:
            call_db.tb_usage.insert(records=[ai_call.usage])
        if ai_call.prompts is not None:
            call_db.tb_prompt.insert(records=ai_call.prompts)
        if ai_call.completions is not None:
            call_db.tb_completion.insert(records=ai_call.completions)

        print(f"AI call transaction is logged with the ID of '{call_summary.call_id}'.")

    def load_call(self, call_id: str) -> AICall:
        call_db = self.load_tables()
        summaries = call_db.tb_summary.select(condition={'call_id': call_id})
        usages = call_db.tb_usage.select(condition={'call_id': call_id})
        prompts = call_db.tb_prompt.select(condition={'call_id': call_id})
        completions = call_db.tb_completion.select(condition={'call_id': call_id})

        assert len(usages) <= 1 and len(summaries) <= 1

        summary = AICallSummary(**summaries[0].__dict__)
        usage = AICallUsage(**usages[0].__dict__) if usages else None
        prompts = [AICallPrompt(**_args) for _args in [p.__dict__ for p in prompts]]
        completions = [AICallCompletion(**_args) for _args in [c.__dict__ for c in completions]]

        return AICall(summary=summary, usage=usage, prompts=prompts, completions=completions)

    def load_summary_table(self) -> pd.DataFrame:
        df_summary = self._load_table(name=self.tb_name_summary).to_pandas()
        df_summary['created'] = df_summary['created'].apply(
            lambda ts: datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
        )
        return df_summary

    @staticmethod
    def to_dict(ai_call: AICall) -> dict:
        d_call = {k: v for k, v in ai_call.summary.to_dict().items() if v is not None}
        d_call['usage'] = {k: v for k, v in ai_call.usage.__dict__.items() if k not in d_call or v != d_call[k]}
        d_call['prompts'] = [{k: v for k, v in p.__dict__.items() if k not in d_call or v != d_call[k]} for p in
                             ai_call.prompts]
        d_call['completions'] = [{k: v for k, v in c.__dict__.items() if k not in d_call or v != d_call[k]} for c in
                                 ai_call.completions]
        return d_call
