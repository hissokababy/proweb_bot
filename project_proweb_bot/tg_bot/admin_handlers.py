import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.storage import StateMemoryStorage
from telebot.types import ReplyParameters

from common.kbds import admin_panel_btn, continue_or_back, mailing_courses, mailing_languages, main_btns_inline, main_btns_reply
from common.texts import texts
from tg_bot.utils import admin_confirm, get_user_lang, is_admin
from tg_bot.bot import bot



@bot.message_handler(commands=['start'])
def admin_start_panel(message: types.Message):
    chat_id = message.chat.id
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



@bot.message_handler(func=lambda message: message.text == 'Рассылка в группы студентов')
def group_mailing(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    state.set(GroupMailing.language)
    
    if is_admin(chat_id):
        bot.send_message(chat_id, 'Выберите язык групп', reply_markup=mailing_languages())


@bot.message_handler(state="*", func=lambda message: message.text == 'Главное меню ↩️')
def any_state(message: types.Message, state: StateContext):
    state.delete()
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Админ панель', reply_markup=admin_panel_btn())


# @bot.message_handler(state="*", func=lambda call: call.data.startswith('state_'))
# def any_state2(call: types.CallbackQuery, state: StateContext):
#     chat_id = call.message.chat.id
#     action = call.data.split('_')[-1]

#     if action == 'add':

chosen_languages = []
@bot.message_handler(state=GroupMailing.language)
def get_language(message: types.Message):
    chat_id = message.chat.id
    text = '\n*' + message.text

    if not text in chosen_languages:
            chosen_languages.append(text)

            if text != '\n*Все языки' and '\n*Все языки' in chosen_languages:
                chosen_languages.remove('\n*Все языки')
                
            elif text == '\n*Все языки' and chosen_languages[-1]:
                chosen_languages.clear()
                chosen_languages.append(text)

            bot.send_message(chat_id, f'Вы выбрали {text}')
            bot.send_message(chat_id, f"Выбранные языки: {' '.join(chosen_languages)}", reply_markup=continue_or_back())
    else:
        chosen_languages.remove(text)
        if chosen_languages[-1]:
            bot.send_message(chat_id, f'Вы убрали {text}')
            bot.send_message(chat_id, f"Выбранные языки: {' '.join(chosen_languages)}", reply_markup=continue_or_back())


    print(chosen_languages)
    # bot.send_message(chat_id, f'Выберите курс', reply_markup=mailing_courses())
    # state.add_data(language=message.text)


# @bot.message_handler(state=GroupMailing.course)
# def get_course(message: types.Message, state: StateContext):
#     chat_id = message.chat.id

#     bot.send_message(chat_id, f'Теперь Введите сообщение')
#     state.add_data(language=message.text)








bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())

# necessary for state parameter in handlers.
from telebot.states.sync.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))


# import time
# from tg_bot.bot import bot

# from tg_bot.models import UserAdmin

# from telebot import types
# from common.texts import texts
# from common.kbds import continue_or_back, go_back, mailing_languages, admin_panel_btn
# from telebot.types import ReplyKeyboardRemove
# from tg_bot.utils import admin_confirm, get_user_lang, is_admin


# @bot.callback_query_handler(func=lambda call: call.data == 'confirm')
# def admin_panel(call: types.CallbackQuery):

#     chat_id = call.message.chat.id
#     bot.send_message(chat_id, 'Админ панель', reply_markup=admin_panel_btn())
#     admin_confirm(chat_id)


# from telebot.storage import StateMemoryStorage
# from telebot.states import State, StatesGroup
# from telebot.states.sync.context import StateContext

# state_storage = StateMemoryStorage()



# class GroupMailing(StatesGroup):
#     language = State()


# msg_id = None
# # рассылка в группы
# @bot.message_handler(func=lambda message: message.text == 'Рассылка в группы студентов')
# def private_mailing(message: types.Message):
#     chat_id = message.chat.id

#     if is_admin(chat_id):
#         # state.set(GroupMailing.language)
#         bot.send_message(chat_id, 'Давайте уточним детали', reply_markup=go_back())
#         msg = bot.send_message(chat_id, 'Выберите язык групп', reply_markup=mailing_languages())
#         global msg_id
#         msg_id = msg.message_id


# @bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
# def language_state(call: types.CallbackQuery):
#     chat_id = call.message.chat.id
#     if call.data == 'lang_all':
#         bot.send_message(chat_id, f'Вы выбрали Все языки', reply_markup=continue_or_back())
#         print(msg_id)
#         bot.delete_message(chat_id, message_id=msg_id)




# # chosen = []
# # msg_id = None
# # @bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
# # def language_state(call: types.CallbackQuery):
# #     chat_id = call.message.chat.id
# #     inlines = call.message.json['reply_markup']['inline_keyboard']
# #     data = call.data.split('_')[-1]
# #     # chosen.clear()
# #     # msg_id = None

# #     btns = []
# #     for i in inlines:
# #         btns.append(*i)
    
# #     for i in btns:
# #         if call.data in i['callback_data']:
# #             text = i['text']
# #             if not i['text'] in chosen:
# #                 chosen.append(i['text'])
# #                 if not msg_id:
# #                     msg = bot.send_message(chat_id, f"Вы выбрали {', '.join(chosen)}", reply_markup=continue_or_back())
# #                     msg_id = msg.message_id
# #                     time.sleep(3)
# #                     bot.delete_message(chat_id, message_id=msg_id)
# #                     msg_id = None
# #                 # else:
# #                 #     bot.delete_message(chat_id, message_id=msg_id)
# #                 #     bot.send_message(chat_id, f"Вы выбрали {', '.join(chosen)}", reply_markup=continue_or_back())

# #             # else:   
# #             #     chosen.remove(i['text'])
# #             #     if chosen != []:
# #             #         msg = bot.send_message(chat_id, f"Вы выбрали {', '.join(chosen)}")

# #             #     bot.delete_message(chat_id, message_id=msg.message_id)


# @bot.message_handler(func=lambda message: message.text == 'Назад ↩️')
# def go_back_state(message: types.Message):
#     chat_id = message.chat.id

#     if is_admin(chat_id):
#         bot.send_message(chat_id, 'Админ панель', reply_markup=admin_panel_btn())
