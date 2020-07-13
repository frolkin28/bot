'''Handlers for drivers'''

from aiogram import types

from application import dp
from application.services import DriverService, DriversQueueService
from application.constants import DriverStatus
from .validators import check_driver


@dp.message_handler(check_driver, commands=['start_shift'])
async def start_shift(message: types.Message):
    telegram_id = message.from_user.id

    DriverService().set_status(telegram_id, DriverStatus.avaliable)
    DriversQueueService().push(telegram_id)

    await message.answer(
        text='Вы начали смену и добавлены в очередь на получение заказа, ожидайте',
    )


@dp.message_handler(check_driver, commands=['end_shift'])
async def end_shift(message: types.Message):
    telegram_id = message.from_user.id

    DriverService().set_status(telegram_id, DriverStatus.unavaliable)
    result = DriversQueueService().remove(telegram_id)
    if result:
        text='Вы закончили смену и убраны из очереди на заказ'
    else:
        text='Что-то пошло не так, попробуйте еще раз'

    await message.answer(text=text)
