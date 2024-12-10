from dataclasses import dataclass
from typing import List
from . import AICallError, AICallSummary, AICallPrompt, AICallCompletion


@dataclass
class AICall:
    error: AICallError = None
    summary: AICallSummary = None
    prompts: List[AICallPrompt] = None
    completions: List[AICallCompletion] = None

    def _get_call_ids(self) -> list:
        call_ids = list()
        if self.error:
            call_ids.append(self.error.call_id)
        if self.summary:
            call_ids.append(self.summary.call_id)
        if self.prompts:
            call_ids.extend([p.call_id for p in self.prompts])
        if self.completions:
            call_ids.extend([c.call_id for c in self.completions])
        call_ids = list(set(call_ids))
        return call_ids

    def get_call_id(self) -> str:
        call_ids = self._get_call_ids()
        if len(call_ids) == 1:
            return call_ids[0]
        else:
            raise NotImplementedError()

    def __bool__(self):
        return len(self._get_call_ids()) == 1
