import json

from API.decorator.command import function_records
from API.api_kook import load_config, KOOKApi
from API.api_log import Log
from plugin_system.plugin_transfer import plugin_transfer


async def process_message(data, plugin_dict):
    kook_token, kook_token_type = load_config()
    kook_api = KOOKApi()

    #############
    #  Objects  #
    #############

    async def kook_user(user_json: json):
        user_id = user_json['id']
        user_username = user_json['username']
        user_nickname = user_json['nickname']
        user_identify_num = user_json['identify_num']
        user_online = user_json['online']
        user_bot = user_json['bot']
        user_status = user_json['status']
        user_avatar_url = user_json['avatar']
        user_vip_avatar_url = user_json['vip_avatar']
        user_roles = user_json['roles']
        return {'id': user_id, 'username': user_username, 'nickname': user_nickname, 'identify_num': user_identify_num,
                'online': user_online, 'bot': user_bot, 'status': user_status, 'avatar': user_avatar_url,
                'vip_avatar': user_vip_avatar_url, 'roles': user_roles}

    async def kook_server_server(guild_json: json):
        server_id = guild_json['id']
        server_name = guild_json['name']
        server_topic = guild_json['topic']
        server_main_id = guild_json['user_id']
        server_icon_url = guild_json['icon']
        server_notify_type = guild_json['notify_type']
        server_region = guild_json['region']
        server_open = guild_json['enable_open']
        server_open_id = guild_json['open_id']
        server_default_channel_id = guild_json['default_channel_id']
        server_welcome_channel_id = guild_json['welcome_channel_id']
        server_roles = guild_json['roles']
        server_channels = guild_json['channels']

    async def kook_channel_json(channel_json: json):
        channel_id = channel_json['id']
        channel_name = channel_json['name']
        channel_creator_id = channel_json['user_id']
        channel_channel_id = channel_json['guild_id']
        channel_topic = channel_json['topic']
        channel_is_category = channel_json['is_category']
        channel_parent_id = channel_json['parent_id']
        channel_level = channel_json['level']
        channel_slow_mode = channel_json['slow_mode']
        channel_type = channel_json['type']
        channel_permission_overwrites = channel_json['permission_overwrites']
        channel_permission_users = channel_json['permission_users']
        channel_permission_sync = channel_json['permission_sync']
        channel_has_password = channel_json['has_password']

    async def kook_quote_json(quote_json: json):
        quote_id = quote_json['id']
        quote_type = quote_json['type']
        quote_content = quote_json['content']
        quote_create_at = quote_json['create_at']
        quote_author = quote_json['author']
        await kook_user(quote_author)

    async def kook_attachments(attachments_json: json):
        attachments_type = attachments_json['type']
        attachments_url = attachments_json['url']
        attachments_file_name = attachments_json['name']
        attachments_file_size = attachments_json['size']

    ##############
    #   Events   #
    ##############

    async def events(events_json: json):
        events_channel_type = events_json['channel_type']
        events_type = events_json['type']
        events_channel_id = events_json['target_id']
        events_author_id = events_json['author_id']
        events_content = data.get("d").get("content", "")
        if events_type == 9:
            events_message = data.get("d", "").get("extra", "").get("kmarkdown", "").get("raw_content", "")
        else:
            events_message = events_content
        events_message_id = events_json['msg_id']
        events_message_timestamp = events_json['msg_timestamp']
        events_nonce = events_json['nonce']
        events_extra = events_json['extra']
        if 'guild_id' in events_extra:
            events_server_id = events_extra['guild_id']
            events_channel_name = events_extra['channel_name']
        else:
            events_server_id = None
            events_channel_name = None
        if 'author' in events_extra:
            events_author = await kook_user(events_extra['author'])
        else:
            events_author = None

        return {'events': {
            'channel_type': events_channel_type, 'type': events_type, 'server_id': events_server_id,
            'author_id': events_author_id, 'content': events_content, 'message': events_message,
            'message_id': events_message_id, 'msg_timestamp': events_message_timestamp, 'nonce': events_nonce,
            'extra': events_extra, 'channel_id': events_channel_id, 'channel_name': events_channel_name},
            'user': events_author
        }

    async def extra_txt(extra_json: json):
        extra_txt_type = extra_json['type']
        extra_txt_channel_id = extra_json['guild_id']
        extra_txt_channel_name = extra_json['channel_name']
        extra_txt_mention = extra_json['mention']
        extra_txt_mention_all = extra_json['mention_all']
        extra_txt_mention_roles = extra_json['mention_roles']
        extra_txt_mention_here = extra_json['mention_here']
        extra_txt_author = extra_json['author']
        await kook_user(extra_txt_author)

    async def extra_card(extra_json: json):
        extra_card_type = extra_json['type']
        extra_card_value = extra_json['body']['value']
        extra_card_message_id = extra_json['body']['msg_id']
        extra_card_user_id = extra_json['body']['user_id']
        extra_card_server_id = extra_json['body']['guild_id']
        extra_card_channel_type = extra_json['body']['channel_type']
        extra_card_channel_id = extra_json['body']['target_id']
        extra_card_user_info = extra_json['body']['user_info']
        user_json = await kook_user(extra_card_user_info)
        return {
            'card': {'type': extra_card_type, 'server_id': extra_card_server_id,
                     'value': extra_card_value, 'message_id': extra_card_message_id,
                     'user_id': extra_card_user_id, 'channel_type': extra_card_channel_type,
                     'channel_id': extra_card_channel_id, 'user_info': extra_card_user_info}, 'user': user_json}

    async def extra_exit_server(kook_data: json):
        extra_exit_server_user_id = kook_data['extra']['body']['user_id']
        extra_exit_server_exit_at = kook_data['extra']['body']['exited_at']
        extra_exit_server_channel_id = kook_data['target_id']
        return {'exit_server': {'user_id': extra_exit_server_user_id, 'exit_at': extra_exit_server_exit_at,
                                'server_id': extra_exit_server_channel_id}}

    async def extra_join_server(kook_data: json):
        extra_join_server_user_id = kook_data['extra']['body']['user_id']
        extra_join_server_join_at = kook_data['extra']['body']['joined_at']
        extra_exit_server_channel_id = kook_data['target_id']
        return {'join_server': {'user_id': extra_join_server_user_id, 'join_at': extra_join_server_join_at,
                                'server_id': extra_exit_server_channel_id}}

    async def extra_self_exit_server(kook_data: json):
        extra_self_exit_server_server_id = kook_data['extra']['body']['guild_id']
        return {
            'self_exit_server': {'server_id': extra_self_exit_server_server_id}
        }

    async def extra_self_join_server(kook_data: json):
        extra_self_join_server_server_id = kook_data['extra']['body']['guild_id']
        return {
            'self_join_server': {'server_id': extra_self_join_server_server_id}
        }

    events_data = await events(data['d'])

    Log.accepted_info(events_data)

    # 传入原始json
    await plugin_transfer('kook_json', plugin_dict, data)

    if data['s'] == 0:
        # 调用插件
        if events_data['events']['type'] in [1, 9]:
            # 文字+KMD
            await plugin_transfer('txt_message', plugin_dict, events_data)
        elif events_data['events']['type'] == 2:
            # 图片
            await plugin_transfer('image_message', plugin_dict, events_data)
        elif events_data['events']['type'] == 3:
            # 视频
            await plugin_transfer('video_message', plugin_dict, events_data)
        elif events_data['events']['type'] == 4:
            # 文件
            await plugin_transfer('file_message', plugin_dict, events_data)
        elif events_data['events']['type'] == 8:
            # 音频
            await plugin_transfer('audio_message', plugin_dict, events_data)
        elif events_data['events']['type'] == 10:
            # 卡片
            await plugin_transfer('card_message', plugin_dict, events_data)
        elif events_data['events']['type'] == 255:
            # 系统
            await plugin_transfer('system_message', plugin_dict, events_data)

        # 有用户加入服务器
        if events_data['events']['channel_type'] == 'GROUP' and events_data['events']['type'] == 255 and \
                events_data['events']['extra']['type'] == 'joined_guild':
            join_json = await extra_join_server(data['d'])
            await plugin_transfer('user_join_server', plugin_dict, join_json)

        # 有用户退出服务器
        if events_data['events']['channel_type'] == 'GROUP' and events_data['events']['type'] == 255 and \
                events_data['events']['extra']['type'] == 'exited_guild':
            exit_json = await extra_exit_server(data['d'])
            await plugin_transfer('user_exit_server', plugin_dict, exit_json)

        # 自己加入服务器
        if events_data['events']['channel_type'] == 'PERSON' and events_data['events']['type'] == 255 and \
                events_data['events']['extra']['type'] == 'self_joined_guild':
            join_json = await extra_self_join_server(data['d'])
            await plugin_transfer('user_self_join_server', plugin_dict, join_json)

        # 自己退出服务器
        if events_data['events']['channel_type'] == 'PERSON' and events_data['events']['type'] == 255 and \
                events_data['events']['extra']['type'] == 'self_exited_guild':
            exit_json = await extra_self_exit_server(data['d'])
            await plugin_transfer('user_self_exit_server', plugin_dict, exit_json)

        # 卡片消息按钮点击
        if events_data['events']['channel_type'] == 'PERSON' and events_data['events']['type'] == 255 and \
                events_data['events']['extra']['type'] == 'message_btn_click':
            plugin_data_card = await extra_card(data['d']['extra'])
            await plugin_transfer('message_button_click', plugin_dict, plugin_data_card)

        # 调用注册过的命令
        for func in function_records:
            if function_records[func]['substring_bool']:
                if len(events_data['events']['message']) > function_records[func]['substring_num'] and \
                        events_data['events']['message'][:function_records[func]['substring_num']] == str(
                    function_records[func]['command']):
                    await function_records[func]['function'](events_data, events_data['events']['message'].split(
                        function_records[func]['command'])[1])
            else:
                if events_data['events']['message'] == str(function_records[func]['command']):
                    await function_records[func]['function'](events_data)
