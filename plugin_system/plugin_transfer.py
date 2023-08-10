import asyncio
import importlib
import traceback

from API.api_log import Log


plugin_data_list = {}


async def plugin_transfer(function_name, plugin_dict, data=None):
    if plugin_dict:
        for plugin_key, plugin_date in plugin_dict.items():
            plugin_name = plugin_date['name']
            plugin_def = plugin_date['def']
            plugin_file_path = plugin_date['file_path']
            if plugin_def is not None:
                if function_name in plugin_def:
                    try:
                        if data is not None:
                            task = asyncio.create_task(plugin_def[function_name](data))
                        else:
                            task = asyncio.create_task(plugin_def[function_name]())

                        # 在后台运行任务对象，不堵塞自身
                        await asyncio.sleep(0)

                    except Exception as e:
                        Log.error('error', f'调用插件 {plugin_file_path} 报错：{traceback.format_exc()}')


async def plugins_date(plugin_dict):
    Log.initialize('正在获取插件元数据')
    for plugin_key, plugin_date in plugin_dict.items():
        plugin_name = plugin_date['name']
        plugin_file_path = plugin_date['file_path']
        try:
            spec = importlib.util.spec_from_file_location('', plugin_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except:
            Log.error('error', f'获取插件 {plugin_file_path} 元数据报错：{traceback.format_exc()}')
            continue

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
    Log.initialize(f'共成功获取到 {len(plugin_data_list)} 个插件的元数据')
    return plugin_data_list
