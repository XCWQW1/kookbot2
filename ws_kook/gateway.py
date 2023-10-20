import aiohttp
import json


async def get_ws(token_type, token) -> json:
    url = 'https://www.kookapp.cn/api/v3/gateway/index'

    headers = {
        "Authorization": f"{token_type} {token}",
        "X-Rate-Limit-Limit": "5",
        "X-Rate-Limit-Remaining": "0",
        "X-Rate-Limit-Reset": "14",
        "X-Rate-Limit-Bucket": "user/info",
        "X-Rate-Limit-Global": ""
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers) as response:
                response = await response.json()
                return response
        except aiohttp.ClientError:
            # 访问失败，再尝试一次
            try:
                async with session.post(url, headers=headers) as response:
                    response = await response.json()
                    return response
            except aiohttp.ClientError:
                # 第二次访问失败
                raise '访问Gateway失败'
