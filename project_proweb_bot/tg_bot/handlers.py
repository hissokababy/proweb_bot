from requests import request
import telebot
from telebot import types
from common.texts import languages
from common.kbds import main_btns_inline_ru, main_btns_reply_ru, main_btns_inline_uz, main_btns_reply_uz

from tg_bot.credentials import TOKEN

from tg_bot.models import User
# подключение бота
from tg_bot.handlers import bot

# главный обработчик апдейта
# def handle_update(update):

    # print(update['callback_query'])

    # update_text = update['message']['text']

    # if update_text == '/start':
    #   start_message(update)

    # elif update_text == 'На главную ↩️':
    #   start_message(update)

    # elif update_text == 'Bosh sahifaga ↩️':
    #   start_message(update, language='uz')

    # elif update_text == "O'zbek tili 🇺🇿":
    #     tg_id = update['message']['from']['id']

    #     user, created = User.objects.get_or_create(tg_id=tg_id)

    #     if not created:
    #        user.language_selected = 'uz'
    #        user.save()
    #     start_message(update, language='uz')


    # elif update_text == "Русский язык 🇷🇺":
    #     tg_id = update['message']['from']['id']

    #     user, created = User.objects.get_or_create(tg_id=tg_id)

    #     if not created:
    #        user.language_selected = 'ru'
    #        user.save()
    #     start_message(update, language='ru')


# обработчики
# @bot.message_handler(commands=['start',])
# def start_message(message: types.Message, language='ru'):
#     chat_id = message.chat.id

#     bot.send_message(chat_id, 'Вас приветсвует центр современных профессий <b>PROWEB!</b>🤗', reply_markup=main_btns_reply_ru())
    
#     bot.send_message(chat_id, languages[language]['welcome'], reply_markup=main_btns_inline_ru())

    # elif language == 'uz':
    #     text = texts_uz['welcome']
        
    #     bot.send_message(chat_id, '<b>PROWEB</b> zamonaviy kasblar markaziga xush kelibsiz!🤗', reply_markup=main_btns_reply_uz())
    #     bot.send_message(chat_id, text, reply_markup=main_btns_inline_uz())


    # # сохранение пользователя в бд
    # tg_user = message['message']['from']
    # tg_id = tg_user['id']

    # username = ''
    # if 'username' in tg_user:
    #     username = tg_user['username']

    # user = User.objects.filter(tg_id=tg_id).first()

    # if not user:
    #     User.objects.create(tg_id=tg_id, username=username)    


# @bot.callback_query_handler(func=lambda callback: True)
# def konkurs_callback(callback: types.CallbackQuery):
#     if callback.data == 'konkursi':
#        bot.send_message(callback.message.chat.id, 'получил колбек')