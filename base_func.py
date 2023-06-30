import vk_api
import random
import time
import requests
import json

from keys import *
from gifs_dict import gifs
from datetime import datetime, timedelta

def vk_auth():
    vk_bot = vk_api.VkApi(token=bot_api_token)
    vk_bot._auth_token()
    vk_bot.get_api()

    vk_chat = vk_api.VkApi(token=stachek_api_token)
    vk_chat._auth_token()
    vk_chat.get_api()

    return vk_bot, vk_chat


def is_admin(user_id):
    if user_id in admin_id:
        return True
    return False


def send_message(vk_bot, chat_peer_id, message=None, attachment=None):
    vk_bot.method("messages.send", {"peer_id": chat_peer_id, 'random_id': get_random_id(),
                                    "message": message, "attachment": attachment})


def get_random_id():
    return random.randint(0, 100000000)


def need_gif(message_text):
    if "плох" == message_text:
        return random.choice(gifs['bad'])
    elif "база" == message_text:
        return random.choice(gifs['based'])
    elif "я занят" == message_text or "я занята" == message_text or "занят" == message_text:
        return random.choice(gifs['busy'])
    elif "пока" == message_text:
        return random.choice(gifs['bye'])
    elif "кринж" == message_text:
        return random.choice(gifs['cringe'])
    elif "факт" == message_text:
        return random.choice(gifs['fact'])
    elif "бесплатно" == message_text:
        return random.choice(gifs['free'])
    elif "гениус" == message_text or "никита воробьев" == message_text:
        return random.choice(gifs['genius'])
    elif "хорош" == message_text:
        return random.choice(gifs['good'])
    elif "иса" == message_text:
        return random.choice(gifs['isa'])
    elif "либерал" == message_text:
        return random.choice(gifs['liberal'])
    elif "много букв" == message_text:
        return random.choice(gifs['many_letters'])
    elif "платно" == message_text:
        return random.choice(gifs['paid'])
    elif "-рейтинг" == message_text:
        return random.choice(gifs['rating_minus'])
    elif "+рейтинг" == message_text:
        return random.choice(gifs['rating_plus'])
    elif "иду" == message_text or "бегу" == message_text:
        return random.choice(gifs['run'])
    elif "торгаш" == message_text:
        return random.choice(gifs['seller'])
    elif "лицо на 0" == message_text:
        return random.choice(gifs['na_nol'])
    elif "что" == message_text:
        return random.choice(gifs['what'])
    return False


def get_random_message():
    messages_to = ["никогда не пиши сюда гениус", "гениус лох", "фу, это же гениус", "ну давай, скинь баян",
                   "кикните гениуса уже"]
    return random.choice(messages_to)


def generate_tag(user_id, user_name):
    user_tag = f"@id{user_id} ({user_name})"
    return user_tag


def get_members_dict(vk_chat):
    chat_members_dict = vk_chat.method("messages.getConversationMembers", {"peer_id": bot_peer_id})
    return chat_members_dict


def remaining_slots(vk_bot, chat_peer_id, max_members, members_for_kick_list):
    if 5 > max_members - len(members_for_kick_list) > 1:
        send_message(vk_bot, chat_peer_id,
                     f"Осталось {max_members - len(members_for_kick_list)} места")
    elif max_members - len(members_for_kick_list) == 1:
        send_message(vk_bot, chat_peer_id,
                     f"Осталось {max_members - len(members_for_kick_list)} место")
    else:
        send_message(vk_bot, chat_peer_id,
                     f"Осталось {max_members - len(members_for_kick_list)} мест")


def kick_preview(vk_bot, vk_chat, chat_peer_id, user_id):
    send_message(vk_bot, chat_peer_id, "Кик через...")
    time.sleep(1)
    send_message(vk_bot, chat_peer_id, "3...")
    time.sleep(1)
    send_message(vk_bot, chat_peer_id, "2...")
    time.sleep(1)
    send_message(vk_bot, chat_peer_id, "1...")
    time.sleep(1)
    kick_user_from_chat(vk_chat, user_id)


def kick_user_from_chat(vk_chat, user_id):
    vk_chat.method("messages.removeChatUser", {"chat_id": int(bot_peer_id) - 2000000000, "member_id": user_id})


def create_jokes():
    jokes_for_genius_file = open('jokes_for_genius.txt', mode="r", encoding="utf-8")
    jokes_for_torg_file = open('jokes_for_torg.txt', mode="r", encoding="utf-8")
    try:
        jokes_for_genius_list = jokes_for_genius_file.read().split("---")
    finally:
        jokes_for_genius_file.close()
    try:
        jokes_for_torg_list = jokes_for_torg_file.read().split("---")
    finally:
        jokes_for_torg_file.close()
    return jokes_for_genius_list, jokes_for_torg_list


def create_members_info(chat_members_dict):
    profiles = chat_members_dict['profiles']
    for profile in profiles:
        print(profile)
        try:
            first_name = profile['first_name']
            last_name = profile['last_name']
            if profile['online_info']['visible']:
                last_online = datetime.fromtimestamp(profile['online_info']['last_seen'])
            else:
                last_online = "*неизвестно*"
            chat_user = f"{first_name} {last_name} был онлайн {last_online}"
            print(chat_user)
        except KeyError:
            print(profile)


def get_user_name_with_id(vk_chat, user_id):
    chat_members_dict = get_members_dict(vk_chat)['profiles']
    for chat_member in chat_members_dict:
        if str(chat_member['id']) == user_id:
            return chat_member['first_name']


def delete_message(vk_chat, messages_id):
    vk_chat.method("messages.delete", {"peer_id": bot_peer_id, "cmids": messages_id, "delete_for_all": 1})


def get_new_invite_link(vk_chat):
    invite_link = vk_chat.method("messages.getInviteLink", {"peer_id": bot_peer_id, "reset": 1})
    return invite_link['link']


def board_create_comment(vk_client_bot, message):
    vk_client_bot.method("board.createComment", {"group_id": stachek_group_id, "topic_id": 48793167, "message": message})


def board_delete_comment(vk_client_bot, comment_id):
    vk_client_bot.method("board.deleteComment", {"group_id": stachek_group_id, "topic_id": 48793167, "comment_id": comment_id})


def board_get_comments(vk_client_bot):
    comments = vk_client_bot.method("board.getComments", {"group_id": stachek_group_id, "topic_id": 48793167})
    return comments['items']


def delete_board_comments(vk_client_bot):
    comments = board_get_comments(vk_client_bot)
    for comment in comments:
        if comment['from_id'] != -206605165:
            board_delete_comment(vk_client_bot, comment['id'])


def get_upload_server(vk_client_bot, group_id, album_id):
    upload_server = vk_client_bot.method("photos.getUploadServer", {"album_id": album_id, "group_id": group_id})
    return upload_server['upload_url']
