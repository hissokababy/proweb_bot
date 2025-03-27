
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
    

from tg_bot.bot import bot
from common.kbds import MAILING_BTN, go_back_or_mail

# функция добавления поста в состояние post
def add_post_to_state(state, message):
    chat_id = message.chat.id

    if not message.media_group_id:
        if message.video and message.caption:
            video_or_photo = {'type':'video', 'video_id': message.video.file_id, 'caption': message.caption}

        elif message.photo and message.caption:
            video_or_photo = {'type':'photo', 'photo_id': message.photo[-1].file_id, 'caption': message.caption}

        with state.data() as data:
            post_data = data.get("post")
            if not post_data:
                post_data = []
            
        if video_or_photo not in post_data:
            post_data.append(video_or_photo)
            state.add_data(post=post_data)
        else:
            post_data.remove(video_or_photo)

        if len(post_data) >= 1:
            bot.send_message(chat_id, 'Пост готов, нажмите <b>"Рассылать"</b>', reply_markup=go_back_or_mail())

        else:
            bot.send_message(chat_id, 'Отправьте хотябы один пост для рассылки')

    elif message.media_group_id:
        if message.video:
            video_or_photo = {'type':'group_video', 'video_id': message.video.file_id}

        elif message.photo:
            video_or_photo = {'type':'group_photo', 'photo_id': message.photo[-1].file_id}
        
        if message.caption:
            caption = message.caption
        
        with state.data() as data:
            post_data = data.get("post")
            media_group_caption = data.get('media_group_caption')

        if not media_group_caption:
            state.add_data(media_group_caption=caption)
        if not post_data:
            post_data = []

        if video_or_photo not in post_data:
            post_data.append(video_or_photo)
            state.add_data(post=post_data)
        else:
            post_data.remove(video_or_photo)

        if len(post_data) > 1:
            bot.send_message(chat_id, f'Пост готов, нажмите <b>"{MAILING_BTN}"</b>', reply_markup=go_back_or_mail())