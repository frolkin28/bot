from .validators import check_admin, check_phone
from config import bot, db
from models import Driver, DriverStatus


@bot.message_handler(func=check_admin, commands=['add_driver'])
def add_driver(message):
	text = 'Отлично! Введи telegram id нового водителя'
	msg = bot.send_message(chat_id=message.chat.id, text=text)
	bot.register_next_step_handler(msg, driver_id_step)


def driver_id_step(message):
	dr = {}
	try:
		dr['telegram_id'] = int(message.text)
	except:
		msg = bot.send_message(chat_id=message.chat.id,
							   text='Введи правильный id')
		bot.register_next_step_handler(message, driver_id_step)
	else:
		text = 'Теперь введи имя водителя'
		msg = bot.send_message(chat_id=message.chat.id, text=text)
		bot.register_next_step_handler(msg, driver_name_step, driver=dr)


def driver_name_step(message, driver):
	dr = driver
	dr['name'] = message.text
	text = 'Теперь введи username админа без символа @'
	msg = bot.send_message(chat_id=message.chat.id, text=text)
	bot.register_next_step_handler(msg, driver_username_step, driver=dr)


def driver_username_step(message, driver):
	dr = driver
	dr['username'] = message.text
	text = 'Теперь введи номерной знак машины водителя'
	msg = bot.send_message(chat_id=message.chat.id, text=text)
	bot.register_next_step_handler(msg, driver_number_step, driver=dr)


def driver_number_step(message, driver):
	dr = driver
	dr['number'] = message.text
	text = 'Теперь введи описание машины'
	msg = bot.send_message(chat_id=message.chat.id, text=text)
	bot.register_next_step_handler(msg, driver_auto_step, driver=dr)


def driver_auto_step(message, driver):
	dr = driver
	dr['auto'] = message.text
	text = 'Теперь введи телефонный номер водителя'
	msg = bot.send_message(chat_id=message.chat.id, text=text)
	bot.register_next_step_handler(msg, driver_phone_step, driver=dr)


def driver_phone_step(message, driver):
	dr = driver
	if check_phone(message.text):
		dr['phone'] = message.text
		# dr['status'] = Status.unavaliable
		text = 'Новый водитель добавлен'
		bot.send_message(chat_id=message.chat.id, text=text)
		driver = Driver(**dr)
		db.session.add(driver)
		db.session.commit()
	else:
		msg = bot.send_message(chat_id=message.chat.id,
							   text='Введи правильный номер')
		bot.register_next_step_handler(msg, driver_phone_step, driver=dr)


@bot.message_handler(func=check_admin, commands=['show_drivers'])
def show_drivers(message):
	drivers = Driver.query.all()
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


@bot.message_handler(func=check_admin, commands=['delete_driver'])
def delete_driver(message):
	msg = bot.send_message(chat_id=message.chat.id, text='Введи id водителя')
	bot.register_next_step_handler(msg, driver_delete_step)


def driver_delete_step(message):
	try:
		telegram_id = int(message.text)
		driver = Driver.query.filter(Driver.telegram_id == telegram_id).first()
	except:
		bot.send_message(chat_id=message.chat.id, text='Такого водителя нет')
	else:
		db.session.delete(driver)
		db.session.commit()
		bot.send_message(chat_id=message.chat.id, text='Водитель удален')
