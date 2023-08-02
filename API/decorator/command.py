function_records = {}


def on_command(command: str, substring: list[bool, int] or bool):
    def decorator(func):
        if type(substring) == bool:
            substring_bool = substring
            substring_num = 0
        else:
            substring_bool = substring[0]
            substring_num = substring[1]
        record = {
            'command': command,
            'function': func,
            'substring_bool': substring_bool,
            'substring_num': substring_num
        }
        function_records[func.__name__] = record
        return func

    if callable(command or substring):
        raise '你没有在装饰器内写入参数'

    return decorator

