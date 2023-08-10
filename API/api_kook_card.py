import json

from API.api_kook import KOOKApi

sdk = KOOKApi()


class Card:
    async def send_img(self, url: str, channel_id: int) -> str:
        json_img = [
            {
                "type": "card",
                "theme": "secondary",
                "size": "lg",
                "modules": [
                    {
                        "type": "container",
                        "elements": [
                            {
                                "type": "image",
                                "src": url
                            }
                        ]
                    }
                ]
            }
        ]

        return await sdk.send_channel_msg(json.dumps(json_img), 10, channel_id)

    async def send_msg(self, msg: str, channel_id: int) -> str:
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
                            "content": msg
                        }
                    }
                ]
            }
        ]

        return await sdk.send_channel_msg(json.dumps(json_data), 10, channel_id)

    async def update_msg(self, msg_id: str, msg: str, channel_message_id: str) -> str:
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
                            "content": msg
                        }
                    }
                ]
            }
        ]

        return await sdk.update_message(msg_id, json.dumps(json_data), quote=channel_message_id)

    async def update_img(self, msg_id: str, url: str, channel_message_id: str) -> str:
        json_img = [
            {
                "type": "card",
                "theme": "secondary",
                "size": "lg",
                "modules": [
                    {
                        "type": "container",
                        "elements": [
                            {
                                "type": "image",
                                "src": url
                            }
                        ]
                    }
                ]
            }
        ]

        return await sdk.update_message(msg_id, json.dumps(json_img), quote=channel_message_id)
