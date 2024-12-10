from dataclasses import dataclass
from typing import List


@dataclass
class AICallUsage:
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

        if 'usage' in kwargs:
            if "prompt_tokens" in kwargs['usage']:
                self.prompt_tokens = self._get_one_of_any(data=kwargs['usage'], keys=['prompt_tokens', 'input_tokens'])
            if "completion_tokens" in kwargs['usage']:
                self.completion_tokens = self._get_one_of_any(data=kwargs['usage'],
                                                              keys=['completion_tokens', 'output_tokens'])
            if "total_tokens" in kwargs['usage']:
                self.total_tokens = kwargs['usage']['total_tokens'] if 'total_tokens' in kwargs[
                    'usage'] else self.prompt_tokens + self.completion_tokens

    @staticmethod
    def _get_one_of_any(data: dict, keys: List[str]):
        for k in keys:
            if k in data.keys():
                return data[k]

        raise NotImplementedError()
