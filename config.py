from telebot import TeleBot
from os import environ

token = environ.get('token')
bot = TeleBot(token)
