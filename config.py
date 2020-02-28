import os
from telebot import TeleBot
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:012810@localhost/taxibot'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


token = os.environ.get('token')
bot = TeleBot(token)
BASE_DIR = os.getcwd()


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
