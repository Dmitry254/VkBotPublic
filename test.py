import random
import time

import schedule
import traceback

from threading import Thread
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from base_func import *


def listen_poll():
    global vk_bot, vk_chat
    try:
        for event in longpoll.listen():
            print(event)
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object.message
                user_id = str(message['from_id'])
                peer_id = str(message['peer_id'])
                message_id = message['conversation_message_id']
                if user_id not in mute_list.keys():
                    if peer_id == chat_peer_id:
                        catch_message(message, user_id)
                        catch_user(message, user_id)
                    if peer_id == chat_peer_id and user_id in admin_id:
                        catch_admin_message(message, user_id)
                    # if peer_id == chat_peer_id and 'action' in event.object['message'].keys():
                    #     if 'chat_invite_user' in event.object['message']['action']['type']:
                    #         send_welcome_message(message, user_id)
                else:
                    delete_message(vk_chat, message_id)
    except:
        traceback.print_exc()
        time.sleep(5)
        vk_bot, vk_chat = vk_auth()


def catch_message(message, user_id):
    message_text = message['text'].lower()
    gif_message = need_gif(message_text)
    if "лох дня" in message_text:
        loh_of_the_day()
    if "лапочка дня" in message_text:
        lapochka_of_the_day()
    if "лапочка вечера" in message_text:
        lapochka_of_the_evening()
    if "числитель" in message_text or "знаменатель" in message_text:
        even_or_odd_week()
    if (("белье" in message_text or "бельё" in message_text or "постельн" in message_text)
            and ("выд" in message_text or "мен" in message_text)) or message_text == "белье" or message_text == "бельё":
        change_bedclothes()
    if ("номер" in message_text or "телефон" in message_text)\
            and ("вахт" in message_text or "коменд" in message_text or " ов" in message_text
                                    or "ов " in message_text or "поликл" in message_text
                                    or "больниц" in message_text or "стоматолог" in message_text):
        send_phone_numbers()
    if ("оплат" in message_text or "квитанц" in message_text) \
            and ("когда" in message_text or "получ" in message_text or "взят" in message_text or "по " in message_text
                    or " по" in message_text):
        send_pay_timetable()
    if ("справк" in message_text) and ("обучен" in message_text or "учишься" in message_text):
        certificate_of_studying()
    if "печать" in message_text or "печата" in message_text or "печата" in message_text\
            or "ксерокопия" in message_text or "отсканить" in message_text:
        best_printing()
    if "погода" == message_text:
        send_weather_info()
    if ("кури" in message_text or "курени" in message_text or "сига" in message_text or "сижка" in message_text\
        or "сигарет" in message_text or "сиги" in message_text or "дымить" in message_text or "сижку" in message_text\
        or "вейп" in message_text or "жижу" in message_text or "жижа" in message_text or "одноразк" in message_text)\
        and "!магазин" not in message_text:
        no_smoke()
    if "!магазин" in message_text:
        if len(message_text) > 8:
            shop_list(message_text.split(' ')[1])
        else:
            shop_list('')
    if "!такси" in message_text and "!такси список" != message_text:
        create_taxi_group(message_text, user_id)
    if "!такси список" == message_text:
        chech_taxi_groups(message_text, user_id)
    if "анекдот про внука" in message_text or "анекдот про деда" in message_text:
        grandson_joke(user_id)
    if "анекдот про лоха" in message_text:
        send_joke_for_genius(user_id)
    if "анекдот про торгаша" in message_text:
        send_joke_for_torg(user_id)
    if "+" == message_text:
        plus_message()
    if gif_message:
        send_message(vk_bot, chat_peer_id, attachment=gif_message)
    if len(message_text) > 200:
        send_message(vk_bot, chat_peer_id, attachment=random.choice(gifs['many_letters']))


def catch_admin_message(message, user_id):
    message_text = message['text'].lower()
    if "конкурс на кик" == message_text:
        kick_competition_thread = Thread(target=kick_competition)
        try:
            kick_competition_thread.start()
        except ZeroDivisionError:
            kick_competition_thread.join()
    if "конкурс на отчисление" == message_text:
        otchislenie_competition_thread = Thread(target=otchislenie_competition)
        try:
            otchislenie_competition_thread.start()
        except ZeroDivisionError:
            otchislenie_competition_thread.join()
    if "игра в слова" == message_text:
        game_words_thread = Thread(target=game_words)
        try:
            game_words_thread.start()
        except ZeroDivisionError:
            game_words_thread.join()
    if "!мут" in message_text:
        add_user_to_mute_list(message, message_text)
    if "!размут" in message_text:
        delete_user_from_mute_list(message)


def catch_user(message, user_id):
    message_text = message['text'].lower()
    message_id = message['conversation_message_id']
    if user_id == "264965602":  # Данилов
        if "конкурс на еду" == message_text:
            food_competition()
    if user_id == "163962491":  # Ушанов
        pass
    if user_id == "79646275":  # Бутятин
        pass
    if user_id == "224377131":  # Гениус
        if random.choices([True, False], weights=[1, 99])[0]:
            send_message(vk_bot, chat_peer_id,
                         "Никита Воробьев более известен как Гениус Фигиус* (*Гениус Фигиус с 15.04.2022 запрещен на территории Стачек 5)")
    if user_id == "288986143":  # Самохина
        if "конкурс на еду" == message_text:
            food_competition()


def loh_of_the_day():
    global first_name_loh, last_name_loh
    if not first_name_loh:
        of_the_day_file = open('of_the_day.txt', mode="r", encoding="utf-8")
        for line in of_the_day_file:
            if "loh:" in line:
                loh_names = line.split(',')
                first_name_loh = loh_names[1]
                last_name_loh = loh_names[2]
        of_the_day_file.close()
    send_message(vk_bot, chat_peer_id, f"Лох {datetime.now().strftime('%d.%m.%Y')} {first_name_loh} {last_name_loh}")


def lapochka_of_the_day():
    global first_name_lapochka, last_name_lapochka
    if not first_name_lapochka:
        of_the_day_file = open('of_the_day.txt', mode="r", encoding="utf-8")
        for line in of_the_day_file:
            if "lapochka:" in line:
                lapochka_names = line.split(',')
                first_name_lapochka = lapochka_names[1]
                last_name_lapochka = lapochka_names[2]
        of_the_day_file.close()
    send_message(vk_bot, chat_peer_id,
                 f"Лапочка {datetime.now().strftime('%d.%m.%Y')} {first_name_lapochka} {last_name_lapochka}")


def lapochka_of_the_evening():
    if 24 > datetime.now().hour > 15:
        send_message(vk_bot, chat_peer_id, f"Лапочка сегодняшнего вечера Юлия Чичина")


def choose_loh_of_the_day():
    global id_loh, first_name_loh, last_name_loh
    loh_list = [{'id': "381865182", 'first_name': "Alexey", 'last_name': "Yamamoto"}]
    loh = random.choice(loh_list)
    id_loh = loh['id']
    first_name_loh = loh['first_name']
    last_name_loh = loh['last_name']
    send_message(vk_bot, chat_peer_id,
                 f"Лох {datetime.now().strftime('%d.%m.%Y')} {generate_tag(id_loh, f'{first_name_loh} {last_name_loh}')}")
    return f"loh: {id_loh},{first_name_loh},{last_name_loh}"


def choose_lapochka_of_the_day():
    global id_lapochka, first_name_lapochka, last_name_lapochka
    chat_members_dict = get_members_dict(vk_chat)['profiles']
    lapochka = random.choice(chat_members_dict)
    id_lapochka = lapochka['id']
    first_name_lapochka = lapochka['first_name']
    last_name_lapochka = lapochka['last_name']
    send_message(vk_bot, chat_peer_id,
                 f"Лапочка {datetime.now().strftime('%d.%m.%Y')} {generate_tag(id_lapochka, f'{first_name_lapochka} {last_name_lapochka}')}")
    return f"lapochka: {id_lapochka},{first_name_lapochka},{last_name_lapochka}"


def even_or_odd_week():
    week_number = int(datetime.now().isocalendar()[1])
    next_monday = (datetime.now() + timedelta(days=-datetime.now().weekday(), weeks=1)).date().day
    if week_number % 2 == 0:
        week_now = f"Сейчас знаменатель, числитель начнется с {next_monday} числа"
    else:
        week_now = f"Сейчас числитель, знаменатель начнется с {next_monday} числа"
    send_message(vk_bot, chat_peer_id, week_now)


def change_bedclothes():
    send_message(vk_bot, chat_peer_id, "Обычно белье меняют в понедельник, вторник и четверг с 13:00 до 16:30")


def certificate_of_studying():
    send_message(vk_bot, chat_peer_id, "Если ты студент ИВТ, то чтобы заказать справку об обучении зайди в 430 кабинет в понедельник или четверг с 10 до 14 или пиши на почту gureevalv@gumrf.ru")


def grandson_joke(user_id):
    global new_joke_time
    full_joke = ""
    joke = ""
    joke_list = "".split(" ")
    if new_joke_time > datetime.now():
        if is_admin(user_id):
            while joke_list:
                word_number = random.randint(0, len(joke_list) - 1)
                full_joke += f"{joke_list[word_number]} "
                joke_list.pop(word_number)
            send_message(vk_bot, chat_peer_id, full_joke)
            if full_joke == joke:
                send_message(vk_bot, chat_peer_id, "Поздравляю, ты смог собрать анекдот")
        return False
    while joke_list:
        word_number = random.randint(0, len(joke_list) - 1)
        full_joke += f"{joke_list[word_number]} "
        joke_list.pop(word_number)
    send_message(vk_bot, chat_peer_id, full_joke)
    new_joke_time = datetime.now() + timedelta(minutes=5)
    if full_joke == joke:
        send_message(vk_bot, chat_peer_id, "Поздравляю, ты смог собрать анекдот")


def plus_message():
    messages_plus = ["Че складываем?", "-", "Крест на могилу?"]
    send_message(vk_bot, chat_peer_id, random.choice(messages_plus))


def send_joke_for_genius(user_id):
    global new_joke_time
    if new_joke_time > datetime.now():
        if is_admin(user_id):
            send_message(vk_bot, chat_peer_id, random.choice(jokes_for_genius_list))
        return False
    send_message(vk_bot, chat_peer_id, random.choice(jokes_for_genius_list))
    new_joke_time = datetime.now() + timedelta(minutes=5)


def send_joke_for_torg(user_id):
    global new_joke_time
    if new_joke_time > datetime.now():
        if is_admin(user_id):
            send_message(vk_bot, chat_peer_id, random.choice(jokes_for_torg_list))
        return False
    send_message(vk_bot, chat_peer_id, random.choice(jokes_for_torg_list))
    new_joke_time = datetime.now() + timedelta(minutes=5)


def send_phone_numbers():
    phone_numbers = "Коменда: 89119426610\nВахта: 88127489786\nПоликлиника №23: 88122467320" \
                    "\nСтоматология №10 (пер. Огородный 4): 88127867720" \
                    "\nСтоматология №10 (ул. Маршала Говорова 32): 88127867198"
    send_message(vk_bot, chat_peer_id, phone_numbers)


def send_pay_timetable():
    pay_timetable = 'Все вопросы по оплате только на эту страницу https://vk.com/id644742916\n' \
                    'Шаблон сообщения для получения квитанции:\n' \
                    '"Привет, нужна квитанция за март, Иванов И.И., комната 111"\n' \
                    'В комментарии к оплате обязательно указывать "За проживание в общежитии"'
    send_message(vk_bot, chat_peer_id, pay_timetable)


def best_printing():
    printers_list = "Печатают они:\nhttps://vk.com/id155803529\nhttps://vk.com/id398514663 - цветное тоже\nhttps://vk.com/yuliaqssss\nhttps://vk.com/sailinyt - цветное тоже\n" \
                    "https://vk.com/liza_sev"
    send_message(vk_bot, chat_peer_id, printers_list)


def shop_list(product):
    shop_text = ""
    torgashi = [
        [["жижа", "doge", "нарва"], "https://vk.com/sanyamaestro - Продает жижу"],
        [["жижа", "жижка", "одноразки"], "https://vk.com/lopytm - Husky prem и elf bar на 4к затяг. Телега: https://t.me/donelfbar"],
        [["жопа"], "https://vk.com/dorylory - Продает свою жопу"]
    ]
    if product:
        for torgash in torgashi:
            if product in torgash[0]:
                shop_text += f"{torgash[1]}\n\n"
    else:
        for torgash in torgashi:
            shop_text += f"{torgash[1]}\n\n"
    if not shop_text:
        shop_text = "Товара нет"
    send_message(vk_bot, chat_peer_id, shop_text)


def no_smoke():
    no_smoke_text = ["Победи никотиновый вред – скажи сигаретам нет",
                     "Ради здоровья и экономии денег замени сигарету на березовый веник",
                     "Не испорть себе портрет – откажись от сигарет",
                     "Скажет вам любой рентген, что табак – канцероген",
                     "Табачок покупаешь – дату смерти приближаешь",
                     "Здоровый образ жизни моден, от курения стань свободен",
                     "Каждая сигарета – это выстрел в себя, причем без промаха",
                     "Вдыхая дым – губишь себя, выдыхая – других",
                     "«Вред курения очевиден. От курения тупеешь.» © В. Гёте",
                     "«Курящая женщина вульгарна» © Л.Н. Толстой.",
                     "«Курение ослабляет силу мысли и делает неясным её выражение» © Л.Н. Толстой.",
                     "«Бросать курить легко. Я сам бросал тысячу раз» © Марк Твен ",
                     "«Сигара может послужить хорошим суррогатом мысли» © Артур Шопенгауэр",
                     "«Табак приносит вред телу, разрушает разум, оглупляет целые нации» © О. Бальзак",
                     "«Всякий курильщик должен знать и помнить, что он отравляет не только себя, но и других» © Н.А. Семашко",
                     "«Отравление никотином через курение подтачивает у человека и физику и психику» © Н.А. Семашко",
                     "«Сигарета - это бикфордов шнур, на одном конце которого огонёк, а на другом – дурак» © Джордж Бернард Шоу",
                     "«Курители сигар - это мои естественные враги» © В.Г. Белинский",
                     "«Если бы я не курил, то прожил бы ещё 10-15 лет» © С.П. Боткин",
                     "«Болезни происходят из образа жизни, частью от воздуха, который мы вводим в себя и в котором мы живем» © Гиппократ",
                     "«После того, как совершенно бросил курить, у меня уже не бывает мрачного и тревожного настроения» © В. Шекспир",
                     "«Привычка – тиран людей» © В. Шекспир",
                     "«Побороть дурные привычки легче сегодня, чем завтра» © Конфуций",
                     "«Человек часто сам себе злейший враг» © Цицерон"]
    send_message(vk_bot, chat_peer_id, random.choice(no_smoke_text), random.choice(gifs['smoke']))


def send_welcome_message(message, user_id):
    user_name = get_user_name_with_id(vk_chat, user_id)
    user_tag = generate_tag(user_id, user_name)
    if random.choices([True, False], weights=[95, 5])[0]:
        welcome_message_list = [f"Привет {user_tag}", f"Приветствую {user_tag}", f"Добро пожаловать {user_tag}",
                                f"Здравствуй {user_tag}", f"{user_tag} добро пожаловать", f"Здарова {user_tag}",
                                f"Хеллоу {user_tag}", f"Че надо {user_tag}? Хотя раз уже тут, то",
                                f"Бонжур {user_tag}", f"Салам {user_tag}", f"Салют {user_tag}", f"Хола {user_tag}"]
        welcome_message = f"{random.choice(welcome_message_list)}\n[https://vk.com/@gumrf.narva-zaselenie|Читай этот гайд]"
        send_message(vk_bot, chat_peer_id, welcome_message)
    else:
        welcome_message = f'Привет {user_tag}. У тебя есть 3 минуты, чтобы скинуть смешной анекдот в беседу ' \
                          f'или тебя ждет кик. Время пошло.'
        send_message(vk_bot, chat_peer_id, welcome_message)


def get_random_message():
    messages_to = ["никогда не пиши сюда гениус", "гениус лох", "фу, это же гениус", "ну давай, скинь баян",
                   "кикните гениуса уже"]
    return random.choice(messages_to)


def send_morning_info():
    week_number = int(datetime.now().isocalendar()[1])
    if week_number % 2 == 0:
        week_now = f"Сегодня знаменатель"
    else:
        week_now = f"Сегодня числитель"
    text = f"{week_now}\n{weather_text}"
    send_message(vk_bot, chat_peer_id, text)


def add_user_to_mute_list(message, message_text):
    muted_user_id = str(message['reply_message']['from_id'])
    print(message_text)
    if len(message_text) > 5:
        mute_duration = int(message_text[5:])
        unmute_time = datetime.now() + timedelta(minutes=mute_duration)
    else:
        mute_duration = 5
        unmute_time = datetime.now() + timedelta(minutes=mute_duration)
    if muted_user_id not in admin_id:
        mute_list.update({muted_user_id: unmute_time})
        user_name = get_user_name_with_id(vk_chat, muted_user_id)
        user_tag = generate_tag(muted_user_id, user_name)
        send_message(vk_bot, chat_peer_id, f"{user_tag} в муте на {mute_duration} минут")


def delete_user_from_mute_list(message):
    muted_user_id = str(message['reply_message']['from_id'])
    user_name = get_user_name_with_id(vk_chat, muted_user_id)
    user_tag = generate_tag(muted_user_id, user_name)
    for muted_user in mute_list.keys():
        if muted_user_id in muted_user:
            mute_list.pop(muted_user)
            send_message(vk_bot, chat_peer_id, f"{user_tag} размучен")
            return True
    send_message(vk_bot, chat_peer_id, f"{user_name} не был муте")


def check_mute_times():
    unmute_list = []
    for muted_user in mute_list.keys():
        if datetime.now() > mute_list[muted_user]:
            unmute_list.append(muted_user)
    for muted_user in unmute_list:
        user_name = get_user_name_with_id(vk_chat, muted_user)
        user_tag = generate_tag(muted_user, user_name)
        mute_list.pop(muted_user)
        send_message(vk_bot, chat_peer_id, f"{user_tag} размучен")


def create_of_the_day_file(of_the_day_list):
    of_the_day_file = open('of_the_day.txt', mode="w", encoding="utf-8")
    try:
        for name in of_the_day_list:
            of_the_day_file.write(name + '\n')
    finally:
        of_the_day_file.close()


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


def weather_info():
    global weather_text
    weather_values = {
        "clear": "ясно",
        "partly-cloudy": "малооблачно",
        "cloudy": "облачно с прояснениями",
        "overcast": "пасмурно",
        "drizzle": "морось",
        "light-rain": "небольшой дождь",
        "rain": "дождь",
        "moderate-rain": "умеренно сильный дождь",
        "heavy-rain": "сильный дождь",
        "continuous-heavy-rain": " длительный сильный дождь",
        "showers": "ливень",
        "wet-snow": "дождь со снегом",
        "light-snow": "небольшой снег",
        "snow": "снег",
        "snow-showers": "снегопад",
        "hail": "град",
        "thunderstorm": "гроза",
        "thunderstorm-with-rain": "дождь с грозой",
        "thunderstorm-with-hail": "гроза с градом"
    }
    url = "https://api.weather.yandex.ru/v2/informers?lat=59.901459&lon=30.272354&lang=ru_RU"
    headers = {
        "X-Yandex-API-Key": "9d5a20f4-4ae5-42a8-a31d-628f103850e3"
    }
    req = requests.get(url, headers=headers)
    weather = json.loads(req.text)['fact']
    weather_text = f"Сейчас {weather_values[weather['condition']]}\nТемпература {weather['temp']}°C, " \
                   f"скорость ветра {weather['wind_speed']} м/с, влажность {weather['humidity']}%"
    return weather_text


def send_weather_info():
    send_message(vk_bot, chat_peer_id, weather_text)


def food_competition():
    members_for_competition_list = []
    max_members = 15
    competition_rules = 'Напиши "Участвую" для участия в конкурсе на еду'
    send_message(vk_bot, chat_peer_id, competition_rules)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message
            user_id = str(message['from_id'])
            peer_id = str(message['peer_id'])
            if peer_id == chat_peer_id:
                message_text = message['text'].lower()
                if "отменить конкурс" == message_text and user_id == "288986143":
                    send_message(vk_bot, chat_peer_id, "Конкурс отменен")
                    raise ZeroDivisionError
                if "участвую" == message_text and len(members_for_competition_list) < max_members:
                    if user_id not in members_for_competition_list:
                        members_for_competition_list.append(user_id)
                        if len(members_for_competition_list) == max_members:
                            send_message(vk_bot, chat_peer_id, "Выбираю победителя")
                            time.sleep(5)
                            winner_user_id = random.choice(members_for_competition_list)
                            winner_user_name = get_user_name_with_id(vk_chat, winner_user_id)
                            send_message(vk_bot, chat_peer_id,
                                         f"Бесплатно поест сегодня {generate_tag(winner_user_id, winner_user_name)}")
                            raise ZeroDivisionError
                        else:
                            remaining_slots(vk_bot, chat_peer_id, max_members, members_for_competition_list)


def kick_competition():
    members_for_competition_list = []
    max_members = 15
    competition_rules = 'Напиши "Участвую" для участия в конкурсе на кик'
    send_message(vk_bot, chat_peer_id, competition_rules)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message
            user_id = str(message['from_id'])
            peer_id = str(message['peer_id'])
            if peer_id == chat_peer_id:
                message_text = message['text'].lower()
                if "отменить конкурс" == message_text and is_admin(user_id):
                    send_message(vk_bot, chat_peer_id, "Конкурс отменен")
                    raise ZeroDivisionError
                if "участвую" == message_text and len(members_for_competition_list) < max_members:
                    if user_id not in members_for_competition_list:
                        members_for_competition_list.append(user_id)
                        if len(members_for_competition_list) == max_members:
                            send_message(vk_bot, chat_peer_id, "Выбираю победителя")
                            time.sleep(5)
                            winner_user_id = random.choice(members_for_competition_list)
                            kick_preview(vk_bot, vk_chat, chat_peer_id, winner_user_id)
                            raise ZeroDivisionError
                        else:
                            remaining_slots(vk_bot, chat_peer_id, max_members, members_for_competition_list)


def otchislenie_competition():
    members_for_competition_list = []
    max_members = 15
    competition_rules = 'Напиши "Участвую" для участия в конкурсе на отчисление. Конкурс проводится совместно с деканатом, поэтому принимай участие на свой страх и риск.'
    send_message(vk_bot, chat_peer_id, competition_rules)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message
            user_id = str(message['from_id'])
            peer_id = str(message['peer_id'])
            if peer_id == chat_peer_id:
                message_text = message['text'].lower()
                if "отменить конкурс" == message_text and is_admin(user_id):
                    send_message(vk_bot, chat_peer_id, "Конкурс отменен")
                    raise ZeroDivisionError
                if "выбрать победителя" == message_text and is_admin(user_id):
                    send_message(vk_bot, chat_peer_id, "Выбираю победителя")
                    time.sleep(5)
                    user_tag = generate_tag("224377131", "Гениус")
                    send_message(vk_bot, chat_peer_id, f"{user_tag} будет отчислен. Соболезнуем.")
                    raise ZeroDivisionError
                if "участвую" == message_text and len(members_for_competition_list) < max_members:
                    if user_id not in members_for_competition_list:
                        members_for_competition_list.append(user_id)
                        if len(members_for_competition_list) == max_members:
                            send_message(vk_bot, chat_peer_id, "Выбираю победителя")
                            time.sleep(5)
                            user_tag = generate_tag("224377131", "Гениус")
                            send_message(vk_bot, chat_peer_id, f"{user_tag} будет отчислен. Соболезнуем.")
                            raise ZeroDivisionError
                        else:
                            remaining_slots(vk_bot, chat_peer_id, max_members, members_for_competition_list)


def search_kicked_member():
    for offset in [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]:
        chat_history = \
        vk_chat.method("messages.getHistory", {"peer_id": int(bot_peer_id), "count": 200, "offset": offset})['items']
        for message in chat_history:
            user_in_chat = False
            if "action" in message.keys():
                if message['action']['type'] == "chat_kick_user":
                    kicked_user = message['action']['member_id']
                    chat_members = get_members_dict(vk_chat)['items']
                    for chat_member in chat_members:
                        if chat_member['member_id'] == kicked_user:
                            user_in_chat = True
                        if message['from_id'] != -206605165:
                            user_in_chat = True
                    if not user_in_chat:
                        group_members = \
                        vk_chat.method("groups.getMembers", {"group_id": stachek_group_id, "fields": ["bdate"]})[
                            'items']
                        for group_member in group_members:
                            if group_member['id'] == kicked_user:
                                vk_bot.method("messages.send", {"user_id": 163962491, 'random_id': get_random_id(),
                                                                "message": f"{generate_tag(kicked_user, group_member['first_name'])} ждет возвращения"})
    return False


def game_words():
    gamers_dict = {}
    bad_letters = ["ъ", "ь", "ы"]
    first_words = ["База", "Ушанов", "Общежитие", "Кринж", "Кокраз", "Стачек", "Пожар", "Гениус", "Кот", "Вася"]
    used_words = []
    game_rules = 'Правила: пишите сообщение, которое начинается с последней буквы предыдущего, ' \
                 'можно использовать любые слова или фразы, повторяться слова не должны, ограничение на ход 15 секунд, ' \
                 'проверяются сообщения идущие друг за другом. если последняя буква "ь", "ъ" или "ы", ' \
                 'то считается предыдущая буква не из этого списка.\n\n' \
                 'Как только истечет время или игрок напишет слово, ' \
                 'которое не начинается с последней буквы предыдущего слова или уже было использовано, ' \
                 'то случайный из всех принявших участие игроков будет в муте.\n\n' \
                 'Победит тот, кто написал больше всего ' \
                 'подходящих слов или фраз и его точно не замутит'
    send_message(vk_bot, chat_peer_id, game_rules)
    first_word = random.choice(first_words)
    last_letter = first_word[-1]
    send_message(vk_bot, chat_peer_id, f"Первое слово - {first_word}")
    time_last_word = datetime.now() + timedelta(minutes=5)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message
            user_id = str(message['from_id'])
            peer_id = str(message['peer_id'])
            if peer_id == chat_peer_id:
                message_text = message['text'].lower()
                first_letter = message_text[0]
                if first_letter == last_letter and message_text not in used_words:
                    if user_id not in gamers_dict.keys():
                        gamers_dict.update({user_id: 1})
                    else:
                        gamers_dict.update({user_id: gamers_dict[user_id] + 1})
                    used_words.append(message_text)
                    last_letter = message_text[-1]
                    if last_letter in bad_letters:
                        last_letter_index = -1
                        while last_letter in bad_letters:
                            last_letter_index -= 1
                            last_letter = message_text[last_letter_index]
                    if time_last_word + timedelta(seconds=15) > datetime.now():
                        time_last_word = datetime.now()
                    else:
                        end_game_words_mute("time", gamers_dict)
                else:
                    end_game_words_mute("word", gamers_dict)


def end_game_words_kick(end_type, gamers_dict):
    if end_type == "time":
        send_message(vk_bot, chat_peer_id, "Время вышло. Игра окончена")
    elif end_type == "word":
        send_message(vk_bot, chat_peer_id, "Неверное слово. Игра окончена")
    winner_id = max(gamers_dict, key=gamers_dict.get)
    winner_name = get_user_name_with_id(vk_chat, winner_id)
    time.sleep(3)
    send_message(vk_bot, chat_peer_id, f"Победил {generate_tag(winner_id, winner_name)} - "
                                       f"{gamers_dict[winner_id]} слов")
    print(gamers_dict)
    gamers_dict.pop(winner_id)
    time.sleep(3)
    loser_id = random.choice(list(gamers_dict))
    loser_name = get_user_name_with_id(vk_chat, loser_id)
    send_message(vk_bot, chat_peer_id, f"А кикнут будет {generate_tag(loser_id, loser_name)}. "
                                       f"У тебя есть 20 секунд на прощание")
    time.sleep(20)
    kick_user_from_chat(vk_chat, loser_id)
    time.sleep(3)
    send_message(vk_bot, chat_peer_id, "Всем спасибо за участие", random.choice(gifs['good']))
    print(gamers_dict)
    raise ZeroDivisionError


def end_game_words_mute(end_type, gamers_dict):
    if end_type == "time":
        send_message(vk_bot, chat_peer_id, "Время вышло. Игра окончена")
    elif end_type == "word":
        send_message(vk_bot, chat_peer_id, "Неверное слово. Игра окончена")
    winner_id = max(gamers_dict, key=gamers_dict.get)
    winner_name = get_user_name_with_id(vk_chat, winner_id)
    time.sleep(3)
    send_message(vk_bot, chat_peer_id, f"Победил {generate_tag(winner_id, winner_name)} - "
                                       f"{gamers_dict[winner_id]} слов")
    print(gamers_dict)
    gamers_dict.pop(winner_id)
    time.sleep(3)
    loser_id = random.choice(list(gamers_dict))
    loser_name = get_user_name_with_id(vk_chat, loser_id)
    send_message(vk_bot, chat_peer_id, f"А в муте будет {generate_tag(loser_id, loser_name)}. "
                                       f"У тебя есть 20 секунд на прощание")
    time.sleep(20)
    if loser_id not in admin_id:
        mute_duration = random.randint(10, 100)
        unmute_time = datetime.now() + timedelta(minutes=mute_duration)
        mute_list.update({loser_id: unmute_time})
        user_tag = generate_tag(loser_id, loser_name)
        send_message(vk_bot, chat_peer_id, f"{user_tag} в муте на {mute_duration} минут")
    time.sleep(3)
    send_message(vk_bot, chat_peer_id, "Всем спасибо за участие", random.choice(gifs['good']))
    print(gamers_dict)
    raise ZeroDivisionError


def chech_taxi_groups(message, user_id):
    global taxi_groups_dict
    text = ""
    print(taxi_groups_dict)
    for taxi_key in taxi_groups_dict:
        if taxi_groups_dict[taxi_key][2] - len(taxi_groups_dict[taxi_key][0]) == 1:
            text = f"Есть такси, где нужен 1 человек"
        elif taxi_groups_dict[taxi_key][2] - len(taxi_groups_dict[taxi_key][0]) == 2:
            text = f"Есть такси, где нужно еще 2 человека"
        elif taxi_groups_dict[taxi_key][2] - len(taxi_groups_dict[taxi_key][0]) == 3:
            text = f"Есть такси, где нужно еще 3 человека"
        elif taxi_groups_dict[taxi_key][2] - len(taxi_groups_dict[taxi_key][0]) == 4:
            text = f"Есть такси, где нужно еще 4 человека"
        send_message(vk_bot, chat_peer_id, text)
    if not text:
        send_message(vk_bot, chat_peer_id, "Такси никто не ищет")


def create_taxi_group(message, user_id):
    global taxi_groups_dict
    user_name = get_user_name_with_id(vk_chat, user_id)
    text = ""
    group_max = 3
    members_number = 1
    approach_group_exist = False
    min_need_group = 10
    if message == "!такси 0":
        taxi_key = user_id
        for item in taxi_groups_dict[taxi_key][0]:
            text += f"{generate_tag(item[0], item[1])}, "
        taxi_groups_dict.pop(taxi_key)
        text = text[:-2]
        text += " ваше такси расформировано"
        send_message(vk_bot, chat_peer_id, text)
        return 0
    if message == "!такси":
        group_max = 3
        members_number = 1
    elif "!такси +" in message:
        members_number = int(message[7:])
        if members_number > 4:
            send_message(vk_bot, chat_peer_id, "Максимум 4 человека")
            return 0
        if members_number < 1:
            send_message(vk_bot, chat_peer_id, "И кто тогда поедет?")
            return 0
    elif "!такси " in message:
        group_max = int(message[6:])
        if group_max > 4:
            send_message(vk_bot, chat_peer_id, "Максимум 4 места")
            return 0
        if group_max < 1:
            send_message(vk_bot, chat_peer_id, "И кто тогда поедет?")
            return 0
    for taxi_key_i in taxi_groups_dict:
        taxi_group = taxi_groups_dict[taxi_key_i][0]
        min_need_group_key = taxi_groups_dict[taxi_key_i][2] - len(taxi_groups_dict[taxi_key_i][0]) - members_number
        if min_need_group_key > 0:
            if min_need_group > min_need_group_key:
                min_need_group = min_need_group_key
                taxi_key = taxi_key_i
                approach_group_exist = True
    if approach_group_exist:
        taxi_group = taxi_groups_dict[taxi_key][0]
        taxi_group.append([user_id, user_name])
        taxi_groups_dict.update({taxi_key: [taxi_group, taxi_groups_dict[taxi_key][1], taxi_groups_dict[taxi_key][2] - members_number + 1]})
        approach_group_exist = True
    if not approach_group_exist:
        taxi_groups_dict.update({user_id: [[], datetime.now()  + timedelta(minutes=15), group_max + 2 - members_number]})
        taxi_key = user_id
        taxi_group = taxi_groups_dict[taxi_key][0]
        taxi_group.append([user_id, user_name])
        text = "Вы создали новую группу"
        send_message(vk_bot, chat_peer_id, text)
        text = ""
    if taxi_groups_dict[taxi_key][2] - len(taxi_group) == 1:
        text = f"Вам нужен еще 1 человек"
    elif taxi_groups_dict[taxi_key][2] - len(taxi_group) == 2:
        text = f"Вам нужно еще 2 человека"
    elif taxi_groups_dict[taxi_key][2] - len(taxi_group) == 3:
        text = f"Вам нужно еще 3 человека"
    elif taxi_groups_dict[taxi_key][2] - len(taxi_group) == 4:
        text = f"Вам нужно еще 4 человека"
    elif taxi_groups_dict[taxi_key][2] - len(taxi_group) == 0:
        for item in taxi_groups_dict[taxi_key][0]:
            text += f"{generate_tag(item[0], item[1])}, "
        taxi_groups_dict.pop(taxi_key)
        text = text[:-2]
        text += " ваше такси набралось"
    send_message(vk_bot, chat_peer_id, text)
    print(taxi_groups_dict)
    return 0


def check_taxi_times():
    taxi_delete_list = []
    for key in taxi_groups_dict.keys():
        if taxi_groups_dict[key][1] < datetime.now():
            taxi_delete_list.append(key)
    for taxi_delete in taxi_delete_list:
        text = ""
        for item in taxi_groups_dict[taxi_delete][0]:
            text += f"{generate_tag(item[0], item[1])}, "
        taxi_groups_dict.pop(taxi_delete)
        text = text[:-2]
        text += " ваше такси не набралось за 15 минут"
        send_message(vk_bot, chat_peer_id, text)


def do_schedule():
    try:
        while True:
            schedule.run_pending()
            time.sleep(25)
    except:
        traceback.print_exc()


def job_list():
    global mute_list
    lapochka_info = choose_lapochka_of_the_day()
    loh_info = choose_loh_of_the_day()
    create_of_the_day_file([lapochka_info, loh_info])
    search_kicked_member()
    mute_list = {}


schedule.every().day.at("09:00").do(send_morning_info)
schedule.every().day.at("12:00").do(job_list)
try:
    schedule.every(1).minutes.do(check_mute_times)
    schedule.every(1).minutes.do(check_taxi_times)
    schedule.every(1).hours.do(weather_info)
except:
    traceback.print_exc()


if __name__ == "__main__":
    weather_text = weather_info()
    chat_peer_id = test_peer_id  # изменить на stachek_peer_id
    new_joke_time = datetime.now() - timedelta(minutes=5)
    jokes_for_genius_list, jokes_for_torg_list = create_jokes()
    id_lapochka, first_name_lapochka, last_name_lapochka = "", "", ""
    id_loh, first_name_loh, last_name_loh = "", "", ""
    mute_list = {}
    taxi_groups_dict = {}

    vk_bot, vk_chat = vk_auth()

    schedule_thread = Thread(target=do_schedule)
    schedule_thread.start()

    longpoll = VkBotLongPoll(vk_bot, bot_group_id)

    while True:
        try:
            listen_poll()
        except:
            traceback.print_exc()
            time.sleep(5)
            vk_bot, vk_chat = vk_auth()
