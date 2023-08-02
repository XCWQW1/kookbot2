import json

from API.api_kook import KOOKApi
from API.api_kook_card import Card
from API.decorator.command import on_command

API = KOOKApi()
API_CARD = Card()


# 有时间我会写个文档挂github去，不知道data的内容可以直接print出来看，是个字典
# 注册指令
# 常规精准识别
@on_command('TEST-0', substring=False)
async def test_0(data):
    msg = 'TEST-0! Hello World!'  # 要发送的消息，此处为提升可读单独赋值给变量后发送，可以直接写到下方API的msg里
    API.send_channel_msg(msg, 1, data['events']['channel_id'], data['events']['message_id'])  # 发送消息, channel_message_id 可不提供，不提供则不引用触发消息直接发送, 1为消息类型 详见KOOK官方文档 发送卡片时需json.dumps(json_data)
    # API.send_channel_msg(msg, 1, data['events']['channel_id'])  # 不引用
    # API.send_channel_msg('TEST! Hello World!', 1, data['events']['channel_id'], data['events']['message_id'])  # 直接写


# 取最左边5个字
@on_command('TEST ', substring=[True, 5])
async def test_0(data, msg):  # data 和上面的一样，msg是除去触发词 TEST  后的内容空格也去了
    API.send_channel_msg(msg, 1, data['events']['channel_id'], data['events']['message_id'])


# 发图
@on_command('TEST-1', substring=False)
async def test_1(data):
    file_url = API.upload_files('plugins/test.png')  # 先上传文件，可是文件路径，也可是文件的二进制 返回图片链接
    API_CARD.send_img(file_url, data['events']['channel_id'])  # 发送


# 自定义卡片
@on_command('TEST-2', substring=False)
async def test_2(data):
    json_data = [
        {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "modules": [
                {
                    "type": "section",
                    "text": {
                        "type": "kmarkdown",
                        "content": "(font)自(font)[success](font)定(font)[purple](font)义(font)[warning](font)卡(font)[pink](font)片(font)[success]"
                    }
                }
            ]
        }
    ]  # 可用kook官方的卡片编辑器生成json : https://www.kookapp.cn/tools/message-builder.html#/card
    API.send_channel_msg(json.dumps(json_data), 10, data['events']['channel_id'])  # 消息ID设置为10即可发送，引用无效


# 添加回应
@on_command('TEST-3', substring=False)
async def test_3(data):
    API.add_reaction(data['events']['message_id'], '✅')  # 要按顺序填入消息ID和要回应的emoji或emoji ID或GuilEmoji


# 发送按钮卡片
@on_command('TEST-4', substring=False)
async def test_4(data):
    json_data = [
        {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "modules": [
                {
                    "type": "action-group",
                    "elements": [
                        {
                            "type": "button",
                            "theme": "primary",
                            "value": "ok",
                            "click": "return-val",
                            "text": {
                                "type": "plain-text",
                                "content": "确定"
                            }
                        },
                        {
                            "type": "button",
                            "theme": "danger",
                            "value": "cancel",
                            "click": "return-val",
                            "text": {
                                "type": "plain-text",
                                "content": "取消"
                            }
                        }
                    ]
                }
            ]
        }
    ]
    API.send_channel_msg(json.dumps(json_data), 10, data['events']['channel_id'])


# 处理按钮卡片按下
async def message_button_click(data):
    API.send_channel_msg(f"{data['user']['nickname']} 按下了 {data['card']['value']}", 9, data['card']['channel_id'], data['card']['message_id'])


async def user_exit_guild(data):
    pass  # 累了 有时间在写 当有用户退出服务器会调用这个函数


async def user_join_guild(data):
    pass  # 同上，有人加入服务器调用


async def user_self_exit_guild(data):
    pass  # 自己退出服务器会调用这个函数


async def user_self_join_guild(data):
    pass  # 同上，自己加入服务器调用


async def on_init():
    print('-------------------------------------------------------------')
    print('用于初始化一些东西，框架将会在框架初始化完成后并且已经连接到ws后时候执行他')
    print('-------------------------------------------------------------')
