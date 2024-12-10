from dataclasses import dataclass
from typing import List


@dataclass
class AICallSummary:
    call_id: str
    provider: str
    service: str
    model: str
    id: str
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    created: int

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.__annotations__:
                self.__dict__[k] = v

        if 'prompt_tokens' not in kwargs.keys():
            self.prompt_tokens = self._get_one_of_any(data=kwargs['usage'], keys=['prompt_tokens', 'input_tokens'])
        if 'completion_tokens' not in kwargs.keys():
            self.completion_tokens = self._get_one_of_any(data=kwargs['usage'],
                                                          keys=['completion_tokens', 'output_tokens'])
        if 'total_tokens' not in kwargs.keys():
            self.total_tokens = kwargs['usage']['total_tokens'] if 'total_tokens' in kwargs[
                'usage'] else self.prompt_tokens + self.completion_tokens

    @staticmethod
    def _get_one_of_any(data: dict, keys: List[str]):
        for k in keys:
            if k in data.keys():
                return data[k]

        raise NotImplementedError()
