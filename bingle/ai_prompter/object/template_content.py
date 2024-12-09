from typing import Dict, List
from dataclasses import dataclass
from natsort import natsorted
from bingle.utils import BracketContentExtractor
from . import Content


@dataclass
class TemplateContent(Content):
    role: str = "text"
    content: str

    def get_varnames(self) -> List[str]:
        return BracketContentExtractor()(text=self.content, bracket_type="curly")

    def is_template(self) -> bool:
        return bool(self.get_varnames())

    def fill_vars(self, variables: Dict[str, str]):
        varnames = self.get_varnames()
        assert natsorted(varnames) == natsorted(variables)
        self.content = self.content.format(**variables)
