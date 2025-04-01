from common.kbds import BACK_TO_MENU_BTN, CONTINUE_BTN, FORWARDING, GROUP_FORWARDING_BTN, MAILING, MAILING_BTN, GROUP_MAILING_BTN, PRIVATE_FORWARDING_BTN, PRIVATE_MAILING_BTN, SEND_POST, mail_or_forward, pin_or_delete_btns
from telebot import types
from tg_bot.bot import bot
from tg_bot.models import Post, PostInChat

def is_continue_btn(text):
    if text == CONTINUE_BTN:
        return True
    
def is_mailing_btn(text):
    if text == MAILING:
        return True
    
def is_forwarding_btn(text):
    if text == FORWARDING:
        return True

    
def is_send_post_btn(text):
    if text == SEND_POST:
        return True

def is_main_btn(text):
    if text == BACK_TO_MENU_BTN:
        return True
    
def is_sending_btn(text):
    if text == MAILING_BTN:
        return True


def is_group_mailing_btn(text):
    if text == GROUP_MAILING_BTN:
        return True

def is_private_mailing_btn(text):
    if text == PRIVATE_MAILING_BTN:
        return True
    
def is_group_forwarding_btn(text):
    if text == GROUP_FORWARDING_BTN:
        return True

def is_private_forwarding_btn(text):
    if text == PRIVATE_FORWARDING_BTN:
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
def mailing_to_receivers(post_data, receivers, chat_id):
    receivers_tg_ids = [i.tg_id for i in receivers]
    msg_ids = []
    post = None
    total_posts = len(post_data)
    
    for receiver in receivers:
        for post_tg_id in post_data:
            post = Post.objects.filter(post_tg_id=post_tg_id) | Post.objects.filter(media_group_id=post_tg_id)
            post = post.first()

            if post.is_forwarding and post.type != 'media':
                    msg = bot.forward_message(receiver.tg_id, from_chat_id=post.is_forwarding, message_id=post.post_tg_id)

            elif post.is_forwarding and post.type == 'media':
                 bot.send_message(chat_id, 'Медиа группу нельзя переслать', reply_markup=mail_or_forward())

            elif post.type == 'text':
                    msg = bot.send_message(receiver.tg_id, post.caption)

            elif post.type == 'photo':
                    msg = bot.send_photo(receiver.tg_id, photo=post.media_id, caption=post.caption)

            elif post.type == 'video':
                    msg = bot.send_video(receiver.tg_id, video=post.media_id, caption=post.caption)

            elif post.type == 'document':
                    msg = bot.send_document(receiver.tg_id, document=post.media_id, caption=post.caption)

            elif post.type == 'media':
                    msg = bot.send_media_group(receiver.tg_id, media=get_media_file_group(post))
            
            msg_ids.append(msg.id)

            post_in_chat = PostInChat.objects.create(post=post, chat_tg_id=receiver.tg_id, message_id=msg.id)

    
    is_send_to_owner(post, chat_id, total_posts)

# отправлен ли пост отправителю
def is_send_to_owner(post, chat_id, total_posts):
    
    for i in range(total_posts):
        if post.type == 'text':
            bot.send_message(chat_id, post.caption, reply_markup=pin_or_delete_btns(post.id))

        elif post.type == 'photo':
            bot.send_photo(chat_id, photo=post.media_id, caption=post.caption, reply_markup=pin_or_delete_btns(post.id))

        elif post.type == 'video':
            bot.send_video(chat_id, video=post.media_id, caption=post.caption, reply_markup=pin_or_delete_btns(post.id))
        elif post.type == 'document':
            bot.send_document(chat_id, document=post.media_id, caption=post.caption, reply_markup=pin_or_delete_btns(post.id))

        elif post.type == 'media':
            bot.send_media_group(chat_id, media=get_media_file_group(post), reply_markup=pin_or_delete_btns(post.id))