import json
import requests
from tg_bot.credentials import TELEGRAM_API_URL, URL
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from tg_bot.handlers import handle_update

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
  
