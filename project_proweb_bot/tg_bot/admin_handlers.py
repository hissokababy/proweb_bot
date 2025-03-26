import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext

from common.kbds import admin_panel_btn, go_back_or_continue_btns, mailing_courses, mailing_languages, main_btns_inline, main_btns_reply
from common.texts import texts
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
    message = State()
    photos = State()


@bot.message_handler(func=lambda message: message.text == 'Рассылка в группы студентов')
def group_mailing(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    state.set(GroupMailing.language)
    
    if is_admin(chat_id):
        bot.send_message(chat_id, 'Выберите язык групп', reply_markup=mailing_languages())
    

# гланое меню кнопка 
@bot.message_handler(state="*", func=lambda message: message.text == 'Главное меню ↩️' or message.text == 'Далее')
def any_state(message: types.Message, state: StateContext):
    chat_id = message.chat.id

    if message.text == 'Главное меню ↩️':
        state.delete()
        bot.send_message(chat_id, 'Админ панель', reply_markup=admin_panel_btn())
    
    elif message.text == 'Далее':
        current_state = state.get()
        print(current_state)
        
        if current_state == "GroupMailing:language":
            state.set('GroupMailing:course')
            bot.send_message(chat_id, f"Выберите курс", reply_markup=mailing_courses())

            print(state.get())
                
        elif current_state == "GroupMailing:course":
            state.set('GroupMailing:message')
            bot.send_message(chat_id, f"Введите текст", reply_markup=go_back_or_continue_btns())


        elif current_state == "GroupMailing:message":
            state.set('GroupMailing:photos')
            bot.send_message(chat_id, f"Отправьте фото")
        
        elif current_state == "GroupMailing:photos":
            with state.data() as data:
                languages = data.get('language')
                courses = data.get('course')
                text = data.get('text')
                photos = data.get('photos')
            bot.send_message(chat_id, f'''
Язык: {languages}
Курс: {courses}
Текст: {text}
Фото: {photos}
''')

                        
@bot.message_handler(state=GroupMailing.language)
def get_language(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    if message.text == 'Все языки':
        state.add_data(language='Все языки')
        bot.send_message(chat_id, f"Выберите курс", reply_markup=mailing_courses())
        state.set('GroupMailing:course')
            
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


        bot.send_message(chat_id, f"<b>Выбранные языки:</b> {', '.join(chosen_languages)}", reply_markup=mailing_languages())
        

@bot.message_handler(state=GroupMailing.course) 
def course_state(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    
    if message.text == 'Все курсы':
        state.add_data(course='Все курсы')
        bot.send_message(chat_id, f"Введите текст", reply_markup=go_back_or_continue_btns())
        state.set(GroupMailing.message)
    
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

        bot.send_message(chat_id, f"<b>Выбранные курсы:</b> {', '.join(chosen_courses)}", reply_markup=mailing_courses())
        
    

@bot.message_handler(state=GroupMailing.message) 
def message_state(message: types.Message, state: StateContext):
    chat_id = message.chat.id

    with state.data() as data:
        text_sent = data.get("text")
        if not text_sent:
                text_sent = []
        
    if message.text not in text_sent:
        text_sent.append(message.text)
        state.add_data(text=text_sent)
    else:
        text_sent.remove(message.text)

    bot.send_message(chat_id, f'<b>Отправленный текст:</b> {text_sent[-1]}', reply_markup=go_back_or_continue_btns())


@bot.message_handler(state=GroupMailing.photos, content_types=['photo']) 
def photos_state(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    photo = message.photo[-1].file_id

    bot.send_photo(chat_id, photo=photo)



bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())

# necessary for state parameter in handlers.
from telebot.states.sync.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))
