from .data_formatter import DataclassToJsonschemaConverter
from .data_formatter import AnthropicToOpenAIDataConverter


class OpenAIDataFormatter(AnthropicToOpenAIDataConverter, DataclassToJsonschemaConverter):
    def __init__(self):
        AnthropicToOpenAIDataConverter.__init__(self)
        DataclassToJsonschemaConverter.__init__(self)
