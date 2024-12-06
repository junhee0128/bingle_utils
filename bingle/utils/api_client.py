import requests
from typing import Union


class APIClient:
    @staticmethod
    def get(url: str, params: dict = None) -> Union[dict, None]:
        response = requests.get(url=url, params=params if params else dict())
        if response.status_code == 200:
            print("GET / response:", response.json())
            return response.json()
        else:
            print("GET / request failed with status code:", response.status_code)
            return

    @staticmethod
    def post(url: str, payload: dict, headers: dict, **kwargs):
        try:
            response = requests.post(url=url, json=payload, headers=headers)
            response.raise_for_status()

            if response.status_code == 200:
                return response.json()
            else:
                print(f"POST /items/ request failed with status code: {response.status_code} ({response.text})")
                return
        except Exception as e:
            return f"API Error: {e}"
