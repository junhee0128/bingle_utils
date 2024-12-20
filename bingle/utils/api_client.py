import requests
from bingle.exception import APIError


class APIClient:
    @staticmethod
    def get(url: str, params: dict = None, ssl_verify: bool = True) -> dict:
        try:
            response = requests.get(url=url, params=params if params else dict(), verify=ssl_verify)
            if response.status_code == 200:
                return response.json()
            else:
                raise APIError(f"status code: {response.status_code}, message: {response.text}")
        except Exception as e:
            raise e

    @staticmethod
    def post(url: str, payload: dict, headers: dict, ssl_verify: bool = True, **kwargs) -> dict:
        try:
            response = requests.post(url=url, json=payload, headers=headers, verify=ssl_verify)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
            else:
                raise APIError(f"status code: {response.status_code}, message: {response.text}")
        except Exception as e:
            raise e
