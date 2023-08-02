import requests
import json


async def get_ws(token_type, token) -> json:
    url = 'https://www.kookapp.cn/api/v3/gateway/index'

    headers = {
        "Authorization": f"{token_type} {token}"
    }

    response = requests.get(url, headers=headers).json()
    return response
