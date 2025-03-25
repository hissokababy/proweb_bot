# добавление группы бота
import re
from tg_bot.models import Group


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
                                     time=time,
                                     is_in_group=True)

# обработка удаления бота из группы
def left_bot_group(tg_group_id):
    group = Group.objects.get(tg_id=tg_group_id)
    group.is_in_group = False
    group.save()

