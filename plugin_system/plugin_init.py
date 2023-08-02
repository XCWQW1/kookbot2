import importlib
import os
import inspect
import importlib.util

from colorama import init
from API.api_log import Log

# 初始化colorama
init()


async def find_plugin():
    plugin_files = [os.path.join("plugins", plugin_file) for plugin_file in os.listdir("plugins")
                    if plugin_file.endswith('.py') and not plugin_file.startswith('__')]
    return plugin_files


async def get_functions_from_file(file_path):
    module_name = inspect.getmodulename(file_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    functions = [name for name, obj in inspect.getmembers(module) if inspect.isfunction(obj)]

    return functions


async def get_plugins_functions_and_def():
    Log.initialize('开始寻找插件！')
    plugin_num = 0
    plugin_dnf_list = {}
    get_find_plugins_list = await find_plugin()
    for file_path in get_find_plugins_list:
        name = file_path.split('plugins/')[1].replace('.py', '')
        Log.initialize(f'找到插件：{name}')
        def_ls = await get_functions_from_file(file_path)
        plugin_dnf_list[plugin_num] = {'name': name, 'file_path': file_path, 'def': def_ls}
        plugin_num = plugin_num + 1
    Log.initialize(f'寻找完毕，共计 {plugin_num} 个插件')
    return plugin_dnf_list
