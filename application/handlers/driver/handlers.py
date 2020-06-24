from collections import deque
from config import db, bot
from models import Driver, DriverStatus
from .validators import check_driver
from admin.validators import check_admin

drivers_queue = deque()


@bot.message_handler(func=check_admin, commands=['avaliable_drivers'])
def avaliable_drivers(message):
    if len(drivers_queue):
        for driver_id in drivers_queue:
            driver = Driver.query.filter_by(telegram_id=driver_id).first()
            text = 'ID: {} | Name: {}\nNumber: {} | Auto: {}\nStatus: {}'.format(
                str(driver.telegram_id),
                driver.name,
                driver.number,
                driver.auto,
                driver.status.name
            )
            bot.send_message(chat_id=message.chat.id, text=text)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Нет доступных водителей')


@bot.message_handler(func=check_driver, commands=['start_shift'])
def start_shift(message):
    driver = Driver.query.filter(
        Driver.telegram_id == message.from_user.id).first()
    if driver.status == DriverStatus.unavaliable:
        driver.status = DriverStatus.avaliable
        db.session.add(driver)
        db.session.commit()
        if driver.telegram_id not in drivers_queue:
            drivers_queue.append(driver.telegram_id)
        bot.send_message(
            chat_id=message.chat.id,
            text='Вы начали смену и добавлены в очередь на получение заказа, ожидайте',
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='Вы уже начали смену',
        )


@bot.message_handler(func=check_driver, commands=['end_shift'])
def end_shift(message):
    driver = Driver.query.filter(
        Driver.telegram_id == message.from_user.id).first()
    if driver.status == DriverStatus.avaliable:
        driver.status = DriverStatus.unavaliable
        db.session.add(driver)
        db.session.commit()
        if driver.telegram_id in drivers_queue:
            drivers_queue.remove(driver.telegram_id)
        bot.send_message(
            chat_id=message.chat.id, text='Вы закончили смену и убраны из очереди на заказ'
        )
    else:
        bot.send_message(
            chat_id=message.chat.id, text='Вы уже закончили смену'
        )
