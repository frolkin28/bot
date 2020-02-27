from config import bot
from collections import defaultdict
from models import Admin, session


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Я помогу тебе вызвать такси")


@bot.message_handler(func=lambda x: True)
def user(message):
    bot.send_message(chat_id=message.chat.id, text='Hello, stranger!')
