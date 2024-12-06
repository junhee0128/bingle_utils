from dataclasses import dataclass
from typing import List, Union


@dataclass
class AICallCompletion:
    call_id: str
    provider: str
    service: str
    model: str
    id: str
    index: int
    role: str
    type: str
    content: str
    message: str
    finish_reason: str
    created: int

    def __init__(self, choice: dict = None, **kwargs):
        for k, v in kwargs.items():
            if k in self.__annotations__:
                self.__dict__[k] = v

        if choice is not None:
            self.index = choice['index']
            self.role = choice['message']['role']
            self.message = str(choice['message'])
            self.type, self.content = self._extract_type_and_content(choice['message']['content'])
            self.finish_reason = self._get_one_of_any(data=choice, keys=['finish_reason', 'stop_reason'])

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

    @staticmethod
    def _get_one_of_any(data: dict, keys: List[str]):
        for k in keys:
            if k in data.keys():
                return data[k]

        raise NotImplementedError()
