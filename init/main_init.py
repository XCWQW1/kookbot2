def main_init():
    # 监测配置文件夹是否存在
    import configparser
    import os
    import sys

    from API.api_log import LogSP

    folders = ['plugins', 'logs', 'errors', 'config']

    LogSP.initialize("正在监测配置文件夹是否存在")
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            LogSP.initialize(f'文件夹 {folder} 不存在，已自动创建')
        else:
            LogSP.initialize(f'文件夹 {folder} 已经存在')

    # 配置文件路径
    config_path = "config/config.ini"

    # 如果配置文件不存在，则创建一个新的配置文件
    if not os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.add_section("kook")
        config.set("kook", "token", "xxxxxxxxxxxxxxxxxxxxxxxx")
        config.set("kook", "token_type", "None")
        with open(config_path, "w") as f:
            config.write(f)
        LogSP.initialize(f'配置文件 {config_path} 不存在，已自动创建')
        LogSP.initialize("已关闭程序，请重新启动以加载配置")
        sys.exit(0)
    else:
        LogSP.initialize(f'配置文件 {config_path} 已经存在')
