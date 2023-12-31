import asyncio
import os
import signal
import sys
import time

from API.api_kook import KOOKApi
from API.api_log import LogSP
from init.main_init import main_init
from ws_kook.ws import connect_to_kook_server
from art import text2art
from colorama import init, Fore, Style

# 初始化colorama
init()


async def kook_bot():
    await connect_to_kook_server()


async def main():
    current_time = time.time()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
    version = 'v1.2.5'
    version_text = f"{Fore.LIGHTBLACK_EX}{now_time}{Fore.RESET} {Fore.GREEN}[版本]{Style.RESET_ALL}" + ' ' + '当前框架运行的版本：' + Fore.GREEN + version + Style.RESET_ALL
    print(version_text)
    art_text = text2art('XCBOT')

    # 拆分艺术字的每一行，并在每行前面添加当前时间
    art_lines = art_text.split('\n')[:5]
    art_with_time = [f"{Fore.LIGHTBLACK_EX}{now_time}{Fore.RESET}{Fore.GREEN} [初始]" + ' ' + line for line in art_lines]

    # 将带有时间的每行重新组合成一个字符串
    result = '\n'.join(art_with_time)

    print(result + Style.RESET_ALL)
    await main_init()
    await kook_bot()


async def off():
    await KOOKApi().offline_user()


def signal_handler(sig, frame):
    asyncio.create_task(off())
    current_time_1 = time.time()
    now_time_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time_1))
    logs = f"{Fore.LIGHTBLACK_EX}{now_time_1}{Fore.RESET} [信息关闭] 框架已关闭"
    LogSP.print_log(logs)
    LogSP.save_log(logs)
    pid = os.getpid()
    os.kill(pid, signal.SIGKILL)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    asyncio.run(main())


'''
                    _ooOoo_
                   o8888888o
                   88" . "88
                   (| -_- |)
                    O\ = /O
                ____/`---'\____
              .   ' \\| |// `.
               / \\||| : |||// \
             / _||||| -:- |||||- \
               | | \\\ - /// | |
             | \_| ''\---/'' | |
              \ .-\__ `-` ___/-. /
           ___`. .' /--.--\ `. . __
        ."" '< `.___\_<|>_/___.' >'"".
        | | : `- \`.;`\ _ /`;.`/ - ` : | |
         \ \ `-. \_ __\ /__ _/ .-` / /
 ======`-.____`-.___\_____/___.-`____.-'======
                    `=---='

 .............................................
          佛祖保佑             永无BUG
'''