import configparser
import json

import aiohttp
import requests

from typing import Optional, Union

from API.api_log import Log

#######################################################################
#                                 接口                                 #
#                          用于调用kook的http api                       #
#                 如果访问失败将会返回json中的状态代码(code)的值             #
#######################################################################


# 加载配置文件
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


# 接口总类
class KOOKApi:
    # 初始化函数
    def __init__(self):
        self.token, self.token_type = load_config()  # 获取token和token_type
        self.koo_url = "https://www.kookapp.cn"  # kook的地址

    async def kook_http_api_post(self, api_url, post_data) -> json:
        """
        带访问头post访问KOOK的API用于简化后面函数的一些操作
        :param api_url:  # 提交的API地址
        :param post_data:  # 提交的数据 json 格式
        :return:  # 访问后返回访问接口后返回的未经过任何处理的原始json
        """
        url = self.koo_url + api_url

        headers = {
            "Authorization": f"{self.token_type} {self.token}",
            "X-Rate-Limit-Limit": "5",
            "X-Rate-Limit-Remaining": "0",
            "X-Rate-Limit-Reset": "14",
            "X-Rate-Limit-Bucket": "user/info",
            "X-Rate-Limit-Global": ""
        }

        response_json = requests.post(url, headers=headers, data=post_data).json()

        return response_json

    async def kook_http_api_get(self, api_url, get_data) -> json:
        """
        带访问头get访问KOOK的API用于简化后面函数的一些操作
        :param api_url:  # 提交的API地址
        :param get_data:  # 提交的数据 json 格式
        :return:  # 访问后返回访问接口后返回的未经过任何处理的原始json
        """
        url = self.koo_url + api_url

        headers = {
            "Authorization": f"{self.token_type} {self.token}",
            "X-Rate-Limit-Limit": "5",
            "X-Rate-Limit-Remaining": "0",
            "X-Rate-Limit-Reset": "14",
            "X-Rate-Limit-Bucket": "user/info",
            "X-Rate-Limit-Global": ""
        }

        response_json = requests.get(url, headers=headers, params=get_data).json()

        return response_json

    async def send_channel_msg(self, send_msg: str or json, msg_type: Optional[int] = 9, channel_id: Optional[int] = None, quote: Optional[str] = None, temp_target_id: Optional[str] = None) -> str:
        """
        给指定频道发送指定消息
        :param quote:  # 要引用的消息ID，可以为空，空则不引用直接发送
        :param msg_type:  # 消息了类型，根据kook官方文档的那个走即可：https://developer.kookapp.cn/doc/http/message#%E5%8F%91%E9%80%81%E9%A2%91%E9%81%93%E8%81%8A%E5%A4%A9%E6%B6%88%E6%81%AF
        :param send_msg:  # 需要发送的消息
        :param channel_id:  # 要发送到频道的频道id
        :param temp_target_id:  # 单独回应的用户id
        :return:  # 成功后返回消息id
        """
        if quote is None:
            post_data = {
                "type": msg_type,
                "target_id": channel_id,
                "content": send_msg
            }
        else:
            post_data = {
                "type": msg_type,
                "target_id": channel_id,
                "content": send_msg,
                "quote": quote
            }
        if temp_target_id is not None:
            post_data['temp_target_id'] = temp_target_id

        request = await self.kook_http_api_post("/api/v3/message/create", post_data)

        if request['code'] == 0:
            if msg_type == 1:
                Log.send(msg_type, send_msg, channel_id, request['data']['msg_id'])
            else:
                Log.send(msg_type, send_msg, channel_id, request['data']['msg_id'])
            return request['data']['msg_id']
        else:
            Log.error('error', '[发送频道消息]' + str(request))
            return request['code']

    async def send_direct_msg(self, send_msg: str or json, msg_type: Optional[int] = 9, user_id: Optional[int] = None, quote: Optional[str] = None) -> str:
        """
        发送私聊消息
        :param send_msg:  要发送的消息
        :param msg_type:   消息类型默认9
        :param user_id:   发送的用户id
        :param quote:  引用消息的id
        :return:
        """
        if quote is None:
            post_data = {
                "type": msg_type,
                "target_id": user_id,
                "content": send_msg
            }
        else:
            post_data = {
                "type": msg_type,
                "target_id": user_id,
                "content": send_msg,
                "quote": quote
            }

        request = await self.kook_http_api_post("/api/v3/direct-message/create", post_data)

        if request['code'] == 0:
            if msg_type == 1:
                Log.send(msg_type, send_msg, user_id, request['data']['msg_id'])
            else:
                Log.send(msg_type, send_msg, user_id, request['data']['msg_id'])
            return request['data']['msg_id']
        else:
            Log.error('error', '[发送私聊消息]' + str(request))
            return request['code']

    async def get_server_name(self, server_id: int) -> str:
        """
        获取指定服务器的名称
        :param server_id:  # 服务器id
        :return:  # 成功后返回服务器名称
        """
        get_data = {
            "guild_id": server_id
        }
        request = await self.kook_http_api_get("/api/v3/guild/view", get_data)
        if request['code'] == 0:
            return request['data']['name']
        else:
            Log.error('error', '[获取服务器名称]' + str(request))
            return request['code']

    async def get_channel_name(self, channel_id: int) -> str:
        """
        获取指定频道的名称
        :param channel_id:  # 频道id
        :return:  # 成功后返回频道名称
        """
        get_data = {
            "target_id": channel_id
        }
        request = await self.kook_http_api_get("/api/v3/channel/view", get_data)
        if request['code'] == 0:
            return request['data']['name']
        else:
            Log.error('error', '[获取频道名称]' + str(request))
            return request['code']

    async def upload_files(self, file_name: Union[str, bytes]) -> str:
        """
        上传文件
        :param file_name:  # 输入str类 则文件精准路径会自动转换为二进制，输入bytes会直接发送，方便图片渲染等直接发送二进制
        :return:  # 成功后返回文件直连
        """

        url = self.koo_url + "/api/v3/asset/create"

        payload = aiohttp.FormData()
        if type(file_name) == str:
            payload.add_field('file', open(file_name, 'rb'))
        else:
            payload.add_field('file', file_name)

        headers = {
            "Authorization": f"{self.token_type} {self.token}"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    response_json = await response.json()
        except Exception as e:
            response_json = {'code': '1', 'data': {'url': 'error'}}

        if response_json['code'] == 0:
            return response_json['data']['url']
        else:
            Log.error('error', '[上传文件]' + str(response_json))
            return response_json['code']

    async def add_reaction(self, msg_id: str, emoji: str) -> str:
        """
        给指定消息添加回应
        :param msg_id:  # 要添加的消息id
        :param emoji:  # 要添加的emoji
        :return:  # 成功后返回code
        """
        post_data = {
            "msg_id": msg_id,
            "emoji": emoji
        }
        request = await self.kook_http_api_post("/api/v3/message/add-reaction", post_data)
        if request['code'] == 0:
            return request['code']
        else:
            Log.error('error', '[添加回应]' + str(request))
            return request['code']

    async def update_message(self, msg_id: str, new_msg: str, quote: Optional[str] = None) -> str:
        """
        更新指定消息
        :param quote:
        :param msg_id:  # 要更新的消息id
        :param new_msg:  # 要更新的消息
        :return:  # 返回code
        """
        if quote is None:
            post_data = {
                "msg_id": msg_id,
                "content": new_msg
            }
        else:
            post_data = {
                "msg_id": msg_id,
                "content": new_msg,
                "quote": quote
            }

        request = await self.kook_http_api_post("/api/v3/message/update", post_data)
        if request['code'] != 0:
            Log.error('error', '[]' + str(request))
        return request['code']

    async def game(self, type: int) -> dict:
        """
        显示游戏列表
        :param type:  类型：0全部 1用户创建 2系统创建
        :return:  返回字典 {id: name, xxxxxxx}
        """
        get_data = {
            "type": type
        }

        request = await self.kook_http_api_get("/api/v3/game", get_data)

        if request['code'] == 0:
            js_dict = {}
            for js in request['data']['items']:
                js_dict[js['id']] = js['name']
            return js_dict
        else:
            Log.error('error', '[显示游戏列表]' + str(request))
            return {'code': request['code']}

    async def create_game(self, name: str) -> str:
        """
        创建游戏
        :param name:  输入游戏名
        :return:  返回游戏id
        """
        post_data = {
            "name": name
        }

        request = await self.kook_http_api_post("/api/v3/game/create", post_data)

        if request['code'] == 0:
            return request['data']['id']
        else:
            Log.error('error', '[创建游戏]' + str(request))
            return request['code']

    #################
    #     未完工     #
    #################

    async def activity_game(self, id: int, data_type: int) -> str:
        post_data = {
            "id": id,
            "data_type": data_type
        }
        request = await self.kook_http_api_post("/api/v3/game/activity", post_data)
        return request['code']

    #################
    #     未完工     #
    #################

    async def voice_channel_user_list(self, channel_id: int):
        post_data = {
            "channel_id": channel_id
        }
        request = await self.kook_http_api_post("/api/v3/channel/user-list", post_data)
        if request['code'] == 0:
            return request['data']
        else:
            Log.error('error', '[语音频道用户列表]' + str(request))
            return request['code']

    async def view_user(self, user_id: int) -> str:
        post_data = {
            "user_id": user_id
        }

        request = await self.kook_http_api_get("/api/v3/user/view", post_data)

        if request['code'] == 0:
            return request['data']
        else:
            Log.error('error', '[获取用户信息]' + str(request))
            return request['code']

    async def offline_user(self) -> str:
        request = await self.kook_http_api_post("/api/v3/user/offline", {})

        if request['code'] == 0:
            return request['data']
        else:
            Log.error('error', '[下线]' + str(request))
            return request['code']

    async def get_me_info(self) -> str:
        request = await self.kook_http_api_get("/api/v3/user/me", {})

        if request['code'] == 0:
            return request['data']
        else:
            Log.error('error', '[获取自身信息]' + str(request))
            return request['code']
