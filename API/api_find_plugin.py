import importlib
import inspect
import os
import traceback

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from art import text2art

from API.api_log import Log
from colorama import init, Fore, Style

# 初始化colorama
init()


def load_plugin(plugin_file):
    # 获取模块名
    name = os.path.splitext(plugin_file)[0]
    Log.initialize(f"检测到插件：{name}")
    # 动态导入模块
    loader = importlib.machinery.SourceFileLoader(name, plugin_file)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    # 返回插件函数和名称
    return module.plugin, name


def list_plugins():
    # 插件列表
    p_plugin_list = []
    p_name_list = []
    Log.initialize("检测插件中...")
    Log.initialize("PS：插件中只有接收到事件才会调用,此时只是导入了内存地址")

    try:
        # 创建线程池
        with ThreadPoolExecutor() as executor:
            plugin_files = [os.path.join("plugins", plugin_file) for plugin_file in os.listdir("plugins")
                            if plugin_file.endswith('.py') and not plugin_file.startswith('.')]
            # 提交插件加载任务到线程池，并获取Future对象列表
            futures = [executor.submit(load_plugin, plugin_file) for plugin_file in plugin_files]

            # 获取所有插件的结果
            results = []
            for future in as_completed(futures):
                plugin, name = future.result()
                results.append((plugin, name))

    except Exception as e:
        Log.error("error", f"加载插件报错：{e}")
        return [], []

    # 处理结果
    for plugin, name in results:
        p_plugin_list.append(plugin)
        p_name_list.append(name)

    current_time = time.time()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
    art_text = text2art('Loaded Successfully')

    # 拆分艺术字的每一行，并在每行前面添加当前时间
    art_lines = art_text.split('\n')
    art_with_time = [f"[{now_time}] [初始]" + ' ' + line for line in art_lines]

    # 将带有时间的每行重新组合成一个字符串
    result = '\n'.join(art_with_time)

    print(Fore.GREEN + result + Style.RESET_ALL)

    return p_plugin_list, p_name_list
