from .data_formatter import DataclassToJsonschemaConverter
from .data_formatter import AnthropicToOpenAIDataConverter


class OpenAIDataFormatter(AnthropicToOpenAIDataConverter, DataclassToJsonschemaConverter):
    def __init__(self):
        AnthropicToOpenAIDataConverter.__init__(self)
        DataclassToJsonschemaConverter.__init__(self)


if __name__ == "__main__":
    from dataclasses import dataclass
    from typing import Literal


    @dataclass
    class Step:
        explanation: str
        output: str
        format: Literal["format_a", "format_b"]


    @dataclass
    class MathResponse:
        steps: list[Step]
        final_answer: str


    data_formatter = OpenAIDataFormatter()
    json_schema = data_formatter.to_json_schema(dataclass=MathResponse)

    print(json_schema)
    print("done")
