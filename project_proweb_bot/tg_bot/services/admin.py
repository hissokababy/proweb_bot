
# подтверждение админа пользователя
from telebot import types
from tg_bot.utils import get_media_file_group, mailing_to_receivers
from tg_bot.services.group import get_group_or_user_field
from tg_bot.models import Group, MediaGroupFile, Post, User, UserAdmin

from tg_bot.bot import bot
from common.kbds import Btns, go_back_or_mail, mail_or_forward

def make_admin(queryset):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn = types.InlineKeyboardButton(text='Да, согласен', callback_data='confirm')
    btn1 = types.InlineKeyboardButton(text='Не согласен', callback_data='cancel')

    for user in queryset:
        bot.send_message(user.user.tg_id, 'PROWEB хочет назначить вас администратором, вы согласны?', reply_markup=markup.add(btn, btn1))



def admin_confirm(tg_id):
    user_admin = UserAdmin.objects.get(user__tg_id=tg_id)
    user_admin.confirmed_by_user = True
    user_admin.save()


# функция добавления поста в состояние post
def add_post_to_state(state, message):
    chat_id = message.chat.id

    with state.data() as data:
        post_data = data.get("post")
        is_forwarding = data.get('forwarding')
        if not post_data:
            post_data = []

    if not message.media_group_id:
        post_tg_id = message.id

        if message.text:
            media_id = message.id
            media_type = 'text'
            media_data = message.html_text

        elif message.video:
            media_id = message.video.file_id
            media_type = 'video'
            media_data = message.html_caption


        elif message.photo:
            media_id = message.photo[-1].file_id
            media_type = 'photo'
            media_data = message.html_caption

        
        elif message.document:
            media_id = message.document.file_id
            media_type = 'document'
            media_data = message.html_caption

        
        elif message.audio:
            media_id = message.audio.file_id
            media_type = 'audio'
            media_data = message.html_caption

        if not is_forwarding:
            post = Post.objects.create(caption=media_data, media_id=media_id, post_tg_id=post_tg_id, type=media_type)
        else:
            post = Post.objects.create(caption=media_data, media_id=media_id, post_tg_id=post_tg_id, type=media_type, is_forwarding=int(message.chat.id))

        # добавление или удаление ид сообщения в состояние post
        if media_id not in post_data:
            post_data.append(post_tg_id)
            state.add_data(post=post_data)
        else:
            post_data.remove(media_id)

    elif message.media_group_id:
        post_tg_id = message.id
        media_group_id = message.media_group_id
        type = 'media'
        if message.html_caption:
            caption = message.html_caption

        # добавление или удаление ид медиа группы в состояние post
        if media_group_id not in post_data:
            post_data.append(media_group_id)
            state.add_data(post=post_data)

        post = Post.objects.filter(type=type, media_group_id=media_group_id).first()
        
        if not post and not is_forwarding:            
            post = Post.objects.create(type=type, media_group_id=media_group_id, caption=caption, post_tg_id=message.id)
        elif not post and is_forwarding:
            post = Post.objects.create(type=type, media_group_id=media_group_id, caption=caption, post_tg_id=message.id, is_forwarding=int(message.chat.id))

        if message.video:
            media_type = 'video'
            media_id = message.video.file_id

        elif message.photo:
            media_type = 'photo'
            media_id = message.photo[-1].file_id

        elif message.document:
            media_type = 'document'
            media_id = message.document.file_id

        post_file = MediaGroupFile.objects.create(post=post, media_id=media_id, type=media_type, message_id=message.id)
    
    if len(post_data) >= 1:
        bot.send_message(chat_id, 'Пост готов, нажмите <b>"Отправить"</b>', reply_markup=go_back_or_mail())


# отправка постов
def posts_mailing(state, message):
    chat_id = message.chat.id

    receivers = None

    users_langs = get_group_or_user_field(private=True)

    with state.data() as data:
        language = data.get("language")
        course = data.get("course")
        post_data = data.get("post")
        forwarding = data.get('forwarding')
        

    if language == Btns.ALL_USERS_LANGUAGES.value:
        receivers = User.objects.all()

    elif language != Btns.ALL_USERS_LANGUAGES.value and language[0] in users_langs:
        receivers = User.objects.filter(language_selected__in=users_langs)

    elif language == Btns.ALL_GROUP_LANGUAGES.value and course != Btns.ALL_COURSES.value:
        receivers = Group.objects.filter(course__in=course, is_in_group=True)

    elif course == Btns.ALL_COURSES.value and language != Btns.ALL_GROUP_LANGUAGES.value:
        receivers = Group.objects.filter(language__in=language, is_in_group=True)

    elif language == Btns.ALL_GROUP_LANGUAGES.value and course == Btns.ALL_COURSES.value:
        receivers = Group.objects.filter(is_in_group=True)

    else:
        receivers = Group.objects.filter(language__in=language, course__in=course, is_in_group=True)

    if type(language) is list:
        language = ', '.join(language)
    if type(course) is list:
        course = ', '.join(course)

    report = {
        'language': language,
        'course': course,
        'receivers': receivers.count(),
    }

    mailing_to_receivers(post_data, receivers, chat_id, report)
