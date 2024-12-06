import re


class BracketContentExtractor:
    def __init__(self):
        self.patterns = {
            "square": r'\[(.*?)\]',  # 대괄호 []
            "round": r'\((.*?)\)',  # 소괄호 ()
            "curly": r'\{(.*?)\}',  # 중괄호 {}
            "non_nested_square": r'\[([^\[\]]*?)\]',  # 중첩 허용하지 않는 대괄호
            "non_nested_round": r'\(([^\(\)]*?)\)',  # 중첩 허용하지 않는 소괄호
            "non_nested_curly": r'\{([^{}]*?)\}'  # 중첩 허용하지 않는 중괄호
        }

    def extract_square(self, text: str, allow_nested: bool = False):
        """Extract content inside square brackets []"""
        return self._extract(text=text, bracket_type="square", allow_nested=allow_nested)

    def extract_round(self, text: str, allow_nested: bool = False):
        """Extract content inside round brackets ()"""
        return self._extract(text=text, bracket_type="round", allow_nested=allow_nested)

    def extract_curly(self, text: str, allow_nested: bool = False):
        """Extract content inside curly braces {}"""
        return self._extract(text=text, bracket_type="curly", allow_nested=allow_nested)

    def _extract(self, text: str, bracket_type: str, allow_nested: bool):
        """Extract content inside brackets"""
        if allow_nested:
            return re.findall(self.patterns[bracket_type], text)
        else:
            return re.findall(self.patterns[f"non_nested_{bracket_type}"], text)
