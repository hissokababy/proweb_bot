from telebot.states import State, StatesGroup


class GroupMailing(StatesGroup):
    language = State()
    course = State()
    post = State()
    sending = State()
    forwarding = State()