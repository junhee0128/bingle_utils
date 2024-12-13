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

    def get_role_prompts(self, roles: List[str] = None, exclude_roles: List[str] = None) -> List[Prompt]:
        prompts = self.prompts
        if roles is not None:
            prompts = [p for p in prompts if p.role in roles]
        if exclude_roles is not None:
            prompts = [p for p in prompts if p.role not in exclude_roles]
        return prompts

    def copy(self):
        return Messages(prompts=self.prompts)
