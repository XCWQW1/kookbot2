import configparser


def load_config() -> [str, str]:
    # 配置文件路径
    c_config_path = "config/config.ini"

    # 读取配置文件
    c_config = configparser.ConfigParser()
    c_config.read(c_config_path)

    # 获取相应的配置信息
    c_kook_token = c_config.get("kook", "token")
    c_kook_token_type = c_config.get("kook", "token_type")

    return c_kook_token, c_kook_token_type
