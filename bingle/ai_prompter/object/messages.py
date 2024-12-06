from dataclasses import dataclass
from typing import List
from . import Prompt


@dataclass
class Messages:
    prompts: List[Prompt]

    def to_dict(self):
        return [p.to_dict() for p in self.prompts]

    def append(self, prompt: Prompt):
        self.prompts.append(prompt)

    def pop(self, index: int = -1):
        return self.prompts.pop(index)
