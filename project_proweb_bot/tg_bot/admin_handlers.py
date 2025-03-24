from tg_bot.bot import bot

from telebot import types
from common.texts import texts
from common.kbds import main_btns_inline, main_btns_reply

from tg_bot.utils import admin_confirm, get_user_lang


@bot.callback_query_handler(func=lambda call: call.data == 'confirm')
def callback_handler(call: types.CallbackQuery):

    chat_id = call.message.chat.id
    user_lang = get_user_lang(tg_id=chat_id)

    if call.data == 'confirm':
       bot.send_message(chat_id, 'Вы вошли в админ панель', reply_markup=main_btns_reply(user_lang, 'mailing', row=1))
       admin_confirm(chat_id)


