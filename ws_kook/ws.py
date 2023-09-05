import asyncio
import configparser
import datetime
import time
import traceback
import zlib
import json
import sys

import websockets

from API.api_kook import KOOKApi
from API.api_log import Log
from ws_kook.gateway import get_ws
from API.api_load_config import load_config
from plugin_system.plugin_init import get_plugins_functions_and_def
from plugin_system.plugin_transfer import plugin_transfer
from .transfer_plugin import process_message


link_status = 1
sleep_time = 0
session_id = ''
sn = 1
wait_json = []
try_link = False
init_stats = False
ping_stats = False


#################################################
# 一个websocket客户端，用于连接kook的websocket服务器 #
#################################################


async def connect_to_kook_server():
    global link_status
    global sleep_time
    global session_id
    global sn
    global wait_json
    global init_stats
    global ping_stats

    plugin_list = await get_plugins_functions_and_def()
    kook_token, kook_token_type = load_config()

    if kook_token_type == "None":
        Log.initialize('请选择鉴权方式：')
        Log.initialize('1，Bot')
        Log.initialize('2，Bearer')
        token_type = input('输入序号：')
        config_path = "config/config.ini"
        config = configparser.ConfigParser()

        if token_type == '1':
            token_type = 'Bot'
            config.read(config_path)
            config.set("kook", "token_type", token_type)
            with open(config_path, "w") as f:
                config.write(f)
            Log.initialize('已写入配置文件，日后更改请更改config/config.ini')

        elif token_type == '2':
            token_type = 'Bearer'
            config.read(config_path)
            config.set("kook", "token_type", token_type)
            with open(config_path, "w") as f:
                config.write(f)
            Log.initialize('已写入配置文件，日后更改请更改config/config.ini')

        elif not token_type in ['1', '2']:
            Log.error('error', '不支持除1和2以外的其他参数')
            sys.exit(0)
    else:
        kook_token, kook_token_type = load_config()

    async def add_sleep_time():
        global sleep_time
        if sleep_time != 60:
            sleep_time = sleep_time + 1

    async def ping_kook(websocket):
        global link_status
        global try_link
        global ping_stats
        global sn
        global wait_json
        global sleep_time

        while True:
            if sn == 1:
                new_sn = 0
            else:
                new_sn = sn - 1
            send_message = {"s": 2, "sn": new_sn}  # 要发送的消息
            try:
                await websocket.send(json.dumps(send_message))
            except:
                await asyncio.sleep(2)
                try:
                    await websocket.send(json.dumps(send_message))
                except:
                    pass
                if ping_stats:
                    ping_stats = False
                    ok_ping_num += 1

                await asyncio.sleep(4)
                try:
                    await websocket.send(json.dumps(send_message))
                except:
                    pass
                if ping_stats:
                    ping_stats = False
                    ok_ping_num += 1

                if ok_ping_num == 2:
                    Log.diy_log('验活', f'两次ping都成功收到pong，复位计数器')
                    ok_ping_num = 0
                else:
                    Log.error('error', f'两次ping都没有收到pong，准备重连')

                    ok_ping_num = 0
                    sn = 1
                    wait_json.clear()
                    link_status = 1

                    try:
                        await KOOKApi().offline_user()
                    except:
                        pass
                    try:
                        await websocket.close()
                    except:
                        pass

                    break

            await asyncio.sleep(6)
            ok_ping = False
            ok_ping_num = 0

            while True:
                if ping_stats:
                    ping_stats = False
                    ok_ping = True
                    break
                else:
                    Log.error('error', f'ping没有收到pong，准备最后尝试两次ping')
                    await asyncio.sleep(2)
                    try:
                        await websocket.send(json.dumps(send_message))
                    except:
                        pass
                    if ping_stats:
                        ping_stats = False
                        ok_ping_num += 1

                    await asyncio.sleep(4)
                    try:
                        await websocket.send(json.dumps(send_message))
                    except:
                        pass
                    if ping_stats:
                        ping_stats = False
                        ok_ping_num += 1

                    if ok_ping_num == 2:
                        Log.diy_log('验活', f'两次ping都成功收到pong，复位计数器')
                        ok_ping_num = 0
                    else:
                        Log.error('error', f'两次ping都没有收到pong，准备重连')

                        ok_ping_num = 0
                        sn = 1
                        wait_json.clear()
                        link_status = 1

                        try:
                            await KOOKApi().offline_user()
                        except:
                            pass
                        try:
                            await websocket.close()
                        except:
                            pass

                break

            # 等待30秒后再次发送
            await asyncio.sleep(30)

    while True:
        try:
            if link_status == 1:
                try:
                    gateway = await get_ws(kook_token_type, kook_token)
                except:
                    Log.error('error', f'访问Gateway失败，正在指数回退 {sleep_time}s 后将会重新获取Gateway')
                    time.sleep(sleep_time)
                    await add_sleep_time()
                if gateway['code'] == 0:
                    kook_ws_url = gateway['data']['url']
                    Log.initialize('Gateway获取成功')
                    sleep_time = 0
                    link_status = 2
                elif gateway["code"] == 401:
                    Log.error('error', '您的TOKEN无效，请检查机器人TOKEN是否正确')
                    sys.exit(0)
                else:
                    Log.error('error', f'访问Gateway失败，正在指数回退 {sleep_time}s 后将会重新获取Gateway')
                    time.sleep(sleep_time)
                    await add_sleep_time()
            elif link_status == 2:
                async with websockets.connect(kook_ws_url) as websocket:
                    loop = asyncio.get_event_loop()
                    task = loop.create_task(ping_kook(websocket))
                    async for message in websocket:
                        try:
                            message = zlib.decompress(message)
                            data = json.loads(message)

                            # DEBUG
                            DEBUG = False
                            if DEBUG:
                                if str(data) == "{'s': 3}":
                                    current_time = datetime.datetime.now()
                                    new_time = current_time + datetime.timedelta(seconds=30)
                                    formatted_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
                                    Log.diy_log('调试', str(data) + f'|下一次pong应位于[{str(formatted_time)}]左右')
                                else:
                                    Log.diy_log('调试', data)
                            # DEBUG

                            if data['s'] == 3:
                                ping_stats = True

                            if data['s'] == 1 and data['d']['code'] == 0:
                                link_status = 3
                                Log.initialize(
                                    f'接收到了kook传回的HELLO包，判断为连接成功，获取到的会话ID为：{data["d"]["session_id"]}')
                                session_id = data["d"]["session_id"]
                                if not init_stats:
                                    Log.initialize('开始初始化所有插件')
                                    await plugin_transfer('on_init', plugin_list)
                                    init_stats = True
                                else:
                                    Log.initialize('初始化已经执行过一次了，跳过初始化')

                                if sleep_time != 0:
                                    sleep_time = 0
                                    Log.diy_log('信息', 'ws连接成功！指数回退已重置为 0s')

                            elif data['s'] == 1 and data['d']['code'] == 40103:
                                Log.error('error',
                                          f'您的TOKEN已过期，正在指数回退 {sleep_time}s 后将会重新获取Gateway并连接ws')
                                time.sleep(sleep_time)
                                await add_sleep_time()

                            elif data['s'] == 1 and data['d']['code'] != 0:
                                link_status = 1
                                Log.error('error',
                                          f'没有接收到kook传回的HELLO包，判断为连接超时，请检查网络或是DNS服务，正在指数回退 {sleep_time}s 后将会重新获取Gateway并连接ws')
                                time.sleep(sleep_time)
                                await add_sleep_time()

                            elif data['s'] == 5 and data['d']['code'] != 0:
                                code = data['d']['code']
                                if code == 40106:
                                    error_txt = 'resume 失败, 缺少参数'
                                elif code == 40107:
                                    error_txt = '当前 session 已过期 (resume 失败, PING 的 sn 无效)'
                                elif code == 40108:
                                    error_txt = '无效的 sn , 或 sn 已经不存在 (resume 失败, PING 的 sn 无效)'
                                else:
                                    error_txt = f'未知错误 code：{code}'

                                Log.error('error',
                                          f'连接已失效，正在指数回退 {sleep_time}s 后将会重新获取Gateway并连接ws，原因：{error_txt}')
                                time.sleep(sleep_time)
                                await add_sleep_time()
                                sn = 1
                                wait_json = []
                                link_status = 1
                                try:
                                    await websocket.close()
                                except:
                                    pass

                            if data['s'] == 0:
                                if wait_json:
                                    if sn == wait_json[0]['sn']:
                                        sn = wait_json[0]['sn'] + 1
                                        if link_status == 3:
                                            pass
                                            await asyncio.gather(process_message(wait_json[0], plugin_list))
                                        del wait_json[0]

                                if sn == data['sn']:
                                    sn = data['sn'] + 1
                                    if link_status == 3:
                                        pass
                                        await asyncio.gather(process_message(data, plugin_list))
                                else:
                                    if data['sn'] > sn:
                                        wait_json.append(data)

                                if sn == 65536:
                                    sn = 1
                        except websockets.ConnectionClosedOK:
                            Log.error('error', f"连接被主机强制关闭准备尝试重连:{traceback.format_exc()}")
                            sn = 1
                            wait_json = []
                            link_status = 1
                            try:
                                await websocket.close()
                            except:
                                pass
                            try:
                                task.cancel()
                            except:
                                pass
                        except Exception as e:
                            sn = 1
                            wait_json = []
                            link_status = 1
                            try:
                                await websocket.close()
                            except:
                                pass
                            try:
                                task.cancel()
                            except:
                                pass
                            Log.error('error', f"框架运行出错:{traceback.format_exc()}")

        except Exception as e:
            Log.error('error', f"框架运行出错:{traceback.format_exc()}")
            sn = 1
            wait_json = []
            link_status = 1
            try:
                await websocket.close()
            except:
                pass
            try:
                task.cancel()
            except:
                pass
