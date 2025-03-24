from tg_bot.bot import bot

from tg_bot.models import UserAdmin

from telebot import types
from common.texts import texts
from common.kbds import main_btns_inline, main_btns_reply

from tg_bot.utils import admin_confirm, get_user_lang, is_admin


@bot.message_handler(func=lambda message: message.text == 'Да, подтвеждаю ✅')
def admin_panel(message: types.Message):

    chat_id = message.chat.id
    user_lang = get_user_lang(tg_id=chat_id)

    bot.send_message(chat_id, 'Админ панель', reply_markup=main_btns_reply(user_lang, 'mailing', row=1))
    admin_confirm(chat_id)


from telebot.storage import StateMemoryStorage
from telebot.states import State, StatesGroup

state_storage = StateMemoryStorage()

# рассылка в личные чаты
@bot.message_handler(func=lambda message: message.text == 'Рассылка в личные чаты пользователей')
def private_mailing(message: types.Message):
    chat_id = message.chat.id

    if is_admin(chat_id):
        bot.send_message(chat_id, '2121')


class GroupMailing(StatesGroup):
    language = State()


# рассылка в группы
@bot.message_handler(func=lambda message: message.text == 'Рассылка в группы студентов' or message.text == 'Talabalar guruhlariga yuborish')
def private_mailing(message: types.Message):
    chat_id = message.chat.id

    if is_admin(chat_id):
        bot.send_message(chat_id, 'рассылка в группы')

