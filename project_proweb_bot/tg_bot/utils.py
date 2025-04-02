from common.kbds import (Btns, pin_or_delete_btns)
from telebot import types
from tg_bot.bot import bot
from tg_bot.models import Post, PostInChat


def is_btn(text, btn):
    if text == btn:
        return True


# получение медиа группы фалов
def get_media_file_group(post):
    post_files = post.files.all()

    group_files = []

    for post_file in post_files:
                    
        if post_file.type == 'photo':
            if post_file == post_files[0]:
                file = types.InputMediaPhoto(media=post_file.media_id, caption=post.caption)
            else:
                file = types.InputMediaPhoto(media=post_file.media_id)

        if post_file.type == 'video':
            if post_file == post_files[0]:
                file = types.InputMediaVideo(media=post_file.media_id, caption=post.caption)
            else:
                file = types.InputMediaVideo(media=post_file.media_id)
                
        group_files.append(file)

    return group_files


# рассылка постов пользователям или группам
def mailing_to_receivers(post_data, receivers, chat_id, report):
    receivers_tg_ids = [i.tg_id for i in receivers]
    posts_sent = []
    msg_media_forward = None
    unsuccessful = 0
    
    for receiver in receivers:
        for post_tg_id in post_data:
            post = Post.objects.filter(post_tg_id=post_tg_id) | Post.objects.filter(media_group_id=post_tg_id)
            post = post.first()

            posts_sent.append(post) if not post in posts_sent else ...

            try:
                if post.is_forwarding and post.type != 'media':
                    msg = bot.forward_message(receiver.tg_id, from_chat_id=post.is_forwarding, message_id=post.post_tg_id)

                elif post.type == 'text':
                    msg = bot.send_message(receiver.tg_id, post.caption)

                elif post.type == 'photo':
                    msg = bot.send_photo(receiver.tg_id, photo=post.media_id, caption=post.caption)

                elif post.type == 'video':
                    msg = bot.send_video(receiver.tg_id, video=post.media_id, caption=post.caption)

                elif post.type == 'document':
                    msg = bot.send_document(receiver.tg_id, document=post.media_id, caption=post.caption)

                elif post.is_forwarding and post.type == 'media':
                    post_msg_ids = [i.message_id for i in post.files.all()]
                    msg_media_forward = bot.forward_messages(receiver.tg_id, from_chat_id=post.is_forwarding, message_ids=post_msg_ids)
                    for i in msg_media_forward:
                        post_in_chat = PostInChat.objects.create(post=post, chat_tg_id=receiver.tg_id, message_id=i.message_id, media_group_id=post.media_group_id)

                elif post.type == 'media':
                    msg_media_forward = bot.send_media_group(receiver.tg_id, media=get_media_file_group(post))
                    post_msg_ids = [i.message_id for i in post.files.all()]
                    for i in msg_media_forward:
                        post_in_chat = PostInChat.objects.create(post=post, chat_tg_id=receiver.tg_id, message_id=i.id, media_group_id=post.media_group_id)

                try:
                    post_in_chat = PostInChat.objects.create(post=post, chat_tg_id=receiver.tg_id, message_id=msg.id)
                except Exception as e:
                    print(e)
                    pass
            except Exception as e:
                print(e)
                unsuccessful += 1

    report['unsuccessful'] = unsuccessful
    is_send_to_owner(posts_sent, chat_id, report)

# отправлен ли пост отправителю
def is_send_to_owner(posts_sent, chat_id, report):
    
    for post in posts_sent:
        if post.type == 'text':
            bot.send_message(chat_id, post.caption, reply_markup=pin_or_delete_btns(post.id))

        elif post.type == 'photo':
            bot.send_photo(chat_id, photo=post.media_id, caption=post.caption, reply_markup=pin_or_delete_btns(post.id))

        elif post.type == 'video':
            bot.send_video(chat_id, video=post.media_id, caption=post.caption, reply_markup=pin_or_delete_btns(post.id))
        elif post.type == 'document':
            bot.send_document(chat_id, document=post.media_id, caption=post.caption, reply_markup=pin_or_delete_btns(post.id))

        elif post.type == 'media':
            bot.send_media_group(chat_id, media=get_media_file_group(post))
            bot.send_message(chat_id, f'Пост {post.id}', reply_markup=pin_or_delete_btns(post.id))
    

    bot.send_message(chat_id, f"Отчёт: \nЯзыки: {report['language']}\nКурсы: {report['course']}\nПолучатели: {report['receivers']}\nУспешно: {report['receivers'] - report['unsuccessful']}\nНе успешно: {report['unsuccessful']}")

