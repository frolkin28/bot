import os
import pydantic

from application import bot
from application.services import AdminService
from config import BASE_DIR
from entities import AdminEntity
from .validators import check_admin


@bot.message_handler(func=check_admin, commands=['show_commands'])
def show_commands(message):
    with open(str(BASE_DIR / 'admin' / 'commands.txt'), 'r') as f:
        text = f.read()
    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(func=check_admin, commands=['add_admin'])
def add_admin(message):
    text = 'Отлично! Введи telegram id нового админа'
    msg = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(msg, admin_id_step)


def admin_id_step(message):
    admin = {}
    admin['telegram_id'] = message.text
    text = 'Теперь введи имя админа'
    msg = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(msg, admin_name_step, admin=admin)


def admin_name_step(message, admin):
    admin['name'] = message.text
    text = 'Теперь введи username админа без символа @'
    msg = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(msg, admin_username_step, admin=admin)


def admin_username_step(message, admin):
    admin['username'] = message.text
    admin['creator'] = False
    try:
        new_admin = AdminEntity(**admin)
    except pydantic.ValidationError:
        bot.send_message(chat_id=message.chat.id,
                         text='Введены неверные данные, попробуй еще раз')
    else:
        service = AdminService()
        created_admin = service.create(new_admin)
    text = f'Админ {created_admin.name} добавлен!'
    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(func=check_admin, commands=['show_admins'])
def show_admins(message):
    service = AdminService()
    admins = service.get_all()
    for admin in admins:
        text = 'ID: {}\nName: {}\nUsername: {}'.format(
            str(admin.telegram_id), admin.name, admin.username)
        bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(func=check_admin, commands=['delete_admin'])
def delete_admin(message):
    msg = bot.send_message(chat_id=message.chat.id, text='Введи telegram id админа')
    bot.register_next_step_handler(msg, admin_delete_step)


def admin_delete_step(message):
    telegram_id = int(message.text)
    service = AdminService()
    admin = service.get_by_tg_id(telegram_id)
    if admin:
        if admin.creator:
            bot.send_message(chat_id=message.chat.id,
                            text='Нельзя удалить создателя')
        elif admin.telegram_id == int(message.from_user.id):
            bot.send_message(chat_id=message.chat.id,
                            text='Прости, но себя удалить нельзя')
        else:
            service.delete(admin.telegram_id)
            bot.send_message(chat_id=message.chat.id,
                        text=f'Админ {admin.name} удален!')
    else:
        bot.send_message(chat_id=message.chat.id,
            text=f'Такого админа не существует')



# @bot.message_handler(func=lambda  message: not message.startswith('/'))
# @bot.message_handler(func=check_admin)
# def admin(message):
#     bot.send_message(chat_id=message.chat.id, text='Hello, admin!')
