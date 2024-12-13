## QuickStart

### OpenAIDataFormatter example.

```python
from dataclasses import dataclass
from typing import Literal
from bingle.ai_caller import OpenAIDataFormatter


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

```
