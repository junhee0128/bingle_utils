import os
from typing import List, Dict
from bingle.ai_caller import AICaller
from bingle.utils import FileProcessor


def get_sample_messages() -> List[dict]:
    from bingle.ai_prompter import Messages, Prompt

    messages = Messages([Prompt(role='system', content="You are a helpful assistant."),
                         Prompt(role='user', content="What is your name?")])

    return messages.to_dict()


def test_ai_caller(apikeys: Dict[str, str]) -> dict:
    service = "chat"
    call_summaries = dict()

    for provider, apikey in apikeys.items():
        api_spec_dir = "./api_spec"
        ai_caller = AICaller(provider=provider, service=service, apikey=apikey, api_spec_dir=api_spec_dir)

        messages = get_sample_messages()

        call_summaries[provider] = ai_caller.complete(messages=messages)

        print(f"[{provider}] {call_summaries[provider].response}")

    return call_summaries


def load_credentials(credential_dir: str, providers: List[str] = AICaller.PROVIDERS) -> Dict[str, str]:
    apikeys = dict()
    for provider in providers:
        apikey_path = os.path.join(credential_dir, f"{provider}_apikey.txt")
        if os.path.exists(apikey_path):
            apikeys[provider] = FileProcessor().load_txt(filepath=apikey_path)

    return apikeys


if __name__ == "__main__":
    call_summ = test_ai_caller(
        apikeys=load_credentials(credential_dir="C:/Users/junhe/.credentials"))

    print("done")
