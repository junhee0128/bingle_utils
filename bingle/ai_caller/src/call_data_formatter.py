class AICallDataFormatter:
    standard_provider: str = "openai"

    @staticmethod
    def convert_anthropic_payload(payload: dict) -> dict:
        _payload = payload.copy()
        if 'system' in payload:
            _payload['messages'] = [{'role': 'system', 'content': payload['system']}] + payload['messages']

        return _payload

    @staticmethod
    def convert_anthropic_response(response: dict) -> dict:
        _response = response.copy()
        choices = list()
        for idx, c in enumerate(response['content']):
            choice = {'index': idx,
                      'message': {'role': response['role'], 'content': [c]},
                      'stop_reason': response['stop_reason']}
            choices.append(choice)
        _response['choices'] = choices
        
        return _response
