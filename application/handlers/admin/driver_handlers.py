import pydantic

from .validators import check_admin
from application import bot
from application.services import DriverService
from application.entities import DriverEntity


@bot.message_handler(func=check_admin, commands=['add_driver'])
def add_driver(message):
    text = 'Отлично! Введи telegram id нового водителя'
    msg = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(msg, driver_id_step)


def driver_id_step(message):
    driver = {}
    driver['telegram_id'] = message.text
    text = 'Теперь введи имя водителя'
    msg = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(msg, driver_name_step, driver=driver)


def driver_name_step(message, driver):
    driver['name'] = message.text
    text = 'Теперь введи username админа без символа @'
    msg = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(msg, driver_username_step, driver=driver)


def driver_username_step(message, driver):
    driver['username'] = message.text
    text = 'Теперь введи номерной знак машины водителя'
    msg = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(msg, driver_number_step, driver=driver)


def driver_number_step(message, driver):
    driver['number'] = message.text
    text = 'Теперь введи описание машины'
    msg = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(msg, driver_auto_step, driver=driver)


def driver_auto_step(message, driver):
    driver['auto'] = message.text
    text = 'Теперь введи телефонный номер водителя (+380...)'
    msg = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(msg, driver_phone_step, driver=driver)


def driver_phone_step(message, driver):
    driver['phone'] = message.text
    try:
        new_driver = DriverEntity(**driver)
    except pydantic.ValidationError:
        bot.send_message(chat_id=message.chat.id,
                         text='Введены неправильные данные')
    else:
        service = DriverService()
        created_driver = service.craete(new_driver)
        if created_driver:
            text = f'Водитель {created_driver.name} добавлен'
        else:
            text = 'Такой водитель уже существует'
        bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(func=check_admin, commands=['show_drivers'])
def show_drivers(message):
    service = DriverService()
    drivers = service.get_all()
    if drivers:
        for driver in drivers:
            text = 'ID: {} | Name: {}\nUsername: {} | Phone: {}\nNumber: {} | Auto: {}\nStatus: {}'.format(
                str(driver.telegram_id),
                driver.name,
                driver.username,
                driver.phone,
                driver.number,
                driver.auto,
                driver.status.name
            )
            bot.send_message(chat_id=message.chat.id, text=text)
    else:
        bot.send_message(chat_id=message.chat.id, text='Нет водителей') 


@bot.message_handler(func=check_admin, commands=['delete_driver'])
def delete_driver(message):
    msg = bot.send_message(chat_id=message.chat.id, text='Введи telegram id водителя')
    bot.register_next_step_handler(msg, driver_delete_step)


def driver_delete_step(message):
    try:
        telegram_id = int(message.text)
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text='Неверный telegram id. Попробуй еще раз')
    else:
        service = DriverService()
        result = service.delete(telegram_id)
        if result:
            bot.send_message(chat_id=message.chat.id, text='Водитель удален')
        else:
            bot.send_message(chat_id=message.chat.id, text='Такого водителя нет')



        
