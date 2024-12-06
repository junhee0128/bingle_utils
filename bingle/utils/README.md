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