from typing import List, Union
from . import Content


class Prompt:
    def __init__(self, role: str, content: Union[List[dict], Content, str], **kwargs):
        self.role = role
        if isinstance(content, List):
            self.content = [Content(type=c['type'], content=c[c['type']]) for c in content]
        elif isinstance(content, Content):
            self.content = [content]
        elif isinstance(content, str):
            self.content = [Content(type='text', content=content)]
        else:
            raise NotImplementedError()

    def to_dict(self):
        return {'role': self.role, 'content': [c.to_dict() for c in self.content]}
