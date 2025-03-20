from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# КНОПКИ НА РУССКОМ
def main_btns_inline_ru():
    markup = InlineKeyboardMarkup(row_width=2)
    
    btn = InlineKeyboardButton(text='Тех. поддержка', url='t.me/itsmylifestyle')
    btn1 = InlineKeyboardButton(text='Коворкинг', url='t.me/proweb_coworking')
    btn2 = InlineKeyboardButton(text='Конкурсы🎉', url='t.me/proweb_coworking')
    btn3 = InlineKeyboardButton(text='Посетить сайт', url='proweb.uz')
    btn4 = InlineKeyboardButton(text='Базовый курс', url='t.me/proweb_coworking')
    btn5 = InlineKeyboardButton(text='Оставить отзыв', url='t.me/proweb_coworking')
    btn6 = InlineKeyboardButton(text='Правила обучния', url='t.me/proweb_coworking')
    markup.add(btn, btn1, btn2, btn3,
               btn4, btn5, btn6)
    

    return markup


def main_btns_reply_ru():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn = KeyboardButton(text='На главную ↩️')
    btn1 = InlineKeyboardButton(text="O'zbek tili 🇺🇿")
    btn2 = KeyboardButton(text='Поделится контактом', request_contact=True)

    markup.add(btn, btn1, btn2)
    
    return markup


# КНОПКИ НА УЗБЕКСКОМ
def main_btns_inline_uz():
    markup = InlineKeyboardMarkup(row_width=2)
    
    btn = InlineKeyboardButton(text='Texnik yoram', url='t.me/itsmylifestyle')
    btn1 = InlineKeyboardButton(text='Kovorking', url='t.me/proweb_coworking')
    btn2 = InlineKeyboardButton(text='Tanlovlar🎉', url='t.me/proweb_coworking')
    btn3 = InlineKeyboardButton(text='Saytga tashrif buyurish', url='proweb.uz/uz')
    btn4 = InlineKeyboardButton(text='Kompyuter asoslari', url='t.me/proweb_coworking')
    btn5 = InlineKeyboardButton(text='Sharh qoldirish', url='t.me/proweb_coworking')
    btn6 = InlineKeyboardButton(text="O'qish qoidalari", url='t.me/proweb_coworking')
    markup.add(btn, btn1, btn2, btn3,
               btn4, btn5, btn6)
    
    return markup


def main_btns_reply_uz():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn = KeyboardButton(text='Bosh sahifaga ↩️')
    btn1 = InlineKeyboardButton(text="Русский язык 🇷🇺")
    btn2 = KeyboardButton(text='Kontakt bilan ulashing', request_contact=True)

    markup.add(btn, btn1, btn2)
    
    return markup


