from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from common.texts import texts


def main_btns_inline(lang, level):
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = texts[lang]['inline_btns'][level]

    btn_lst = []

    for i in buttons:
       button = InlineKeyboardButton(text=i['text'], url=i['url'], callback_data=i['callback_data'])
       btn_lst.append(button)
    
    for btn in btn_lst:
        markup.add(btn)

    return markup


def main_btns_reply(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = texts[lang]['reply_btns']['main']

    btn_lst = []

    for i in buttons:
       button = KeyboardButton(text=i['text'], request_contact=i['request_contact'])
       btn_lst.append(button)
    
    for btn in btn_lst:
        markup.add(btn)
    
    return markup
