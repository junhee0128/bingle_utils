from test_ai_caller import *
from demo.ai_call_log_handler import AICallLogHandler


def test_ai_call_db_logging(log_base_dir: str, providers: List[str]):
    responses, payloads = test_ai_caller(
        apikeys=load_credentials(credential_dir="C:/Users/junhe/.credentials", providers=providers))

    log_handler = AICallLogHandler(base_dir=log_base_dir)

    service = "chat"

    for provider, response in responses.items():
        log_handler.log_to_db(provider=provider, service=service,
                              payload=payloads[provider], response=responses[provider])


def test_ai_call_db_log_loading(log_base_dir: str, call_id: str):
    log_handler = AICallLogHandler(base_dir=log_base_dir)

    return log_handler.load_call(call_id=call_id)


if __name__ == "__main__":
    log_dir = "./"

    test_ai_call_db_logging(log_base_dir=log_dir, providers=['azure_openai'])

    cid = "a4dfd96a-90b6-42f9-bdf3-6781fa018f8d"
    call_obj = test_ai_call_db_log_loading(log_base_dir=log_dir, call_id=cid)
    if call_obj:
        print(f"The call_id of the loaded object is '{call_obj.get_call_id()}'.")

    print("done")
