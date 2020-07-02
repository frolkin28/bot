from application import bot
from application.services import DriverService, DriversQueueService
from application.constants import DriverStatus
from .validators import check_driver


@bot.message_handler(func=check_driver, commands=['start_shift'])
def start_shift(message):
    telegram_id = message.from_user.id

    DriverService().set_status(telegram_id, DriverStatus.avaliable)
    DriversQueueService().push(telegram_id)

    bot.send_message(
        chat_id=message.chat.id,
        text='Вы начали смену и добавлены в очередь на получение заказа, ожидайте',
    )


@bot.message_handler(func=check_driver, commands=['end_shift'])
def end_shift(message):
    telegram_id = message.from_user.id

    DriverService().set_status(telegram_id, DriverStatus.unavaliable)
    result = DriversQueueService().remove(telegram_id)
    if result:
        bot.send_message(
            chat_id=message.chat.id, text='Вы закончили смену и убраны из очереди на заказ'
        )
    else:
        bot.send_message(
            chat_id=message.chat.id, text='Что-то пошло не так, попробуйте еще раз'
        )

