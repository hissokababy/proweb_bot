from tg_bot.credentials import TOKEN
import telebot
from telebot.storage import StateMemoryStorage
from telebot.states.sync.middleware import StateMiddleware
from telebot import custom_filters

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage, parse_mode='HTML', use_class_middlewares=True)



bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())

# necessary for state parameter in handlers.
from telebot.states.sync.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))