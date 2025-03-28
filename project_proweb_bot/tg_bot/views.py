from tg_bot.services.group import add_bot_group
from tg_bot import  group_handler, admin_handlers, user_handlers
from tg_bot import models

import requests
import telebot

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from tg_bot.credentials import TELEGRAM_API_URL, URL


# установка вебхука
def setwebhook(request):
  response = requests.post(TELEGRAM_API_URL + "setWebhook?url=" + URL).json()
  return HttpResponse(f"{response}")

from tg_bot.bot import bot

@csrf_exempt
def telegram_bot(request):
  if request.method == 'POST':
    json_string = request.body.decode('utf-8')

    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])


    return HttpResponse('ok')

  else:
    return HttpResponseBadRequest('Bad Request')
  
