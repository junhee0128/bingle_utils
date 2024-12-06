# Utils

## File Processor

* 설계 목적: 자주 사용하는 유틸리티 모음.
* 서브모듈
    * FileProcessor
        * 목적: 자주 사용하는 파일 처리 함수 모음.
        * 함수 구성
            * load_json(filepath: str) -> dict: json 파일 읽기.
            * save_json(filepath: str, obj: dict): json 파일 쓰기.

## API Client

## Port Killer

### Quickstart

```python
from bingle.utils import PortKiller

port = 5000  # designates the port to kill.
p_killer = PortKiller()  # declares PortKiller instance.
if p_killer.is_alive(port):  # checks if the port is occupied.
    p_killer.kill(port)  # kills the port.
```

## Bracket Content Extractor

### Quickstart
```python
from bingle.utils import BracketContentExtractor

text = "Here are [square brackets], (round brackets), {curly braces}, and {nested {example}}."

extractor = BracketContentExtractor()
```

You can extract the enclosed text with brackets, as follows:
1) square brackets
```python
extractor.extract_square(text=text)
```
```python
['square brackets']
```

2) round brackets
```python
extractor.extract_round(text=text)
```
```python
['round brackets']
```

3) curly brackets
```python
extractor.extract_curly(text=text)
```
```python
['curly brackets', 'example']
```

4) nested brackets (you can allow to extract nested brackets for square and round cases in a similar manner.)
```python
extractor.extract_curly(text=text, allow_nested=True)
```
```python
['nested {example}']
```
