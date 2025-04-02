import telebot
from tg_bot.models import UserAdmin

# проверка пользоваетя на админа
class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_admin'
    
    @staticmethod
    def check(message: telebot.types.Message):
        tg_id = message.from_user.id
        admin = UserAdmin.objects.filter(user__tg_id=tg_id, confirmed_by_user=True).exists()
        return admin

