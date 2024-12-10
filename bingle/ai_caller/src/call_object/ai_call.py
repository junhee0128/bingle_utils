from dataclasses import dataclass
from typing import List
from .ai_call_summary import AICallSummary
from .ai_call_usage import AICallUsage
from .ai_call_prompt import AICallPrompt
from .ai_call_completion import AICallCompletion


@dataclass
class AICall:
    summary: AICallSummary = None
    usage: AICallUsage = None
    prompts: List[AICallPrompt] = None
    completions: List[AICallCompletion] = None

    def reset_from_summary(self, summary: AICallSummary):
        self.summary = AICallSummary(**summary.to_dict())
        if summary.success:
            usage_args = self._get_usage_args(summary=summary)
            p_args_list = self._get_prompt_args_list(summary=summary)
            c_args_list = self._get_completion_args_list(summary=summary)

            self.usage = AICallUsage(**usage_args)
            self.prompts = [AICallPrompt(**_args) for _args in p_args_list]
            self.completions = [AICallCompletion(**_args) for _args in c_args_list]

    @staticmethod
    def _get_usage_args(summary: AICallSummary) -> dict:
        usage_args = summary.to_dict().copy()
        usage_args.update(summary.payload)
        usage_args.update(summary.response)
        return usage_args

    @staticmethod
    def _get_completion_args_list(summary: AICallSummary) -> List[dict]:
        c_args_list = list()
        for choice in summary.response['choices']:
            c_args = summary.to_dict()
            c_args.update(summary.response.copy())
            c_args.update({'choice': choice})
            c_args_list.append(c_args)
        return c_args_list

    @staticmethod
    def _get_prompt_args_list(summary: AICallSummary) -> List[dict]:
        _meta_args = summary.to_dict()

        p_args_list = list()
        for msg_idx, msg in enumerate(summary.payload['messages']):
            if isinstance(msg['content'], list):
                for c_idx, c in enumerate(msg['content']):
                    p_args = _meta_args.copy()
                    p_args.update(summary.payload.copy())
                    p_args.update({'message_idx': msg_idx, 'content_idx': c_idx, 'role': msg['role'], 'content': c})
                    p_args_list.append(p_args)
            elif isinstance(msg['content'], str):
                p_args = _meta_args.copy()
                p_args.update(summary.payload.copy())
                p_args.update(
                    {'message_idx': msg_idx, 'content_idx': 0, 'role': msg['role'], 'content': msg['content']})
                p_args_list.append(p_args)
            else:
                raise NotImplementedError()
        return p_args_list
