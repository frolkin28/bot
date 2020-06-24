import os
from telebot import TeleBot

import config

token = os.environ.get('token')
bot = TeleBot(token)