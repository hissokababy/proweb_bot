
# подтверждение админа пользователя
from telebot import types
from tg_bot.models import MediaGroupFile, MediaGroupPost, UserAdmin


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
        with state.data() as data:
            post_data = data.get("post")
            media_group_caption = data.get('media_group_caption')
        
        if message.video:
            media_id = message.video.file_id
            media_file_type = 'video'


        elif message.photo:
            media_id = message.photo[-1].file_id
            media_file_type = 'photo'
        
        if message.caption:
            caption = message.caption
        
        media_group_post = MediaGroupPost.objects.filter(media_group_id=message.media_group_id).first()

        if media_group_post:
            media_group_file = MediaGroupFile.objects.create(media_group=media_group_post, media_id=media_id)

        else:
            media_group_post = MediaGroupPost.objects.create(media_group_id=message.media_group_id,
                                                             caption=caption, media_file_type=media_file_type)
            
            media_group_file = MediaGroupFile.objects.create(media_group=media_group_post, media_id=media_id)


        with state.data() as data:
            post_data = data.get("post")
            if not post_data:
                post_data = []

        if message.media_group_id not in post_data:
            post_data.append(message.media_group_id)
            state.add_data(post=post_data)

        bot.send_message(chat_id, f'Пост готов, нажмите <b>"{MAILING_BTN}"</b>', reply_markup=go_back_or_mail())

# отправка постов
def posts_mailing(state, message):
    chat_id = message.chat.id

    with state.data() as data:
        post_data = data.get("post")
        media_group_caption = data.get('media_group_caption')

    media_group_posts = []

    for item in post_data:
        if type(item) is dict:
            if item['type'] == 'video':
                bot.send_video(chat_id, video=item['video_id'], caption=item['caption'])

            elif item['type'] == 'photo':
                bot.send_photo(chat_id, photo=item['photo_id'], caption=item['caption'])
        else:
            media_group_post = MediaGroupPost.objects.get(media_group_id=item)
            if media_group_post not in media_group_posts:
                media_group_posts.append(media_group_post)


    if len(media_group_posts) >= 1:
        for post in media_group_posts:
            caption = post.caption
            post_files = post.files.all()

            group = []

            for post_file in post_files:
                if post.media_file_type == 'photo':
                    if post_file == post_files[0]:
                        group.append(types.InputMediaPhoto(post_file.media_id, caption=caption))
                    else:
                        group.append(types.InputMediaPhoto(post_file.media_id))
                
                if post.media_file_type == 'video':
                    if post_file == post_files[0]:
                        group.append(types.InputMediaVideo(post_file.media_id, caption=caption))
                    else:
                        group.append(types.InputMediaVideo(post_file.media_id))
                

            bot.send_media_group(chat_id, media=group)