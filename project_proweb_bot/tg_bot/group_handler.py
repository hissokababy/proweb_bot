import telebot
from telebot import types

from tg_bot.services.group import add_bot_group, left_bot_group
from tg_bot.models import Group
from tg_bot.bot import bot


@bot.message_handler(chat_types=['supergroup', 'group'], content_types=['new_chat_members', 'group_chat_created', 'migrate_to_chat_id'])
def group_add_handler(message: types.Message):
    if not message.migrate_to_chat_id:

        group = message.chat
        add_bot_group(group)

    else:
        from_id = message.chat.id
        to_id = message.migrate_to_chat_id
        
        group = Group.objects.filter(tg_id=from_id).first()
        group.tg_id = to_id
        group.save()


@bot.message_handler(chat_types=['supergroup', 'group'], content_types=['left_chat_member'])
def group_left_handler(message: types.Message):
    if message.left_chat_member.is_bot == True:
        left_bot_group(message.chat.id)
