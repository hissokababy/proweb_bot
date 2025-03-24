import telebot

from tg_bot.credentials import TOKEN
# подключение бота
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

