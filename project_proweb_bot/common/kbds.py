from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from common.texts import texts


def main_btns_inline(lang, level):
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = texts[lang]['inline_btns'][level]

    btn_lst = []

    for i in buttons:
       button = InlineKeyboardButton(**i)
       btn_lst.append(button)
    
    markup.add(*btn_lst)

    return markup


def main_btns_reply(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = texts[lang]['reply_btns']['main']

    btn_lst = []

    for i in buttons:
       button = KeyboardButton(**i)
       btn_lst.append(button)
    
    markup.add(*btn_lst)
    return markup
