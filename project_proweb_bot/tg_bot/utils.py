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


# подтверждение админа пользователя
def admin_confirm(tg_id):
    user_admin = UserAdmin.objects.get(user__tg_id=tg_id)
    user_admin.confirmed_by_user = True
    user_admin.save()


# проверка пользоваетя на админа
def is_admin(tg_id):
    admins = UserAdmin.objects.filter(confirmed_by_user=True)
    lst = [i.user.tg_id for i in admins]

    if tg_id in lst:
        return True


# добавление группы бота
def add_bot_group(group):
    tg_id = group.id
    title = group.title.split()
    
    if title[0].startswith('PROWEB'):
        if title[1].isupper() and title[2].isupper():
            if re.match(r"^(([0,1][0-9])|(2[0-3])):[0-5][0-9]$", title[-1]):
                if re.match(r"[А-Я][А-Я]-[А-Я][А-Я]|[A-Z][A-Z]-[A-Z][A-Z]", title[3]):
                    course = title[1]
                    language = title[2]
                    days = title[3]
                    time = title[-1]
                    group = Group.objects.filter(tg_id=tg_id).exists()

                    if not group:
                        Group.objects.create(tg_id=tg_id,
                                     course=course,
                                     language=language,
                                     days=days,
                                     time=time)
