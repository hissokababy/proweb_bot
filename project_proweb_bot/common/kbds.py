from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from common.texts import texts

def main_btns_inline(lang, level, row=2):
    markup = InlineKeyboardMarkup(row_width=row)

    buttons = texts[lang]['inline_btns'][level]

    btn_lst = []

    for i in buttons:
       button = InlineKeyboardButton(**i)
       btn_lst.append(button)
    
    markup.add(*btn_lst)

    return markup


def main_btns_reply(lang, level, row=2):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row)

    buttons = texts[lang]['reply_btns'][level]

    btn_lst = []

    for i in buttons:
       button = KeyboardButton(**i)
       btn_lst.append(button)
    
    markup.add(*btn_lst)
    return markup


def admin_confirm_btn():
   markup = InlineKeyboardMarkup(row_width=1)
   btn = InlineKeyboardButton(text='Да, подтверждаю ✅', callback_data='confirm')
   return markup.add(btn)


def admin_panel_btn():
   markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
   btn = KeyboardButton(text='Рассылка в личные чаты пользователей')
   btn1 = KeyboardButton(text='Рассылка в группы студентов')
   return markup.add(btn, btn1)


def mailing_languages():
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text="Все языки")
   btn1 = KeyboardButton(text='Русский 🇷🇺')
   btn2 = KeyboardButton(text="O'zbek tili 🇺🇿")
   btn3 = KeyboardButton(text='Главное меню ↩️')
   btn4 = KeyboardButton(text='Далее')

   markup.add(btn)
   markup.add(btn1, btn2)
   markup.add(btn3, btn4)
   return markup

def mailing_courses():
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text="Все курсы")
   btn1 = KeyboardButton(text='PYTHON')
   btn2 = KeyboardButton(text="Web Programming")
   btn3 = KeyboardButton(text="Pro Design")
   btn4 = KeyboardButton(text='Главное меню ↩️')
   btn5 = KeyboardButton(text='Далее')

   markup.add(btn)
   markup.add(btn1, btn2, btn3)
   markup.add(btn4, btn5)
   return markup

