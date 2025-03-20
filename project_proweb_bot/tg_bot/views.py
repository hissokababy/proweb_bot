import json
import requests
import telebot
from tg_bot.credentials import TELEGRAM_API_URL, URL
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from telebot import types

from common.kbds import main_btns_inline_ru, main_btns_inline_uz, main_btns_reply_ru, main_btns_reply_uz

from common.texts import languages

# установка вебхука
def setwebhook(request):
  response = requests.post(TELEGRAM_API_URL + "setWebhook?url=" + URL).json()
  return HttpResponse(f"{response}")

from tg_bot.credentials import TOKEN
# подключение бота
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')


@csrf_exempt
def telegram_bot(request):
  if request.method == 'POST':
    json_string = request.body.decode('utf-8')

    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return HttpResponse('ok')
  else:
    return HttpResponseBadRequest('Bad Request')
  
  
@bot.message_handler(commands=['start',])
def start_message(message: types.Message, language='uz'):
    chat_id = message.chat.id

    bot.send_message(chat_id, 'Вас приветсвует центр современных профессий <b>PROWEB!</b>🤗', reply_markup=main_btns_reply_ru())
    
    bot.send_message(chat_id, languages[language]['welcome'], reply_markup=main_btns_inline_ru())

