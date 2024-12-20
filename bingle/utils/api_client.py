import requests
from bingle.exception import APIError, APILimitError


class APIClient:
    def get(self, url: str, params: dict = None, ssl_verify: bool = True, **kwargs) -> dict:
        response = requests.get(url=url, params=params if params else dict(), verify=ssl_verify)
        return self.post_processing(response)

    def post(self, url: str, payload: dict, headers: dict, ssl_verify: bool = True, **kwargs) -> dict:
        response = requests.post(url=url, json=payload, headers=headers, verify=ssl_verify)
        return self.post_processing(response)

    @staticmethod
    def post_processing(response) -> dict:
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        else:
            err_msg = f"status code: {response.status_code}, message: {response.text}"
            if response.status_code == 429:
                print(err_msg)
                raise APILimitError(err_msg)
            else:
                raise APIError(err_msg)
