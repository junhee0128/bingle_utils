from bingle.utils import BracketContentExtractor


def test_bracket_content_extractor():
    BracketContentExtractor()
    text = "Here are [square brackets], (round brackets), {curly braces}, and {nested {example}}."
    extractor = BracketContentExtractor()

    print("- Square brackets:", extractor.extract_square(text))
    print("- Round brackets:", extractor.extract_round(text))
    print("- Curly braces:", extractor.extract_curly(text))

    print("- Square brackets (nested allowed):", extractor.extract_square(text, allow_nested=True))
    print("- Round brackets (nested allowed):", extractor.extract_round(text, allow_nested=True))
    print("- Curly braces (nested allowed):", extractor.extract_curly(text, allow_nested=True))


if __name__ == "__main__":
    test_bracket_content_extractor()
