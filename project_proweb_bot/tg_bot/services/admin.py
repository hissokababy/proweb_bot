
# подтверждение админа пользователя
from tg_bot.models import UserAdmin


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