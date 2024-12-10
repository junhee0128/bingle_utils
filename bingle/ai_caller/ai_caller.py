import os
import shutil
import traceback
from typing import List, Dict
from bingle.utils import APIClient
from .src.call_object import AICallSummary
from .src.ai_api_spec import AIAPISpec
from .src.call_data_formatter import AICallDataFormatter


class AICaller(AICallDataFormatter):
    APIKEY_ENV_NAME: str = "BINGLE_APIKEY"
    PROVIDERS: List[str] = ["openai", "llamaapi", "perplexity", "anthropic", "xai", "azure_openai"]

    def __init__(self, provider: str, service: str, apikey: str = None, api_spec_dir: str = None):
        AICallDataFormatter.__init__(self)
        if provider in self.list_providers():
            self.provider = provider
            self.service = service
            self.api_spec_dir = api_spec_dir
            if apikey is not None:
                os.environ[self.APIKEY_ENV_NAME] = apikey
            self._copy_default_api_spec_to(to_dir=api_spec_dir, ignore_error=True)
        else:
            raise NotImplementedError(f"Not supported for the provider '{provider}'.")

    def list_providers(self) -> List[str]:
        return self.PROVIDERS

    def complete(self, messages: List[Dict], model: str = None, standardize_format: bool = True) -> AICallSummary:
        api_spec = self._load_ai_api_spec()
        _model = api_spec.default['model'] if model is None else model

        try:
            # Payload 세팅.
            payload = self._get_payload(default=api_spec.default, messages=messages, model=_model)

            # API Call
            response = APIClient().post(payload=payload, ssl_verify=False, **api_spec.__dict__)

            if standardize_format and self.provider == 'anthropic':
                payload = self.convert_anthropic_payload(payload=payload)
                response = self.convert_anthropic_response(response=response)

            summary = AICallSummary(provider=self.provider, service=self.service, model=_model, success=True)
            summary.insert_payload(payload)
            summary.insert_response(response)
            return summary
        except Exception as e:
            return AICallSummary(provider=self.provider, service=self.service, model=_model, success=False,
                                 error=e.__class__.__name__, message=str(e), traceback=traceback.format_exc())

    def list_models(self) -> List[str]:
        api_spec = self._load_ai_api_spec()
        return api_spec.supported_models

    def _load_ai_api_spec(self) -> AIAPISpec:
        return AIAPISpec(provider=self.provider, service=self.service,
                         apikey=self._get_apikey(), api_spec_dir=self.api_spec_dir)

    def _get_apikey(self):
        return os.environ[self.APIKEY_ENV_NAME]

    def _get_payload(self, default: dict, messages: List[Dict], model: str):
        assert messages
        payload = default.copy()
        if isinstance(model, str):
            payload["model"] = model
        if self.provider == "anthropic":
            # 시스템 메시지는 없거나 하나만 있어야 하고, messages의 맨 앞에 위치 해야 함.
            assert len([msg for msg in messages[1:] if msg['role'] == 'system']) == 0
            if messages[0]['role'] == 'system':
                payload['system'] = messages[0]['content']
                payload['messages'] = messages[1:]
            else:
                payload['messages'] = messages
        else:
            payload['messages'] = messages

        return payload

    @staticmethod
    def get_model_list_url() -> dict:
        return {"openai": "https://platform.openai.com/docs/models",
                "xai": "https://docs.x.ai/docs#models",
                "perplexity": "https://docs.perplexity.ai/guides/model-cards",
                "llamaapi": "https://docs.llama-api.com/quickstart",
                "anthropic": "https://docs.anthropic.com/en/docs/about-claude/models",
                "azure_openai": "https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=python-secure%2Cglobal-standard%2Cstandard-chat-completions"}

    @staticmethod
    def _copy_default_api_spec_to(to_dir: str, ignore_error: bool = False):
        if os.path.exists(to_dir):
            if not ignore_error:
                raise FileExistsError(f"Directory '{os.path.abspath(to_dir)}' already exists.")
            else:
                pass
        else:
            shutil.copytree(AIAPISpec.API_SPEC_DIR, to_dir)
