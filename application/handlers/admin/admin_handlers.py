import os
import pydantic

from aiogram import types
from aiogram.dispatcher import FSMContext

from application import dp
from application.services import AdminService
from application.states import AddAdmin, DeleteAdmin
from config import BASE_DIR
from application.entities import AdminEntity
from .validators import check_admin


@dp.message_handler(check_admin, commands=['show_commands'])
async def show_commands(message: types.Message):
    file_path = str(BASE_DIR / 'application' /
                    'handlers' / 'admin' / 'commands.txt')
    with open(file_path, 'r') as f:
        text = f.read()
    await message.answer(text=text)


@dp.message_handler(check_admin, commands=['add_admin'])
async def add_admin(message: types.Message):
    text = 'Отлично! Введи telegram_id нового админа'
    await AddAdmin.TELEGRAM_ID.set()
    await message.answer(text=text)


@dp.message_handler(check_admin, state=AddAdmin.TELEGRAM_ID)
async def admin_id_step(message: types.Message, state: FSMContext):
    telegram_id = message.text

    async with state.proxy() as state:
        state['admin'] = {'telegram_id': telegram_id}
    text = 'Теперь введи имя админа'

    await AddAdmin.NAME.set()
    await message.answer(text=text)


@dp.message_handler(check_admin, state=AddAdmin.NAME)
async def admin_name_step(message: types.Message, state: FSMContext):
    name = message.text

    async with state.proxy() as state:
        state['admin']['name'] = name

    text = 'Теперь введи username админа без символа @'
    await AddAdmin.USERNAME.set()
    await message.answer(text=text)


@dp.message_handler(check_admin, state=AddAdmin.USERNAME)
async def admin_username_step(message: types.Message, state: FSMContext):
    username = message.text
    data = await state.get_data()
    admin = data.get('admin')
    admin['username'] = username
    await state.finish()
    try:
        new_admin = AdminEntity(**admin)
    except pydantic.ValidationError:
        await message.answer(text='Введены неверные данные, попробуй еще раз')
    else:
        created_admin = AdminService().create(new_admin)
        if created_admin:
            text = f'Админ {created_admin.name} добавлен!'
        else:
            text = 'Такой админ уже существует'

        await message.answer(text=text)


@dp.message_handler(check_admin, commands=['show_admins'])
async def show_admins(message: types.Message):
    admins = AdminService().get_all()
    if admins:
        for admin in admins:
            text = 'ID: {}\nName: {}\nUsername: {}'.format(
                str(admin.telegram_id), admin.name, admin.username)
            await message.answer(text=text)
    else:
        await message.answer(text='Пока нет админов')


@dp.message_handler(check_admin, commands=['delete_admin'])
async def delete_admin(message: types.Message):
    await DeleteAdmin.TELEGRAM_ID.set()
    await message.answer(text='Введи telegram id админа')


@dp.message_handler(check_admin, state=DeleteAdmin.TELEGRAM_ID)
async def admin_delete_step(message: types.Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        service = AdminService()
        admin = service.get_by_tg_id(telegram_id)
        if admin:
            if admin.creator:
                text = 'Нельзя удалить создателя'
            elif admin.telegram_id == int(message.from_user.id):
                text='Прости, но себя удалить нельзя'
            else:
                service.delete(admin.telegram_id)
                text=f'Админ {admin.name} удален!'
        else:
            text=f'Такого админа не существует'
    except ValueError:
        text=f'Неверный telegram id. Попробуй еще раз'

    await state.finish()
    await message.answer(text=text)


# @bot.message_handler(func=lambda  message: not message.startswith('/'))
# @bot.message_handler(func=check_admin)
# def admin(message):
#     bot.send_message(chat_id=message.chat.id, text='Hello, admin!')
