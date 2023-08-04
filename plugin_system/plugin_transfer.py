import asyncio
import importlib

from API.api_log import Log


async def plugin_transfer(function_name, plugin_dict, data=None):
    if plugin_dict:
        for plugin_key, plugin_date in plugin_dict.items():
            plugin_name = plugin_date['name']
            plugin_def = plugin_date['def']
            plugin_file_path = plugin_date['file_path']

            if function_name in plugin_def:
                try:
                    spec = importlib.util.spec_from_file_location(function_name, plugin_file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    target_function = getattr(module, function_name)

                    if data is not None:
                        task = asyncio.create_task(target_function(data))
                    else:
                        task = asyncio.create_task(target_function())

                    # 在后台运行任务对象，不堵塞自身
                    await asyncio.sleep(0)

                except Exception as e:
                    Log.error('error', f'调用插件 {plugin_file_path} 报错：{e}')


async def plugins_date(plugin_dict):
    plugin_data_list = {}
    for plugin_key, plugin_date in plugin_dict.items():
        plugin_name = plugin_date['name']
        plugin_file_path = plugin_date['file_path']
        spec = importlib.util.spec_from_file_location('', plugin_file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, 'PLUGIN_DATE'):
            PLUGIN_DATE = getattr(module, 'PLUGIN_DATE')
        else:
            PLUGIN_DATE = {
                'name': plugin_name,
                "author": "[未知]",
                'version': '[未知]',
                "description": "[未知]",
                "dependencies": {}
            }
        plugin_data_list[plugin_name] = PLUGIN_DATE

    return plugin_data_list
