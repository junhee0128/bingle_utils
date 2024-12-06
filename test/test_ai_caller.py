import os
from typing import List, Dict
from bingle.ai_caller import AICaller
from bingle.utils import FileProcessor


def get_sample_messages() -> List[dict]:
    from bingle.ai_prompter import Messages, Prompt

    messages = Messages([Prompt(role='system', content="You are a helpful assistant."),
                         Prompt(role='user', content="What is your name?")])

    return messages.to_dict()


def test_ai_caller(apikeys: Dict[str, str]) -> (dict, dict):
    service = "chat"
    responses = dict()
    payloads = dict()

    for provider, apikey in apikeys.items():
        ai_caller = AICaller(provider=provider, service=service, apikey=apikey)

        messages = get_sample_messages()

        api_spec_dir = "./api_spec"
        ai_caller.copy_default_api_spec_to(to_dir=api_spec_dir, ignore_error=True)

        responses[provider], payloads[provider] = ai_caller.complete(messages=messages, return_payload=True,
                                                                     api_spec_dir=api_spec_dir)

        print(f"[{provider}] {responses[provider]}")

    return responses, payloads


def load_credentials(credential_dir: str, providers: List[str] = AICaller.PROVIDERS) -> Dict[str, str]:
    apikeys = dict()
    for provider in providers:
        apikey_path = os.path.join(credential_dir, f"{provider}_apikey.txt")
        if os.path.exists(apikey_path):
            apikeys[provider] = FileProcessor().load_txt(filepath=apikey_path)

    return apikeys


if __name__ == "__main__":
    resp, payl = test_ai_caller(
        apikeys=load_credentials(credential_dir="C:/Users/junhe/.credentials", providers=["openai"]))

    print("done")
