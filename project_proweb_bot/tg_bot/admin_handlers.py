import telebot
from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext

from common.kbds import (admin_panel_btn, go_to_menu, go_back_or_mail, 
                         mailing_courses, mailing_languages, main_btns_inline, main_btns_reply)
from common.texts import texts
from tg_bot.utils import is_continue_btn, is_main_btn
from tg_bot.services.admin import admin_confirm, is_admin
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


@bot.message_handler(func=lambda message: message.text == 'Рассылка в группы студентов')
def group_mailing(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    state.set(GroupMailing.language)
    
    if is_admin(chat_id):
        bot.send_message(chat_id, 'Выберите язык групп', reply_markup=mailing_languages())
    

# обраюотчик кнопка главное меню 
@bot.message_handler(state=[GroupMailing.language, GroupMailing.course, GroupMailing.post])
def main_menu_btn_handler(message: types.Message, state: StateContext):
    
    if is_main_btn(message.text):
        admin_start_panel(message)


# обраюотчик кнопка далее 
@bot.message_handler(state=[GroupMailing.language, GroupMailing.course])
def continue_handler(message: types.Message, state: StateContext):
    chat_id = message.chat.id

    if is_continue_btn(message.text):
        current_state = state.get()
        if current_state == GroupMailing.language.name:
            bot.send_message(chat_id, f"Выберите курс", reply_markup=mailing_courses())
            state.set(GroupMailing.course)

        elif current_state == GroupMailing.course.name:
            bot.send_message(chat_id, f"Введите пост для рассылки", reply_markup=go_to_menu())
            state.set(GroupMailing.post)


@bot.message_handler(state=GroupMailing.language)
def get_language(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    if message.text == 'Все языки':
        state.add_data(language='Все языки')
        bot.send_message(chat_id, f"Выберите курс", reply_markup=mailing_courses())
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
            bot.send_message(chat_id, f"<b>Выбранные языки:</b> {', '.join(chosen_languages)}", reply_markup=mailing_languages())
        else:
            bot.send_message(chat_id, 'Выберите язык')


@bot.message_handler(state=GroupMailing.course) 
def course_state(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    if message.text == 'Все курсы':
        state.add_data(course='Все курсы')
        bot.send_message(chat_id, f"Введите пост для рассылки", reply_markup=go_to_menu())
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

            bot.send_message(chat_id, f"<b>Выбранные курсы:</b> {', '.join(chosen_courses)}", reply_markup=mailing_courses())

        else:
            bot.send_message(chat_id, 'Выберите курс')

