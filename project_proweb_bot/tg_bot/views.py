from tg_bot.handlers import group_handler, admin_handlers, user_handlers

import telebot

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from tg_bot.bot import bot

@csrf_exempt
def telegram_bot(request):
  if request.method == 'POST':
    json_string = request.body.decode('utf-8')

    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])

    # print(update.message)


    return HttpResponse('ok')

  else:
    return HttpResponseBadRequest('Bad Request')
  
