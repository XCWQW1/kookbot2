import configparser
import json
import logging
import os
import sys
import threading

from API.flask import request, Flask
from API.api_log import LogSP, Log
from API.api_kook import KOOKApi

sdk = KOOKApi()


def plugin(msg_type, channel_id, channel_name, channel_message, channel_message_id, channel_user_id, channel_user_name,
           channel_user_nickname, channel_user_bot, target_id, target_name, data):
    pass


class LogApi:
    @staticmethod
    def info(info):
        log = f"[{LogSP.now_time()}] [信息] [接口] {info}"
        print(log)


def http_api():
    global http_api_ip
    global http_api_port
    app = Flask(__name__)

    # 配置日志记录器，将日志级别设置为更高级别以隐藏错误信息
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # 禁止将日志消息传播到父记录器
    log.propagate = False

    # 禁用 Flask 的默认启动日志
    cli_logger = logging.getLogger('werkzeug')
    cli_logger.setLevel(logging.ERROR)

    @app.route('/', methods=['GET'])
    def none_req():
        return_txt = "无效接口"
        LogApi.info(f"[接受] 来自：{request.remote_addr}，请求方法：{request.method}，访问：{request.url}，返回：{return_txt}")
        return return_txt

    @app.route('/send', methods=['GET'])
    def send():
        # 获取 URL 参数
        channel_id = int(request.args.get('channel_id'))
        message = request.args.get('message')
        if channel_id and message:
            # 两个参数都存在，执行相应操作
            send_message_id = sdk.send_channel_msg(message, 1, channel_id)
            return_txt = {"message_id": send_message_id, "stats": "ok"}
        else:
            # 两个参数都不存在或者有一个参数不存在，返回错误信息
            return_txt = {"stats": "failed", "error": "missing parameter"}
        LogApi.info(f"[接受] 来自：{request.remote_addr}，请求方法：{request.method}，访问：{request.url}，返回：{return_txt}")
        return return_txt

    @app.route('/webhook', methods=['POST'])
    def webhook():
        data = request.get_json()
        sdk.send_channel_msg(data["msg"], 1, 3273270382689856)
        LogApi.info(f"[接受] 来自：{request.remote_addr}，请求方法：{request.method}，访问：{request.url}，提交：{data}")
        return 'OK'

    @app.route('/webhook_mc', methods=['POST'])
    def webhook_mc():
        data = request.get_json()
        sdk.send_channel_msg(data["msg"], 1, 1795946950814768)
        LogApi.info(f"[接受] 来自：{request.remote_addr}，请求方法：{request.method}，访问：{request.url}，提交：{data}")
        return 'OK'

    @app.route('/webhook_ddnet', methods=['POST'])
    def webhook_ddnet():
        data = request.get_json()
        sdk.send_channel_msg(data["msg"], 1, 8182745819484970)
        LogApi.info(f"[接受] 来自：{request.remote_addr}，请求方法：{request.method}，访问：{request.url}，提交：{data}")
        return 'OK'

    @app.route('/webhook_giscord', methods=['POST'])
    def webhook_giscord():
        data = request.get_json()
        sdk.send_channel_msg(data["msg"], 1, 2595377413316826)
        LogApi.info(f"[接受] 来自：{request.remote_addr}，请求方法：{request.method}，访问：{request.url}，提交：{data}")
        return 'OK'

    @app.route('/ddn', methods=['GET'])
    def ddn():
        ip = request.args.get('ip')
        if ip:
            js_data = [
                {
                    "type": "card",
                    "theme": "secondary",
                    "size": "lg",
                    "modules": [
                        {
                            "type": "section",
                            "text": {
                                "type": "plain-text",
                                "content": f"服务器IP变动，当前为："
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "paragraph",
                                "cols": 2,
                                "fields": [
                                    {
                                        "type": "kmarkdown",
                                        "content": "**服务器**\n钩子模式\n\n\n钩子模式\n\n\n钩子模式\n\n\n感染模式\n\n\n榴弹夺旗模式\n\n\n猎人杀模式"
                                    },
                                    {
                                        "type": "kmarkdown",
                                        "content": f"**地址**\n[{ip}]:8303\n\n[{ip}]:8304\n\n[{ip}]:8305\n\n[{ip}]:8306\n\n[{ip}]:8308\n\n[{ip}]:8309"
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
            sdk.send_channel_msg(json.dumps(js_data), 10, 9933023112717409)
            LogApi.info(f"[接受] 来自：{request.remote_addr}，请求方法：{request.method}，访问：{request.url}，提交：{ip}")
        return 'OK'

    LogSP.initialize(f'[HTTP_API] 正在启动http api服务于地址：{http_api_ip}，端口：{http_api_port}')
    try:
        app.run(host=http_api_ip, port=http_api_port)
    except Exception as e:
        Log.error("error", f'[HTTP API] 错误信息：{e}')


async def on_init():
    global http_api_ip
    global http_api_port
    # 监测配置文件夹是否存在
    folders = ['plugins/qqbot_http_api']

    LogSP.initialize("[HTTP_API] 正在监测配置文件夹是否存在")
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            LogSP.initialize(f'[HTTP_API] 文件夹 {folder} 不存在，已自动创建')
        else:
            LogSP.initialize(f'[HTTP_API] 文件夹 {folder} 已经存在')
    # 配置文件路径
    config_path = "plugins/qqbot_http_api/config.ini"

    # 如果配置文件不存在，则创建一个新的配置文件
    if not os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.add_section("bot_http_api")
        config.set("bot_http_api", "http_api_ip", "0.0.0.0")
        config.set("bot_http_api", "http_api_port", "5000")
        with open(config_path, "w") as f:
            config.write(f)
        LogSP.initialize(f'[HTTP_API] 配置文件 {config_path} 不存在，已自动创建')
        LogSP.initialize("[HTTP_API] 已关闭程序，请重新启动以加载配置")
        sys.exit(0)
    else:
        LogSP.initialize(f'[HTTP_API] 配置文件 {config_path} 已经存在')

    # 读取配置文件
    c_config = configparser.ConfigParser()
    c_config.read(config_path)

    # 获取相应的配置信息
    http_api_ip = c_config.get("bot_http_api", "http_api_ip")
    http_api_port = int(c_config.get("bot_http_api", "http_api_port"))

    # 创建新线程
    t = threading.Thread(target=http_api, daemon=True)

    # 启动线程
    t.start()
