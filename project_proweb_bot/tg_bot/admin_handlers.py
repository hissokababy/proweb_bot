import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.storage import StateMemoryStorage
from telebot.types import ReplyParameters

from common.kbds import admin_panel_btn, mailing_courses, mailing_languages, main_btns_inline, main_btns_reply
from common.texts import texts
from tg_bot.services.admin import admin_confirm, is_admin
from tg_bot.services.user import get_user_lang
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
    

# гланое меню кнопка 
@bot.message_handler(state="*", func=lambda message: message.text == 'Главное меню ↩️' or message.text == 'Далее')
def any_state(message: types.Message, state: StateContext):
    num = 0
    if message.text == 'Главное меню ↩️':
        state.delete()
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Админ панель', reply_markup=admin_panel_btn())
    
    elif message.text == 'Далее':
        print(state.get())


@bot.message_handler(state=GroupMailing.language)
def get_language(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    state.add_data(language=message.text)

    with state.data() as data:
        chosen_languages = data.get("language")
    bot.send_message(chat_id, f'Выбранные языки {chosen_languages}')



    # if not text in chosen_languages:
    #         chosen_languages.append(text)

    #         if text != '\n*Все языки' and '\n*Все языки' in chosen_languages:
    #             chosen_languages.remove('\n*Все языки')

    #         elif text == '\n*Все языки' and chosen_languages[-1]:
    #             chosen_languages.clear()
    #             chosen_languages.append(text)

    #         bot.send_message(chat_id, f"Выбранные языки: {' '.join(chosen_languages)}")
    # else:
    #     chosen_languages.remove(text)
    #     if chosen_languages[-1]:
    #         bot.send_message(chat_id, f"Выбранные языки: {' '.join(chosen_languages)}")


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())

# necessary for state parameter in handlers.
from telebot.states.sync.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))

