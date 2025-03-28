import telebot
from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext

from common.kbds import (admin_panel_btn, go_to_menu, go_back_or_mail, 
                         mailing_courses, mailing_languages, main_btns_inline, main_btns_reply)
from common.texts import texts
from tg_bot.services.group import get_group_field
from tg_bot.utils import is_continue_btn, is_group_mailing_btn, is_main_btn, is_private_mailing_btn, is_sending_btn
from tg_bot.services.admin import admin_confirm, is_admin, posts_mailing
from tg_bot.services.user import get_user_lang, save_user
from tg_bot.bot import bot



@bot.message_handler(commands=['start'])
def admin_start_panel(message: types.Message):
    chat_id = message.chat.id
    save_user(tg_user=message.from_user)

    if is_admin(chat_id):
        bot.send_message(chat_id, 'Админ панель', reply_markup=admin_panel_btn())

    else:
      user_lang = get_user_lang(tg_id=message.from_user.id)

      bot.send_message(chat_id, texts[user_lang]['welcome']['hello_msg'], reply_markup=main_btns_reply(user_lang, 'main'))
      
      bot.send_message(chat_id, texts[user_lang]['welcome']['greeting'], reply_markup=main_btns_inline(user_lang, 'main'))


@bot.callback_query_handler(func=lambda call: call.data == 'confirm')
def admin_panel(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    admin_confirm(chat_id)
    admin_start_panel(call.message)


class GroupMailing(StatesGroup):
    language = State()
    course = State()
    post = State()
    sending = State()


# расслыка по группам
@bot.message_handler(func=lambda message: is_group_mailing_btn(message.text))
def group_mailing(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    if is_admin(chat_id):
        state.set(GroupMailing.language)
        bot.send_message(chat_id, 'Выберите язык групп', reply_markup=mailing_languages(get_group_field(language=True)))
    

# расслыка по личным чатам
@bot.message_handler(func=lambda message: is_private_mailing_btn(message.text))
def group_mailing(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    if is_admin(chat_id):
        state.set(GroupMailing.language)
        bot.send_message(chat_id, 'Выберите язык пользователей', reply_markup=mailing_languages(get_group_field(language=True)))
    

# обраюотчик кнопка главное меню 
@bot.message_handler(state=[GroupMailing.language, GroupMailing.course, GroupMailing.post], 
                     func=lambda message: is_main_btn(message.text))
def main_menu_btn_handler(message: types.Message, state: StateContext):
    
    admin_start_panel(message)
    state.delete()


# обраюотчик кнопка далее 
@bot.message_handler(state=[GroupMailing.language, GroupMailing.course], 
                     func=lambda message: is_continue_btn(message.text))
def continue_handler(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    with state.data() as data:
        language = data.get('language')
        course = data.get('course')

    current_state = state.get()
    if current_state == GroupMailing.language.name:
        if language:
            bot.send_message(chat_id, f"Выберите курс", reply_markup=mailing_courses(get_group_field(course=True)))            
            state.set(GroupMailing.course)

        else:
            bot.send_message(chat_id, 'Выберите хотябы один язык')

    elif current_state == GroupMailing.course.name:
        if course:
            bot.send_message(chat_id, f"Введите пост для рассылки", reply_markup=go_to_menu())
            state.set(GroupMailing.post)
        
        else:
            bot.send_message(chat_id, 'Выберите хотябы один курс')


@bot.message_handler(state=GroupMailing.language)
def get_language(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    if message.text == 'Все языки':
        state.add_data(language='Все языки')
        bot.send_message(chat_id, f"Выберите курс", reply_markup=mailing_courses(get_group_field(course=True)))
        state.set(GroupMailing.course)
            
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
            bot.send_message(chat_id, f"<b>Выбранные языки:</b> {', '.join(chosen_languages)}", reply_markup=mailing_languages(get_group_field(language=True)))
        else:
            bot.send_message(chat_id, 'Выберите язык')


@bot.message_handler(state=GroupMailing.course) 
def course_state(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    if message.text == 'Все курсы':
        state.add_data(course='Все курсы')
        bot.send_message(chat_id, f"Отправьте пост для рассылки", reply_markup=go_to_menu())
        state.set(GroupMailing.post)
    
    else:
        with state.data() as data:
            chosen_courses = data.get("course")
            if not chosen_courses:
                chosen_courses = []
        
        if message.text not in chosen_courses:
            chosen_courses.append(message.text)
            state.add_data(course=chosen_courses)
        else:
            chosen_courses.remove(message.text)


        if len(chosen_courses) >= 1:

            bot.send_message(chat_id, f"<b>Выбранные курсы:</b> {', '.join(chosen_courses)}", reply_markup=mailing_courses(get_group_field(course=True)))

        else:
            bot.send_message(chat_id, 'Выберите курс')




@bot.message_handler(state=[GroupMailing.post, GroupMailing.sending], func=lambda message: is_sending_btn(message.text)) 
def sending_state(message: types.Message, state: StateContext):
    chat_id = message.chat.id

    state.set(GroupMailing.sending)
    posts_mailing(state, message)

    state.delete()
    admin_start_panel(message)


from tg_bot.services.admin import add_post_to_state

@bot.message_handler(state=GroupMailing.post, content_types=['text', 'photo', 'video']) 
def post_state(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    add_post_to_state(state, message)


