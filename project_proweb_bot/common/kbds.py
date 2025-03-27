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


def admin_panel_btn():
   markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
   btn = KeyboardButton(text='Рассылка в личные чаты пользователей')
   btn1 = KeyboardButton(text='Рассылка в группы студентов')
   return markup.add(btn, btn1)


CONTINUE_BTN = 'Далее'
BACK_TO_MENU_BTN = 'Главное меню ↩️'

def mailing_languages(LANGUAGES):
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text="Все языки")

   langs = [KeyboardButton(text=i) for i in LANGUAGES]

   btn3 = KeyboardButton(text=BACK_TO_MENU_BTN)
   btn4 = KeyboardButton(text=CONTINUE_BTN)

   markup.add(btn)
   markup.add(*langs)
   markup.add(btn3, btn4)
   return markup

def mailing_courses(COURSES):
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text="Все курсы")
   courses = [KeyboardButton(text=i) for i in COURSES]

   btn4 = KeyboardButton(text=BACK_TO_MENU_BTN)
   btn5 = KeyboardButton(text=CONTINUE_BTN)

   markup.add(btn)
   markup.add(*courses)
   markup.add(btn4, btn5)
   return markup



def go_to_menu():
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text=BACK_TO_MENU_BTN)

   markup.add(btn)
   return markup


def go_back_or_mail():
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text=BACK_TO_MENU_BTN)
   btn1 = KeyboardButton(text='Переслать')

   markup.add(btn, btn1)
   return markup