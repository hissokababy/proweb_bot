from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from enum import Enum

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


# class syntax
class Btns(Enum):
   MAILING = 'Рассылать'
   FORWARDING = 'Переслать'
   PRIVATE_MAILING_BTN = 'Рассылка в личные чаты пользователей'
   GROUP_MAILING_BTN = 'Рассылка в группы студентов'
   PRIVATE_FORWARDING_BTN = 'Переслать в личные чаты пользователей'
   GROUP_FORWARDING_BTN = 'Переслать в группы студентов'
   CONTINUE_BTN = 'Далее'
   BACK_TO_MENU_BTN = 'Главное меню ↩️'
   ALL_GROUP_LANGUAGES = 'Все языки'
   ALL_USERS_LANGUAGES = 'Все языки пользователей'
   ALL_COURSES = 'Все курсы'
   MAILING_BTN = 'Рассылать'
   SEND_POST = 'Отправить'
   PIN_BTN = 'Закрепить пост'
   DELETE_BTN = 'Удалить пост'
   UNPIN_POST_BTN = 'Открепить пост'


def mail_or_forward():
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text=Btns.MAILING.value)
   btn1 = KeyboardButton(text=Btns.FORWARDING.value)
   return markup.add(btn, btn1)




def mailing_type_btns():
   markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
   btn = KeyboardButton(text=Btns.PRIVATE_MAILING_BTN.value)
   btn1 = KeyboardButton(text=Btns.GROUP_MAILING_BTN.value)
   btn2 = KeyboardButton(text=Btns.BACK_TO_MENU_BTN.value)
   
   return markup.add(btn, btn1, btn2)


def forwarding_type_btns():
   markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
   btn = KeyboardButton(text=Btns.PRIVATE_FORWARDING_BTN.value)
   btn1 = KeyboardButton(text=Btns.GROUP_FORWARDING_BTN.value)
   btn2 = KeyboardButton(text=Btns.BACK_TO_MENU_BTN.value)
   
   return markup.add(btn, btn1, btn2)




def mailing_languages(LANGUAGES, groups=None):
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

   if not groups:
      btn = KeyboardButton(text=Btns.ALL_USERS_LANGUAGES.value)
   else:
      btn = KeyboardButton(text=Btns.ALL_GROUP_LANGUAGES.value)

   langs = [KeyboardButton(text=i) for i in LANGUAGES]

   btn3 = KeyboardButton(text=Btns.BACK_TO_MENU_BTN.value)
   btn4 = KeyboardButton(text=Btns.CONTINUE_BTN.value)

   markup.add(btn)
   markup.add(*langs)
   markup.add(btn3, btn4)
   return markup

def mailing_courses(COURSES):
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text=Btns.ALL_COURSES.value)
   courses = [KeyboardButton(text=i) for i in COURSES]

   btn4 = KeyboardButton(text=Btns.BACK_TO_MENU_BTN.value)
   btn5 = KeyboardButton(text=Btns.CONTINUE_BTN.value)

   markup.add(btn)
   markup.add(*courses)
   markup.add(btn4, btn5)
   return markup



def go_to_menu():
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text=Btns.BACK_TO_MENU_BTN.value)

   markup.add(btn)
   return markup


def go_back_or_mail():
   markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
   btn = KeyboardButton(text=Btns.BACK_TO_MENU_BTN.value)
   btn1 = KeyboardButton(text=Btns.SEND_POST.value)
   
   markup.add(btn1)
   markup.add(btn)
   return markup




def pin_or_delete_btns(post_id):
   markup = InlineKeyboardMarkup(row_width=2)
   btn = InlineKeyboardButton(text=Btns.PIN_BTN.value, callback_data=f'post_pin_{post_id}')
   btn1 = InlineKeyboardButton(text=Btns.DELETE_BTN.value, callback_data=f'post_delete_{post_id}')
   
   markup.add(btn, btn1)
   return markup


def unpin_or_delete_btns(post_id):
   markup = InlineKeyboardMarkup(row_width=2)
   btn = InlineKeyboardButton(text=Btns.UNPIN_POST_BTN.value, callback_data=f'post_unpin_{post_id}')
   btn1 = InlineKeyboardButton(text=Btns.DELETE_BTN.value, callback_data=f'post_delete_{post_id}')
   
   markup.add(btn, btn1)
   return markup


def confirm_delete(post_id):
   markup = InlineKeyboardMarkup(row_width=2)
   btn = InlineKeyboardButton(text='Да, удалить', callback_data=f'delete_yes_{post_id}')
   btn1 = InlineKeyboardButton(text='Нет, не удалять', callback_data=f'delete_no_{post_id}')
   
   markup.add(btn, btn1)
   return markup



