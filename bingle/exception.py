class APIError(Exception):
    pass


class AICallerPrepreparationError(Exception):
    pass


class AICallerAPIError(Exception):
    pass


class AICallerPostprocessingError(Exception):
    pass


class APILimitError(Exception):
    pass
