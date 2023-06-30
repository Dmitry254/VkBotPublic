import vk_api
import random

from datetime import datetime, timedelta
from keys import stachek_api_token, stachek_group_id, stachek_peer_id, bot_peer_id, bot_api_token, client_api
from base_func import generate_tag, get_random_id


def get_group_members_list():
    group_members_dict = vk_group_bot.method("groups.getMembers", {"group_id": stachek_group_id, "fields": ["bdate"]})['items']
    print(group_members_dict)
    for group_member in group_members_dict:
        member_birthday = ""
        if 'bdate' in group_member.keys():
            if group_member['bdate'].count('.') == 1:
                member_birthday = datetime.strptime(group_member['bdate'], "%d.%m").date().strftime('%d-%m')
            elif group_member['bdate'].count('.') > 1:
                member_birthday = datetime.strptime(group_member['bdate'], "%d.%m.%Y").date().strftime('%d-%m')
        if member_birthday == datetime.now().date().strftime('%d-%m'):
            print(group_member)
            print(member_birthday)


def get_members_dict():
    chat_members_dict = vk_group_bot.method("messages.getConversationMembers", {"peer_id": bot_peer_id})
    return chat_members_dict


def add_user_to_chat(user_id):
    add_user = vk_group_bot.method("messages.addChatUser", {"chat_id ": int(bot_peer_id) - 2000000000, "user_id": user_id})
    print(add_user)
    return add_user


def search_kicked_member():
    for offset in [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]:
        chat_history = vk_chat.method("messages.getHistory", {"peer_id": int(bot_peer_id), "count": 200, "offset": offset})['items']
        for message in chat_history:
            user_in_chat = False
            if "action" in message.keys():
                if message['action']['type'] == "chat_kick_user":
                    print(message)
                    kicked_user = message['action']['member_id']
                    chat_members = get_members_dict()['items']
                    for chat_member in chat_members:
                        if chat_member['member_id'] == kicked_user:
                            user_in_chat = True
                        if message['from_id'] != -206605165:
                            user_in_chat = True
                    if not user_in_chat:
                        group_members = vk_group_bot.method("groups.getMembers", {"group_id": stachek_group_id, "fields": ["bdate"]})['items']
                        for group_member in group_members:
                            if group_member['id'] == kicked_user:
                                # vk_bot.method("messages.send", {"user_id": 163962491, 'random_id': get_random_id(),
                                #                                 "message": f"{generate_tag(kicked_user, group_member['first_name'])} ждет возвращения {generate_tag(163962491, 'Кирилл')}"})
                                # print(kicked_user)
                                print(kicked_user)


def get_user_name_with_id(user_id):
    chat_members_dict = get_members_dict()['profiles']
    for chat_member in chat_members_dict:
        if str(chat_member['id']) == user_id:
            return chat_member['first_name']


def delete_message(messages_id):
    vk_chat.method("messages.delete", {"peer_id": bot_peer_id, "cmids": messages_id, "delete_for_all": 1})


def get_new_invite_link():
    invite_link = vk_chat.method("messages.getInviteLink", {"peer_id": bot_peer_id, "reset": 1})
    return invite_link['link']


def kick_user_from_chat(vk_chat, user_id):
    vk_chat.method("messages.removeChatUser", {"chat_id": int(bot_peer_id) - 2000000000, "member_id": user_id})


if __name__ == "__main__":
    vk_group_bot = vk_api.VkApi(token=stachek_api_token)
    vk_group_bot._auth_token()
    vk_group_bot.get_api()

    vk_chat = vk_api.VkApi(token=stachek_api_token)
    vk_chat._auth_token()
    vk_chat.get_api()

    vk_bot = vk_api.VkApi(token=bot_api_token)
    vk_bot._auth_token()
    vk_bot.get_api()

    kick_user_from_chat(vk_chat, 232813508)
