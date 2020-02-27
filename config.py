from telebot import TeleBot
import os

token = os.environ.get('token')
bot = TeleBot(token)
BASE_DIR = os.getcwd()
