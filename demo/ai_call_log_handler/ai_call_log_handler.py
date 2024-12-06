from bingle.ai_caller import AICallObjectHandler, AICall
from . import AICallDBManager


class AICallLogHandler(AICallDBManager, AICallObjectHandler):
    def __init__(self, base_dir: str):
        AICallDBManager.__init__(self, base_dir=base_dir)
        AICallObjectHandler.__init__(self)
        self.create(force=False)

    def log_to_db(self, provider: str, service: str, payload: dict, response: dict):
        ai_call = self.convert_payload_and_response_into_ai_call_objects(provider=provider, service=service,
                                                                         payload=payload, response=response)

        call_db = self.load_tables()

        if ai_call.error is not None:
            call_db.tb_error.insert(records=[ai_call.error])
        if ai_call.summary is not None:
            call_db.tb_summary.insert(records=[ai_call.summary])
        if ai_call.prompts is not None:
            call_db.tb_prompt.insert(records=ai_call.prompts)
        if ai_call.completions is not None:
            call_db.tb_completion.insert(records=ai_call.completions)

        print(f"AI call transaction is logged with the ID of '{ai_call.get_call_id()}'.")

    def load_call(self, call_id: str) -> AICall:
        call_db = self.load_tables()
        errors = call_db.tb_error.select(condition={'call_id': call_id})
        summaries = call_db.tb_summary.select(condition={'call_id': call_id})
        prompts = call_db.tb_prompt.select(condition={'call_id': call_id})
        completions = call_db.tb_completion.select(condition={'call_id': call_id})

        assert len(errors) <= 1 and len(summaries) <= 1

        ai_call = self.convert_args_into_call_objects(err_args=errors[0].__dict__ if errors else None,
                                                      summ_args=summaries[0].__dict__ if summaries else None,
                                                      prompt_args_list=[p.__dict__ for p in
                                                                        prompts] if prompts else None,
                                                      completion_args_list=[c.__dict__ for c in
                                                                            completions] if completions else None)

        return ai_call
