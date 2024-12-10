from dataclasses import dataclass
from typing import Union


@dataclass
class AICallPrompt:
    call_id: str
    provider: str
    service: str
    model: str
    id: str
    message_idx: int
    content_idx: int
    role: str
    type: str
    content: str
    created: int

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.__annotations__:
                self.__dict__[k] = v

        if "content" in kwargs:
            self.type, self.content = self._extract_type_and_content(kwargs['content'])

    @staticmethod
    def _extract_type_and_content(content: Union[dict, str]) -> (str, str):
        if isinstance(content, dict):
            _type = content['type']
            _content = content[_type]
        elif isinstance(content, str):
            _type = 'text'
            _content = content
        else:
            raise NotImplementedError()
        return _type, _content
