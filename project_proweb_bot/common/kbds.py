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


MAILING = 'Рассылать'
FORWARDING = 'Переслать'

def mail_or_forward():
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text=MAILING)
   btn1 = KeyboardButton(text=FORWARDING)
   return markup.add(btn, btn1)


PRIVATE_MAILING_BTN = 'Рассылка в личные чаты пользователей'
GROUP_MAILING_BTN = 'Рассылка в группы студентов'

PRIVATE_FORWARDING_BTN = 'Переслать в личные чаты пользователей'
GROUP_FORWARDING_BTN = 'Переслать в группы студентов'

def mailing_type_btns():
   markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
   btn = KeyboardButton(text=PRIVATE_MAILING_BTN)
   btn1 = KeyboardButton(text=GROUP_MAILING_BTN)
   btn2 = KeyboardButton(text=BACK_TO_MENU_BTN)
   
   return markup.add(btn, btn1, btn2)


def forwarding_type_btns():
   markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
   btn = KeyboardButton(text=PRIVATE_FORWARDING_BTN)
   btn1 = KeyboardButton(text=GROUP_FORWARDING_BTN)
   btn2 = KeyboardButton(text=BACK_TO_MENU_BTN)
   
   return markup.add(btn, btn1, btn2)


CONTINUE_BTN = 'Далее'
BACK_TO_MENU_BTN = 'Главное меню ↩️'
ALL_GROUP_LANGUAGES = 'Все языки групп'
ALL_USERS_LANGUAGES = 'Все языки пользователей'
ALL_COURSES = 'Все курсы'
MAILING_BTN = 'Рассылать'
SEND_POST = 'Отправить'

def mailing_languages(LANGUAGES, groups=None):
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

   if not groups:
      btn = KeyboardButton(text=ALL_USERS_LANGUAGES)
   else:
      btn = KeyboardButton(text=ALL_GROUP_LANGUAGES)

   langs = [KeyboardButton(text=i) for i in LANGUAGES]

   btn3 = KeyboardButton(text=BACK_TO_MENU_BTN)
   btn4 = KeyboardButton(text=CONTINUE_BTN)

   markup.add(btn)
   markup.add(*langs)
   markup.add(btn3, btn4)
   return markup

def mailing_courses(COURSES):
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text=ALL_COURSES)
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
   btn1 = KeyboardButton(text=SEND_POST)
   
   markup.add(btn1)
   markup.add(btn)
   return markup


PIN_BTN = 'Закрепить пост'
DELETE_BTN = 'Удалить пост'
UNPIN_POST_BTN = 'Открепить пост'

def pin_or_delete_btns(post_id):
   markup = InlineKeyboardMarkup(row_width=2)
   btn = InlineKeyboardButton(text=PIN_BTN, callback_data=f'post_pin_{post_id}')
   btn1 = InlineKeyboardButton(text=DELETE_BTN, callback_data=f'post_delete_{post_id}')
   
   markup.add(btn, btn1)
   return markup


def unpin_or_delete_btns(post_id):
   markup = InlineKeyboardMarkup(row_width=2)
   btn = InlineKeyboardButton(text=UNPIN_POST_BTN, callback_data=f'post_unpin_{post_id}')
   btn1 = InlineKeyboardButton(text=DELETE_BTN, callback_data=f'post_delete_{post_id}')
   
   markup.add(btn, btn1)
   return markup


def confirm_delete(post_id):
   markup = InlineKeyboardMarkup(row_width=2)
   btn = InlineKeyboardButton(text='Да, удалить', callback_data=f'delete_yes_{post_id}')
   btn1 = InlineKeyboardButton(text='Нет, не удалять', callback_data=f'delete_no_{post_id}')
   
   markup.add(btn, btn1)
   return markup



