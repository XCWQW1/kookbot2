import inspect
import os

function_records = {}


def on_command(command: str, substring: list[bool, int] or bool):
    def decorator(func):
        if type(substring) == bool:
            substring_bool = substring
            substring_num = 0
        else:
            substring_bool = substring[0]
            substring_num = substring[1]
        plugins_file = os.getcwd() + '/plugins/'
        file_name = inspect.getfile(func).replace(plugins_file, '').replace('.py', '')
        record = {
            'command': command,
            'func_name': func.__name__,
            'file_name': file_name,
            'substring_bool': substring_bool,
            'substring_num': substring_num
        }
        if file_name in function_records:
            function_records[file_name][record['command']] = record
        else:
            function_records[file_name] = {record['command']: record}
        return func

    if callable(command or substring):
        raise Exception('你没有在装饰器内写入参数')

    return decorator
