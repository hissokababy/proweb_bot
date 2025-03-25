import telebot
from telebot import types

from tg_bot.services.group import add_bot_group, left_bot_group
from tg_bot.models import Group
from tg_bot.bot import bot


@bot.message_handler(chat_types=['supergroup', 'group'], content_types=['new_chat_members', 'group_chat_created'])
def group_add_handler(message: types.Message):
    group = message.chat
    add_bot_group(group)


@bot.message_handler(chat_types=['supergroup', 'group'], content_types=['left_chat_member'])
def group_add_handler(message: types.Message):
    tg_group_id = message.chat.id
    left_bot_group(tg_group_id)
