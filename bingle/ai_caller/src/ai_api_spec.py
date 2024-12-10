import os
from typing import List
from bingle.utils import FileProcessor


class DefaultKeyDict(dict):
    def __missing__(self, key):
        return f"{{{key}}}"


class AIAPISpec:
    API_SPEC_DIR: str = os.path.abspath(os.path.join(os.path.split(__file__)[0], "../api_spec"))

    def __init__(self, provider: str, service: str, apikey: str, api_spec_dir: str = None):
        if api_spec_dir is None:
            api_spec_dir = self.API_SPEC_DIR

        api_spec = FileProcessor().load_json(filepath=os.path.join(api_spec_dir, f"{provider}.json"))
        self.provider = provider
        self.service = service
        self.url = api_spec["endpoint_uri"].format_map(
            DefaultKeyDict({"resource_path": api_spec["resource_path"][service]}))
        if "uri_params" in api_spec:
            self.url = self.url.format(**api_spec["uri_params"])
        self.headers = api_spec["headers"]
        for key in self.headers:
            self.headers[key] = self.headers[key].format(apikey=apikey)
        self.default = api_spec["default"][service]

    def list_models(self) -> List[str]:
        model_list = FileProcessor().load_json(filepath=self.API_SPEC_DIR)
        assert self.provider in model_list
        return model_list[self.provider]
