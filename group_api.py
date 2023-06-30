import vk_api

from keys import stachek_api_token, stachek_group_id, stachek_peer_id


def get_group_members_list():
    group_members_dict = vk_group_bot.method("groups.getMembers", {"group_id": stachek_group_id, "fields": ["bdate"]})
    print(group_members_dict)


if __name__ == "__main__":
    vk_group_bot = vk_api.VkApi(token=stachek_api_token)
    vk_group_bot._auth_token()
    vk_group_bot.get_api()
    get_group_members_list()
