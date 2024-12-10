from dataclasses import dataclass


@dataclass
class AICallError:
    call_id: str
    provider: str
    service: str
    message: str
    created: int

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.__annotations__:
                self.__dict__[k] = v
