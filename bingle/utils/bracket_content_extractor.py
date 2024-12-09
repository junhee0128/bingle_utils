import re
from typing import Dict, List, Literal


class BracketContentExtractor:
    BRACKET_TYPE: List[str] = ["square", "round", "curly"]
    REGEX: Dict[str, Dict[str, str]] = {"nested": {"square": r'\[(.*?)\]',  # 대괄호 []
                                                   "round": r'\((.*?)\)',  # 소괄호 ()
                                                   "curly": r'\{(.*?)\}'  # 중괄호 {}
                                                   },
                                        "non_nested": {"square": r'\[([^\[\]]*?)\]',  # 중첩 허용하지 않는 대괄호
                                                       "round": r'\(([^\(\)]*?)\)',  # 중첩 허용하지 않는 소괄호
                                                       "curly": r'\{([^{}]*?)\}'  # 중첩 허용하지 않는 중괄호
                                                       }
                                        }

    def __call__(self, text: str, bracket_type: Literal["square", "round", "curly"], allow_nested: bool = False) -> \
    List[str]:
        return self._extract(text=text, bracket_type=bracket_type, allow_nested=allow_nested)

    def extract_square(self, text: str, allow_nested: bool = False) -> List[str]:
        """Extract content inside square brackets []"""
        return self._extract(text=text, bracket_type="square", allow_nested=allow_nested)

    def extract_round(self, text: str, allow_nested: bool = False) -> List[str]:
        """Extract content inside round brackets ()"""
        return self._extract(text=text, bracket_type="round", allow_nested=allow_nested)

    def extract_curly(self, text: str, allow_nested: bool = False) -> List[str]:
        """Extract content inside curly braces {}"""
        return self._extract(text=text, bracket_type="curly", allow_nested=allow_nested)

    def _extract(self, text: str, bracket_type: str, allow_nested: bool) -> List[str]:
        """Extract content inside brackets"""
        regex = self.REGEX["nested" if allow_nested else "non_nested"][bracket_type]
        return re.findall(regex, text)
