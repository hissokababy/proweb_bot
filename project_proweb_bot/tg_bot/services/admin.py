
# подтверждение админа пользователя
from telebot import types
from tg_bot.services.group import get_group_or_user_field
from tg_bot.models import Group, MediaGroupFile, Post, PostEntities, User, UserAdmin


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
from common.kbds import ALL_COURSES, ALL_GROUP_LANGUAGES, ALL_USERS_LANGUAGES, MAILING_BTN, go_back_or_mail

# функция добавления поста в состояние post
def add_post_to_state(state, message):
    chat_id = message.chat.id

    with state.data() as data:
        post_data = data.get("post")
        if not post_data:
            post_data = []

    if not message.media_group_id:
        if message.text:
            media_id = message.id
            media_data = message.text
            media_type = 'text'

        post = Post.objects.create(caption=media_data, post_tg_id=media_id, type=media_type)

        if message.entities:
            entities = message.entities
            for entity in entities:
                post_entity = PostEntities.objects.create(post=post, type=entity.type, offset=entity.offset,
                                                length=entity.length, url=entity.url, user=entity.user,
                                                language=entity.language, custom_emoji_id=entity.custom_emoji_id)


    if media_id not in post_data:
        post_data.append(media_id)
        state.add_data(post=post_data)
    else:
        post_data.remove(media_id)

    if len(post_data) >= 1:
        bot.send_message(chat_id, 'Пост готов, нажмите <b>"Рассылать"</b>', reply_markup=go_back_or_mail())

    else:
        bot.send_message(chat_id, 'Отправьте хотябы один пост для рассылки')



        # if message.video and message.caption:
        #     video_or_photo = {'type':'video', 'video_id': message.video.file_id, 'caption': message.caption}

        # elif message.photo and message.caption:
        #     video_or_photo = {'type':'photo', 'photo_id': message.photo[-1].file_id, 'caption': message.caption}

        # elif message.text:
        #     video_or_photo = {'type':'text', 'text': message.text}

        # with state.data() as data:
        #     post_data = data.get("post")
        #     if not post_data:
        #         post_data = []
            
        # if video_or_photo not in post_data:
        #     post_data.append(video_or_photo)
        #     state.add_data(post=post_data)
        # else:
        #     post_data.remove(video_or_photo)

        # if len(post_data) >= 1:
        #     bot.send_message(chat_id, 'Пост готов, нажмите <b>"Рассылать"</b>', reply_markup=go_back_or_mail())

        # else:
        #     bot.send_message(chat_id, 'Отправьте хотябы один пост для рассылки')

    # elif message.media_group_id:
    #     with state.data() as data:
    #         post_data = data.get("post")
    #         media_group_caption = data.get('media_group_caption')
        
    #     if message.video:
    #         media_id = message.video.file_id
    #         media_file_type = 'video'


    #     elif message.photo:
    #         media_id = message.photo[-1].file_id
    #         media_file_type = 'photo'
        
    #     if message.caption:
    #         caption = message.caption
        
    #     media_group_post = Post.objects.filter(media_group_id=message.media_group_id).first()

    #     if media_group_post:
    #         media_group_file = MediaGroupFile.objects.create(media_group=media_group_post, media_id=media_id)

    #     else:
    #         media_group_post = Post.objects.create(media_group_id=message.media_group_id,
    #                                                          caption=caption, media_file_type=media_file_type)
            
    #         media_group_file = MediaGroupFile.objects.create(media_group=media_group_post, media_id=media_id)


    #     with state.data() as data:
    #         post_data = data.get("post")
    #         if not post_data:
    #             post_data = []

    #     if message.media_group_id not in post_data:
    #         post_data.append(message.media_group_id)
    #         state.add_data(post=post_data)

    #     bot.send_message(chat_id, f'Пост готов, нажмите <b>"{MAILING_BTN}"</b>', reply_markup=go_back_or_mail())


# отправка постов
def posts_mailing(state, message):
    chat_id = message.chat.id

    groups = None
    users = None
    users_langs = get_group_or_user_field(private=True)

    with state.data() as data:
        language = data.get("language")
        course = data.get("course")
        post_data = data.get("post")
    
    users = User.objects.all()

    for user in users:
        for item in post_data:
            post = Post.objects.get(post_tg_id=item)

            entities = []
            for i in post.entities.all():

                entity = types.MessageEntity(type=i.type, offset=i.offset, length=i.length,
                                             url=i.url)
                entities.append(entity)
            print(entities)
            bot.send_message(user.tg_id, post.caption, entities=entities)




    # if language == ALL_USERS_LANGUAGES:
    #     users = User.objects.all()
    
    # elif language != ALL_USERS_LANGUAGES and language[0] in users_langs:
    #     users = User.objects.filter(language_selected__in=users_langs)

    # elif language == ALL_GROUP_LANGUAGES and course != ALL_COURSES:
    #     groups = Group.objects.filter(course__in=course, is_in_group=True)

    # elif course == ALL_COURSES and language != ALL_GROUP_LANGUAGES:
    #     groups = Group.objects.filter(language__in=language, is_in_group=True)

    # elif language == ALL_GROUP_LANGUAGES and course == ALL_COURSES:
    #     groups = Group.objects.filter(is_in_group=True)

    # else:
    #     groups = Group.objects.filter(language__in=language, course__in=course, is_in_group=True)

    # media_group_posts = []

    # if groups:
    #     for group in groups:
    #         if group.is_in_group:
    #             for item in post_data:
    #                 if type(item) is str and not item.isdigit():
    #                     bot.send_message(group.tg_id, item)

    #                 elif type(item) is dict:
    #                     if item['type'] == 'video':
    #                         bot.send_video(group.tg_id, video=item['video_id'], caption=item['caption'])

    #                     elif item['type'] == 'photo':
    #                         bot.send_photo(group.tg_id, photo=item['photo_id'], caption=item['caption'])

    #                     elif item['type'] == 'text':
    #                         bot.send_message(group.tg_id, item['text'])

    #                 else:
    #                     media_group_post = MediaGroupPost.objects.get(media_group_id=item)
    #                     if media_group_post not in media_group_posts:
    #                         media_group_posts.append(media_group_post)


    #             if len(media_group_posts) >= 1:
    #                 for post in media_group_posts:
    #                     caption = post.caption
    #                     post_files = post.files.all()

    #                     group_media = []

    #                     for post_file in post_files:
    #                         if post.media_file_type == 'photo':
    #                             if post_file == post_files[0]:
    #                                 group_media.append(types.InputMediaPhoto(post_file.media_id, caption=caption))
    #                             else:
    #                                 group_media.append(types.InputMediaPhoto(post_file.media_id))
                            
    #                         if post.media_file_type == 'video':
    #                             if post_file == post_files[0]:
    #                                 group_media.append(types.InputMediaVideo(post_file.media_id, caption=caption))
    #                             else:
    #                                 group_media.append(types.InputMediaVideo(post_file.media_id))
                            

    #                     bot.send_media_group(chat_id=group.tg_id, media=group_media)
    
    # elif users:
    #     for user in users:
    #             for item in post_data:
    #                 if type(item) is str and not item.isdigit():
    #                     bot.send_message(user.tg_id, item)

    #                 elif type(item) is dict:
    #                     if item['type'] == 'video':
    #                         bot.send_video(user.tg_id, video=item['video_id'], caption=item['caption'])

    #                     elif item['type'] == 'photo':
    #                         bot.send_photo(user.tg_id, photo=item['photo_id'], caption=item['caption'])

    #                     elif item['type'] == 'text':
    #                         bot.send_message(user.tg_id, item['text'])

    #                 else:
    #                     media_group_post = MediaGroupPost.objects.get(media_group_id=item)
    #                     if media_group_post not in media_group_posts:
    #                         media_group_posts.append(media_group_post)


    #             if len(media_group_posts) >= 1:
    #                 for post in media_group_posts:
    #                     caption = post.caption
    #                     post_files = post.files.all()

    #                     group_media = []

    #                     for post_file in post_files:
    #                         if post.media_file_type == 'photo':
    #                             if post_file == post_files[0]:
    #                                 group_media.append(types.InputMediaPhoto(post_file.media_id, caption=caption))
    #                             else:
    #                                 group_media.append(types.InputMediaPhoto(post_file.media_id))
                            
    #                         if post.media_file_type == 'video':
    #                             if post_file == post_files[0]:
    #                                 group_media.append(types.InputMediaVideo(post_file.media_id, caption=caption))
    #                             else:
    #                                 group_media.append(types.InputMediaVideo(post_file.media_id))
                            

    #                     bot.send_media_group(chat_id=user.tg_id, media=group_media)
    