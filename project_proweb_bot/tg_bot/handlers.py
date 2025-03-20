import telebot

from common.texts import texts_ru, texts_uz
from common.kbds import main_btns_inline_ru, main_btns_reply_ru, main_btns_inline_uz, main_btns_reply_uz

from tg_bot.credentials import TOKEN

from tg_bot.models import User
# подключение бота
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')


# обработчики
def handle_update(update):
    update_text = update['message']['text']
    if update_text == '/start':
      start_message(update)

    elif update_text == 'На главную ↩️':
      start_message(update)

    # elif update_text == "O'zbek tili 🇺🇿":
    #     tg_user = update['message']['from']['id']
        

@bot.message_handler(commands=['start',])
def start_message(message: telebot.types.Message):
    chat_id = message['message']['chat']['id']

    text = texts_ru['welcome']
    
    bot.send_message(chat_id, 'Вас приветсвует центр современных профессий <b>PROWEB!</b>🤗', reply_markup=main_btns_reply_ru())
    bot.send_message(chat_id, text, reply_markup=main_btns_inline_ru())

    # сохранение пользователя в бд
    tg_user = message['message']['from']
    tg_id = tg_user['id']

    username = ''
    if 'username' in tg_user:
        username = tg_user['username']

    user = User.objects.filter(tg_id=tg_id).first()

    if not user:
        User.objects.create(tg_id=tg_id, username=username)    

