import requests
from bingle.exception import APIError


class APIClient:
    def get(self, url: str, params: dict = None, ssl_verify: bool = True) -> dict:
        response = requests.get(url=url, params=params if params else dict(), verify=ssl_verify)
        return self._post_processing(response=response)

    def post(self, url: str, payload: dict, headers: dict, ssl_verify: bool = True, **kwargs) -> dict:
        response = requests.post(url=url, json=payload, headers=headers, verify=ssl_verify)
        response.raise_for_status()
        return self._post_processing(response=response)

    @staticmethod
    def _post_processing(response):
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError(f"status code: {response.status_code}, message: {response.text}")
