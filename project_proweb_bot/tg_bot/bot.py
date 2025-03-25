from tg_bot.credentials import TOKEN
import telebot
from telebot.storage import StateMemoryStorage
from telebot.states.sync.middleware import StateMiddleware


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage, parse_mode='HTML', use_class_middlewares=True)

bot.setup_middleware(StateMiddleware(bot))