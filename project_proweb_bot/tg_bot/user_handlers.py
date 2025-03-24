from tg_bot.credentials import CONTACT_GROUP_ID
from tg_bot.bot import bot

from telebot import types
from common.texts import texts
from common.kbds import main_btns_inline, main_btns_reply

from tg_bot.utils import get_user_lang, is_admin, save_user, set_user_lang

from tg_bot.admin_handlers import admin_panel

@bot.message_handler(commands=['start',])
def start_message(message: types.Message):
    chat_id = message.chat.id
    save_user(tg_user=message.from_user)
    
    if is_admin(chat_id):
         admin_panel(message)

    else:
      user_lang = get_user_lang(tg_id=message.from_user.id)

      bot.send_message(chat_id, texts[user_lang]['welcome']['hello_msg'], reply_markup=main_btns_reply(user_lang, 'main'))
      
      bot.send_message(chat_id, texts[user_lang]['welcome']['greeting'], reply_markup=main_btns_inline(user_lang, 'main'))


@bot.message_handler(content_types=['text', 'contact'])
def set_language_or_back(message: types.Message):
    if message.text == "O'zbek tili 🇺🇿" or message.text == "Bosh sahifaga ↩️":
       set_user_lang(message.from_user.id, 'uz')
       start_message(message)

    elif message.text == "Русский язык 🇷🇺" or message.text == "На главную ↩️":
      set_user_lang(message.from_user.id, 'ru')
      start_message(message)

    elif message.contact:
      contact = message.contact
      bot.send_message(CONTACT_GROUP_ID, contact.phone_number)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: types.CallbackQuery):

    chat_id = call.message.chat.id
    user_lang = get_user_lang(tg_id=call.message.chat.id)

    if call.data == 'konkursi':
       bot.send_message(chat_id, texts[user_lang]['konkursi']['text'])
    
    elif call.data == 'base_course':
       bot.send_message(chat_id, texts[user_lang]['base_course'], reply_markup=main_btns_inline(user_lang, 'base_course'))

    elif call.data == 'comment':
       bot.send_message(chat_id, texts[user_lang]['wishes'], reply_markup=main_btns_inline(user_lang, 'wishes'))

    elif call.data == 'complaint':
       bot.send_message(chat_id, texts[user_lang]['complaints'])

    elif call.data == 'rules':
       bot.send_message(chat_id, texts[user_lang]['rules'])
