from dataclasses import dataclass
from typing import List, Iterator
from collections import Counter
from . import Prompt


@dataclass
class Messages:
    prompts: List[Prompt]

    def __iter__(self) -> Iterator[Prompt]:
        return iter(self.prompts)

    def to_dict(self):
        return [p.to_dict() for p in self.prompts]

    def append(self, prompt: Prompt):
        self.prompts.append(prompt)

    def pop(self, index: int = -1):
        return self.prompts.pop(index)

    def count_roles(self) -> Counter:
        return Counter([p.role for p in self.prompts])
