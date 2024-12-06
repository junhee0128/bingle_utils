from bingle.ai_caller import AICall, AICallError, AICallSummary, AICallPrompt, AICallCompletion, AICallDataFormatter
from datetime import datetime
from uuid import uuid4
from typing import List


class AICallObjectHandler(AICallDataFormatter):
    def __init__(self):
        AICallDataFormatter.__init__(self)

    def convert_payload_and_response_into_ai_call_objects(self,
                                                          provider: str, service: str,
                                                          payload: dict, response: dict) -> AICall:

        err_args, summ_args, p_args_list, c_args_list = None, None, None, None

        meta_args = self._get_meta_args(call_id=self._get_call_id(), provider=provider, service=service)

        if isinstance(response, str):
            err_args = self._get_error_args(meta_args=meta_args, response=response)
        elif isinstance(response, dict):
            summ_args = self._get_summary_args(meta_args=meta_args, payload=payload, response=response)

            if provider == 'anthropic':
                payload = self.convert_anthropic_payload(payload=payload)

            p_args_list = self._get_prompt_args_list(meta_args=meta_args, payload=payload, response=response)

            if provider == 'anthropic':
                response = self.convert_anthropic_response(response=response)

            c_args_list = self._get_completion_args_list(meta_args=meta_args, response=response)
        else:
            raise NotImplementedError()

        ai_call = self.convert_args_into_call_objects(err_args=err_args, summ_args=summ_args,
                                                      prompt_args_list=p_args_list, completion_args_list=c_args_list)

        return ai_call

    @staticmethod
    def convert_args_into_call_objects(err_args: dict, summ_args: dict,
                                       prompt_args_list: List[dict], completion_args_list: List[dict]) -> AICall:
        error = AICallError(**err_args) if err_args else None
        summary = AICallSummary(**summ_args) if summ_args else None
        prompts = [AICallPrompt(**_args) for _args in prompt_args_list] if prompt_args_list else None
        completions = [AICallCompletion(**_args) for _args in completion_args_list] if completion_args_list else None

        return AICall(error=error, summary=summary, prompts=prompts, completions=completions)

    @staticmethod
    def _get_call_id():
        return str(uuid4())

    @staticmethod
    def _get_meta_args(call_id: str, provider: str, service: str) -> dict:
        args = {'call_id': call_id, 'provider': provider, 'service': service,
                'id': f'{provider}_{str(uuid4())}',
                'created': int(datetime.now().timestamp())}
        return args

    @staticmethod
    def _get_error_args(meta_args: dict, response: str) -> dict:
        error_args = meta_args.copy()
        error_args.update({'message': response})
        return error_args

    @staticmethod
    def _get_summary_args(meta_args: dict, payload: dict, response: dict) -> dict:
        summary_args = meta_args.copy()
        summary_args.update(payload)
        summary_args.update(response)
        return summary_args

    @staticmethod
    def _get_completion_args_list(meta_args: dict, response: dict) -> List[dict]:
        c_args_list = list()
        for choice in response['choices']:
            c_args = meta_args.copy()
            c_args.update(response.copy())
            c_args.update({'choice': choice})
            c_args_list.append(c_args)
        return c_args_list

    @staticmethod
    def _get_prompt_args_list(meta_args: dict, payload: dict, response: dict) -> List[dict]:
        _meta_args = meta_args.copy()
        _meta_args['model'] = response['model']

        p_args_list = list()
        for msg_idx, msg in enumerate(payload['messages']):
            if isinstance(msg['content'], list):
                for c_idx, c in enumerate(msg['content']):
                    p_args = _meta_args.copy()
                    p_args.update(payload.copy())
                    p_args.update({'message_idx': msg_idx, 'content_idx': c_idx, 'role': msg['role'], 'content': c})
                    p_args_list.append(p_args)
            elif isinstance(msg['content'], str):
                p_args = _meta_args.copy()
                p_args.update(payload.copy())
                p_args.update(
                    {'message_idx': msg_idx, 'content_idx': 0, 'role': msg['role'], 'content': msg['content']})
                p_args_list.append(p_args)
            else:
                raise NotImplementedError()
        return p_args_list
