import inspect
from datetime import datetime
from typing import Callable

__CTX_VARS_NAME__ = "context_variables"


def debug_print(debug: bool, *args: str) -> None:
    if not debug:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = " ".join(map(str, args))
    print(f"\033[97m[\033[90m{timestamp}\033[97m]\033[90m {message}\033[0m")


def function_to_json(func: Callable, exclude_parameter_names: []) -> dict:
    """
    将一个函数转成json格式，用来传递给大模型completion的tools参数
    :param func: 要转换的函数
    :param exclude_parameter_names: 要排除的变量名字
    :return: func为None时，返回空的dict
    """
    if not func:
        return {}
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }
    # 获取 func 的函数参数
    signature = inspect.signature(func)
    # 将参数填充到 parameters 中
    parameters = {}
    for param in signature.parameters.values():
        # 如果存在在“不需要转换的参数名列表”，那么就不转换
        if param.name in exclude_parameter_names:
            continue
        param_type = type_map.get(param.annotation, "string")
        parameters[param.name] = {"type": param_type, "description": ""}

    # 必填参数
    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
        and param.name not in exclude_parameter_names
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required
            }
        }
    }


