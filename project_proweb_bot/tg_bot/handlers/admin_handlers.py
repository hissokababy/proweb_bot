import telebot
from telebot import types
from telebot.states.sync.context import StateContext

from common.kbds import (Btns, forwarding_type_btns, mailing_type_btns, confirm_delete, go_to_menu, 
                         go_back_or_mail, mail_or_forward, 
                         mailing_courses, mailing_languages, main_btns_inline, main_btns_reply, 
                         pin_or_delete_btns, unpin_or_delete_btns)
from django.db.models import Subquery, OuterRef

from common.texts import texts
from tg_bot.models import Post, PostInChat
from tg_bot.services.group import get_group_or_user_field
from tg_bot.utils import is_btn
from tg_bot.handlers.state import GroupMailing
from tg_bot.services.admin import admin_confirm, posts_mailing
from tg_bot.services.user import get_user_lang, save_user
from tg_bot.bot import bot
from tg_bot.services.admin import add_post_to_state


@bot.message_handler(is_admin=True, commands=['start'])
def admin_start_panel(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Админ панель', reply_markup=mail_or_forward())


# обраюотчик кнопка главное меню 
@bot.message_handler(is_admin=True, func=lambda message: is_btn(message.text, Btns.BACK_TO_MENU_BTN.value))
def main_menu_btn_handler(message: types.Message, state: StateContext):
    admin_start_panel(message)
    state.delete()



@bot.callback_query_handler(func=lambda call: call.data == 'confirm')
def admin_panel(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    admin_confirm(chat_id)
    admin_start_panel(call.message)


@bot.message_handler(is_admin=True, func=lambda message: is_btn(message.text, Btns.MAILING.value))
def handle_mailing(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите тип чата', reply_markup=mailing_type_btns())


@bot.message_handler(is_admin=True, func=lambda message: is_btn(message.text, Btns.FORWARDING.value))
def handle_forwarding(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите тип чата', reply_markup=forwarding_type_btns())



@bot.callback_query_handler(is_admin=True, func=lambda call: call.data.startswith('post_'))
def handle_post(call: types.CallbackQuery):
    chat_id = call.message.chat.id

    _, action, post_id = call.data.split('_')

    post = Post.objects.filter(id=post_id).first()

    post_in_chats_all = post.chats.all()

    post_in_chats = PostInChat.objects.filter(
        id=Subquery(
            post.chats.filter(chat_tg_id=OuterRef("chat_tg_id")).values("pk")[:1]
        )
    )
    if action == 'delete':
        msg = bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=confirm_delete(post.id))
        bot.answer_callback_query(msg.id, 'Вы действительно хотите удалить этот пост?')

    elif action == 'pin':
        if post.type == 'media':
            for i in post_in_chats:
                msg = bot.pin_chat_message(chat_id=i.chat_tg_id, message_id=i.message_id)

                bot.answer_callback_query(call.id, 'Пост был закреплён')

        else:
            for i in post_in_chats_all:
                msg = bot.pin_chat_message(chat_id=i.chat_tg_id, message_id=i.message_id)


        bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=unpin_or_delete_btns(post_id))

    elif action == 'unpin':
        for chat in post_in_chats_all:
            try:
                msg = bot.unpin_chat_message(chat_id=int(chat.chat_tg_id), message_id=int(chat.message_id))
                bot.answer_callback_query(call.id, 'Пост был откреплён')
            except Exception as e:
                print(e)
                pass
        bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=pin_or_delete_btns(post_id))



@bot.callback_query_handler(is_admin=True, func=lambda call: call.data.startswith('delete_'))
def confirm_delete_handler(call: types.CallbackQuery):
    chat_id = call.message.chat.id

    _, action, post_id = call.data.split('_')

    post = Post.objects.filter(id=post_id).first()

    post_in_chat_ids = post.chats.all()


    if action == 'yes':
        for chat in post_in_chat_ids:
            try:
                bot.delete_message(chat.chat_tg_id, chat.message_id)
            except Exception as e:
                print(e)
                pass
        bot.send_message(chat_id, 'Пост был удалён')
        bot.delete_message(chat_id, call.message.id)

    elif action == 'no':
        bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=pin_or_delete_btns(post_id))


# расслыка по группам
@bot.message_handler(is_admin=True, func=lambda message: is_btn(message.text, Btns.GROUP_MAILING_BTN.value))
def group_mailing(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    state.set(GroupMailing.language)
    bot.send_message(chat_id, 'Выберите язык', reply_markup=mailing_languages(get_group_or_user_field(language=True), groups=True))
    

# расслыка по личным чатам
@bot.message_handler(is_admin=True, func=lambda message: is_btn(message.text, Btns.PRIVATE_MAILING_BTN.value))
def private_mailing(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    state.set(GroupMailing.language)
    bot.send_message(chat_id, 'Выберите язык пользователей', reply_markup=mailing_languages(get_group_or_user_field(private=True)))
    

# перессылка по группам
@bot.message_handler(is_admin=True, func=lambda message: is_btn(message.text, Btns.GROUP_FORWARDING_BTN.value))
def group_forwarding(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    state.set(GroupMailing.language)
    state.add_data(forwarding=True)
    bot.send_message(chat_id, 'Выберите язык', reply_markup=mailing_languages(get_group_or_user_field(language=True), groups=True))
    

# перессылка по личным чатам
@bot.message_handler(is_admin=True, func=lambda message: is_btn(message.text, Btns.PRIVATE_FORWARDING_BTN.value))
def private_forwarding(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    state.set(GroupMailing.language)
    state.add_data(forwarding=True)
    bot.send_message(chat_id, 'Выберите язык пользователей', reply_markup=mailing_languages(get_group_or_user_field(private=True)))


# обраюотчик кнопка далее 
@bot.message_handler(is_admin=True, state=[GroupMailing.language, GroupMailing.course], 
                     func=lambda message: is_btn(message.text, Btns.CONTINUE_BTN.value))
def continue_handler(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    users_langs = get_group_or_user_field(private=True)

    with state.data() as data:
        language = data.get('language')
        course = data.get('course')
        forwarding = data.get('forwarding')
    
    if not language:
        bot.send_message(chat_id, 'Пожалуйста выберите язык ниже')

    else:

        current_state = state.get()

        if current_state == GroupMailing.language.name and language[0] in users_langs:
            if not forwarding:
                bot.send_message(chat_id, f"Введите пост для рассылки", reply_markup=go_to_menu())
            else:
                bot.send_message(chat_id, f"Отправьте пост", reply_markup=go_to_menu())

            state.set(GroupMailing.post)

        elif current_state == GroupMailing.language.name:
            if language:
                bot.send_message(chat_id, f"Выберите курс", reply_markup=mailing_courses(get_group_or_user_field(course=True)))            
                state.set(GroupMailing.course)

            else:
                bot.send_message(chat_id, 'Выберите хотябы один язык')
        
        elif current_state == GroupMailing.course.name:
            if course:
                if not forwarding:
                    bot.send_message(chat_id, f"Введите пост для рассылки", reply_markup=go_to_menu())
                else:
                    bot.send_message(chat_id, f"Отправьте пост", reply_markup=go_to_menu())

                state.set(GroupMailing.post)
            
            else:
                bot.send_message(chat_id, 'Выберите хотябы один курс')


@bot.message_handler(is_admin=True, state=GroupMailing.language)
def get_language(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    users_langs = get_group_or_user_field(private=True)

    if not message.text in get_group_or_user_field(language=True) and message.text != Btns.ALL_GROUP_LANGUAGES.value and message.text != Btns.ALL_USERS_LANGUAGES:
        bot.send_message(chat_id, 'Пожалуйста выберите язык ниже')
    else:
        if message.text == Btns.ALL_GROUP_LANGUAGES.value:
            state.add_data(language=message.text)
            bot.send_message(chat_id, f"Выберите курс", reply_markup=mailing_courses(get_group_or_user_field(course=True)))
            state.set(GroupMailing.course)

        elif message.text == Btns.ALL_USERS_LANGUAGES.value:
            state.add_data(language=message.text)
            bot.send_message(chat_id, f"Отправляйте пост", reply_markup=go_to_menu())
            state.set(GroupMailing.post)

                
        else:
            with state.data() as data:
                chosen_languages = data.get("language")
                if not chosen_languages:
                    chosen_languages = []
            
            if message.text not in chosen_languages:
                chosen_languages.append(message.text)
                state.add_data(language=chosen_languages)
            else:
                chosen_languages.remove(message.text)

            if len(chosen_languages) >= 1:
                if not message.text in users_langs:
                    bot.send_message(chat_id, f"<b>Выбранные языки:</b> {', '.join(chosen_languages)}", reply_markup=mailing_languages(get_group_or_user_field(language=True), groups=True))
                else:
                    bot.send_message(chat_id, f"<b>Выбранные языки:</b> {', '.join(chosen_languages)}", reply_markup=mailing_languages(get_group_or_user_field(private=True)))

            else:
                bot.send_message(chat_id, 'Выберите язык')


@bot.message_handler(is_admin=True, state=GroupMailing.course) 
def course_state(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    if not message.text in get_group_or_user_field(course=True) and message.text != Btns.ALL_COURSES.value:
        bot.send_message(chat_id, 'Пожалуйста выберите курс ниже')

    else:
    
        with state.data() as data:
            chosen_courses = data.get("course")
            forwarding = data.get('forwarding')
            if not chosen_courses:
                chosen_courses = []

        if message.text == 'Все курсы':
            state.add_data(course='Все курсы')
            if not forwarding:
                bot.send_message(chat_id, f"Отправьте пост для рассылки", reply_markup=go_to_menu())
            else:
                bot.send_message(chat_id, f"Перешлите пост", reply_markup=go_to_menu())
            state.set(GroupMailing.post)
        
        else:
            
            if message.text not in chosen_courses:
                chosen_courses.append(message.text)
                state.add_data(course=chosen_courses)
            else:
                chosen_courses.remove(message.text)


            if len(chosen_courses) >= 1:

                bot.send_message(chat_id, f"<b>Выбранные курсы:</b> {', '.join(chosen_courses)}", reply_markup=mailing_courses(get_group_or_user_field(course=True)))

            else:
                bot.send_message(chat_id, 'Выберите курс')



@bot.message_handler(is_admin=True, state=[GroupMailing.post, GroupMailing.sending], func=lambda message: is_btn(message.text, Btns.SEND_POST.value)) 
def sending_state(message: types.Message, state: StateContext):
    chat_id = message.chat.id

    state.set(GroupMailing.sending)
    posts_mailing(state, message)
    
    state.delete()
    admin_start_panel(message)


@bot.message_handler(is_admin=True, state=GroupMailing.post, content_types=['text', 'photo', 'video', 'document', 'voice', 'audio']) 
def post_state(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    add_post_to_state(state, message)

