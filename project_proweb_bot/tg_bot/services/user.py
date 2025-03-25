from tg_bot.models import Group, User, UserAdmin
import re

# сохранение пользователя в бд
def save_user(tg_user):
    tg_id = tg_user.id
    username = tg_user.username

    user = User.objects.filter(tg_id=tg_id).first()

    if not user:
        User.objects.create(tg_id=tg_id, username=username)
    else:
        return user

# установить язык пользователя
def set_user_lang(tg_id, lang):
    user = User.objects.get(tg_id=tg_id)

    user.language_selected = lang
    user.save()

# язык пользователя
def get_user_lang(tg_id):
    lan = User.objects.get(tg_id=tg_id).language_selected
    return lan


