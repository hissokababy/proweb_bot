from django.core.management.base import BaseCommand, CommandError
from tg_bot.credentials import TELEGRAM_API_URL, URL, TOKEN

from tg_bot.bot import bot

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        bot.delete_webhook(URL)

    