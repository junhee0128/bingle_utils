import inspect
from typing import Callable, Dict


class FunctionInspector:
    @staticmethod
    def inspect(func: Callable) -> Dict[str, str]:
        # 함수명
        func_name = func.__name__

        # 시그니처 가져오기
        signature = inspect.signature(func)

        # required 및 optional args (kwargs 제외)
        required_args = []
        optional_args = {}

        for name, param in signature.parameters.items():
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                continue  # **kwargs는 제외

            if param.default is inspect.Parameter.empty:
                required_args.append(name)
            else:
                optional_args[name] = param.default

        # 반환 타입
        return_type = signature.return_annotation
        if return_type is inspect.Signature.empty:
            return_type = "Not specified"

        return {"name": func_name,
                "func": func,
                "required_args": required_args,
                "optional_args": optional_args,
                "return_type": return_type}
