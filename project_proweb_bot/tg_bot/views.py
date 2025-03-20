import json
import requests
from tg_bot.credentials import TELEGRAM_API_URL, URL
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from common.texts import texts
# подключение бота
import telebot
from tg_bot.credentials import TOKEN

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# установка вебхука
def setwebhook(request):
  response = requests.post(TELEGRAM_API_URL + "setWebhook?url=" + URL).json()
  return HttpResponse(f"{response}")


@csrf_exempt
def telegram_bot(request):
  if request.method == 'POST':
    update = json.loads(request.body.decode('utf-8'))
    handle_update(update)
    return HttpResponse('ok')
  else:
    return HttpResponseBadRequest('Bad Request')
  



# обработчики

def handle_update(update):
    if update['message']['text'] == '/start':
      start_message(update)


@bot.message_handler(commands=['start',])
def start_message(message):
    chat_id = message['message']['chat']['id']
    text = texts['welcome']

    bot.send_message(chat_id, text)




# def handle_update(update):
#   chat_id = update['message']['chat']['id']
#   text = update['message']['text']
  
#   if text == '/start':
#     send_message("sendMessage", {
#       'chat_id': chat_id,
#       'text': f'you said {text}'
#     })


# def send_message(method, data):
#   return requests.post(TELEGRAM_API_URL + method, data)