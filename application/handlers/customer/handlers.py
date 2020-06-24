from config import bot
from models import Admin, User
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Я помогу тебе вызвать такси')


@bot.message_handler(commands=['make_order'])
def make_order(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    current_botton = InlineKeyboardButton(
        'Мое местоположение', callback_data='current')
    other_button = InlineKeyboardButton('Другое', callback_data='other')
    cancel_button = InlineKeyboardButton('Отмена', callback_data="cancel")
    markup.add(current_botton, other_button, cancel_button)
    bot.send_message(message.chat.id, "Откуда едем?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def callback_yes(call):
    bot.answer_callback_query(call.id, "Answer is Yes")


@bot.message_handler(func=lambda x: True)
def user(message):
    bot.send_message(chat_id=message.chat.id, text='Hello, stranger!')
