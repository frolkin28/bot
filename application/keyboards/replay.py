'''This module contains telegram keyboards'''

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


from_location_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Мое метоположение', request_location=True)
        ],
        [
            KeyboardButton(text='Поиск'),
            KeyboardButton(text='Отмена заказа'),
            KeyboardButton(text='Прикрепить локацию')
        ]
    ],
    resize_keyboard=True
)

to_location_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Поиск'),
            KeyboardButton(text='Прикрепить локацию')
        ],
        [
            KeyboardButton(text='Отмена заказа')
        ]
    ],
    resize_keyboard=True
)