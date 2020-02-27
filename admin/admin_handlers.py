from admin.validators import check_admin
from config import bot, BASE_DIR
from models import Admin, session
import os


@bot.message_handler(func=check_admin, commands=['show_commands'])
def show_commands(message):
    with open(os.path.join(BASE_DIR, 'admin/', 'commands.txt'), 'r') as f:
        text = f.read()
    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(func=check_admin, commands=['add_admin'])
def add_admin(message):
    text = 'Отлично! Введи telegram id нового админа'
    msg = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(msg, admin_id_step)


def admin_id_step(message):
    ad = {}
    try:
        ad['telegram_id'] = int(message.text)
    except:
        msg = bot.send_message(chat_id=message.chat.id,
                               text='Введи правильный id')
        bot.register_next_step_handler(msg, admin_id_step)
    else:
        text = 'Теперь введи имя админа'
        msg = bot.send_message(chat_id=message.chat.id, text=text)
        bot.register_next_step_handler(msg, admin_name_step, admin=ad)


def admin_name_step(message, admin):
    ad = admin
    ad['name'] = message.text
    text = 'Теперь введи username админа без символа @'
    msg = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(msg, admin_username_step, admin=ad)


def admin_username_step(message, admin):
    ad = admin
    ad['username'] = message.text
    text = 'Новый админ добавлен'
    admin = Admin(telegram_id=ad['telegram_id'],
                  name=ad['name'], username=ad['username'], creator=False)
    session.add(admin)
    session.commit()
    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(func=check_admin, commands=['show_admins'])
def show_admins(message):
    admins = session.query(Admin).all()
    for admin in admins:
        text = 'ID: {}\nName: {}\nUsername: {}'.format(
            str(admin.telegram_id), admin.name, admin.username)
        bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(func=check_admin, commands=['delete_admin'])
def delete_admin(message):
    msg = bot.send_message(chat_id=message.chat.id, text='Введи id админа')
    bot.register_next_step_handler(msg, admin_delete_step)


def admin_delete_step(message):
    telegram_id = int(message.text)
    admin = session.query(Admin).filter(
        Admin.telegram_id == telegram_id).one()
    if admin.creator == True:
        bot.send_message(chat_id=message.chat.id,
                         text='Нельзя удалить создателя')
    elif admin.telegram_id == int(message.from_user.id):
        bot.send_message(chat_id=message.chat.id,
                         text='Прости, но себя удалить нельзя')
    else:
        session.delete(admin)
        session.commit()
        bot.send_message(chat_id=message.chat.id, text='Админ удален')


@bot.message_handler(func=check_admin)
def admin(message):
    bot.send_message(chat_id=message.chat.id, text='Hello, admin!')
