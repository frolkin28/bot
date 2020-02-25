from validators import check_admin
from config import bot
from collections import defaultdict

START, TG_ID, NAME, USERNAME = range(4)

ADMIN_STATE = defaultdict(lambda: START)


def get_state(message):
    return ADMIN_STATE[message.chat.id]


def set_state(message, state):
    ADMIN_STATE[message.chat.id] = state


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Я помогу тебе вызвать такси")


@bot.message_handler(func=check_admin)
def admin(message):
    print(message.from_user.id, message.from_user.username)
    # bot.send_message(chat_id=message.chat.id, text='Hello, admin!')


@bot.message_handler(func=lambda x: True)
def user(message):
    bot.send_message(chat_id=message.chat.id, text='Hello, stranger!')


@bot.message_handler(func=check_admin, commands=['add_admin'])
def add_admin(message):
    pass
