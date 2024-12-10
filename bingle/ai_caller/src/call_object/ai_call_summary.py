from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime
from typing import List


@dataclass
class AICallSummary:
    provider: str
    service: str
    success: bool
    model: str
    call_id: str = None
    error: str = None
    message: str = None
    traceback: str = None
    id: str = None
    created: int = None
    payload: dict = None
    response: dict = None

    def __init__(self, **kwargs):
        for k in self.__annotations__:
            if k in kwargs:
                if k not in self._get_temp_args():
                    self.__dict__[k] = kwargs[k]
            else:
                self.__dict__[k] = None

        if self.call_id is None:
            self.call_id = self._get_call_id()
        if self.created is None:
            self.created = int(datetime.now().timestamp())

    @staticmethod
    def _get_call_id():
        return str(uuid4())

    def insert_payload(self, payload: dict):
        self.payload = payload
        if 'model' in payload and payload['model'] is not None:
            self.model = payload['model']

    def insert_response(self, response: dict):
        self.response = response
        self.id = response['id'] if 'id' in response else f'{self.provider}_{str(uuid4())}'
        if 'created' in response and response['created'] is not None:
            self.created = response['created']
        if 'model' in response and response['model'] is not None:
            self.model = response['model']

    @staticmethod
    def _get_temp_args() -> List[str]:
        return ['payload', 'response']

    def to_dict(self) -> dict:
        _dict = dict()
        for k in self.__annotations__:
            if k not in self._get_temp_args():
                if k in self.__dict__:
                    _dict[k] = self.__dict__[k]
                else:
                    _dict[k] = None
        return {k: self.__dict__[k] for k in self.__annotations__ if k not in self._get_temp_args()}
