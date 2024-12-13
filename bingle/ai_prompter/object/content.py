from dataclasses import dataclass


@dataclass
class Content:
    type: str
    content: str

    def to_dict(self):
        return {'type': self.type, self.type: self.content}

    def copy(self):
        return Content(**{"role": self.type, "content": self.content})
