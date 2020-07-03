import pydantic

from aiogram import types
from aiogram.dispatcher import FSMContext

from .validators import check_admin
from application import dp
from application.services import DriverService
from application.entities import DriverEntity
from application.constants import DriverStatus
from application.states import AddDriver, DeleteDriver


@dp.message_handler(check_admin, commands=['add_driver'])
async def add_driver(message: types.Message):
    text = 'Отлично! Введи telegram id нового водителя'
    await AddDriver.TELEGRAM_ID.set()
    await message.answer(text=text)


@dp.message_handler(check_admin, state=AddDriver.TELEGRAM_ID)
async def driver_id_step(message: types.Message, state: FSMContext):
    telegram_id = message.text
    async with state.proxy() as state:
        state['driver'] = {'telegram_id': telegram_id}

    text = 'Теперь введи имя водителя'
    await AddDriver.NAME.set()
    await message.answer(text=text)


@dp.message_handler(check_admin, state=AddDriver.NAME)
async def driver_name_step(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as state:
        state['driver']['name'] = name

    text = 'Теперь введи username админа без символа @'
    await AddDriver.USERNAME.set()
    await message.answer(text=text)


@dp.message_handler(check_admin, state=AddDriver.USERNAME)
async def driver_username_step(message: types.Message, state: FSMContext):
    username = message.text
    async with state.proxy() as state:
        state['driver']['username'] = username

    text = 'Теперь введи номерной знак машины водителя'
    await AddDriver.NUMBER.set()
    await message.answer(text=text)


@dp.message_handler(check_admin, state=AddDriver.NUMBER)
async def driver_number_step(message: types.Message, state: FSMContext):
    number = message.text
    async with state.proxy() as state:
        state['driver']['number'] = number

    text = 'Теперь введи описание машины'
    await AddDriver.AUTO.set()
    await message.answer(text=text)


@dp.message_handler(check_admin, state=AddDriver.AUTO)
async def driver_auto_step(message: types.Message, state: FSMContext):
    auto = message.text
    async with state.proxy() as state:
        state['driver']['auto'] = auto

    text = 'Теперь введи телефонный номер водителя (+380...)'
    await AddDriver.PHONE.set()
    await message.answer(text=text)


@dp.message_handler(check_admin, state=AddDriver.PHONE)
async def driver_phone_step(message: types.Message, state: FSMContext):
    phone = message.text
    data = await state.get_data()
    driver = data.get('driver')
    driver['phone'] = phone
    await state.finish()
    try:
        new_driver = DriverEntity(**driver)
    except pydantic.ValidationError:
        await message.answer(text='Введены неправильные данные')
    else:
        service = DriverService()
        created_driver = service.craete(new_driver)
        if created_driver:
            text = f'Водитель {created_driver.name} добавлен'
        else:
            text = 'Такой водитель уже существует'
        await message.answer(text=text)


@dp.message_handler(check_admin, commands=['show_drivers'])
async def show_drivers(message: types.Message):
    drivers = DriverService().get_all()
    if drivers:
        for driver in drivers:
            text = 'ID: {} | Name: {}\nUsername: {} | Phone: {}\nNumber: {} | Auto: {}\nStatus: {}'.format(
                driver.telegram_id,
                driver.name,
                driver.username,
                driver.phone,
                driver.number,
                driver.auto,
                driver.status.name
            )
            await message.answer(text=text)
    else:
        await message.answer(text='Нет водителей')


@dp.message_handler(check_admin, commands=['delete_driver'])
async def delete_driver(message: types.Message):
    await DeleteDriver.TELEGRAM_ID.set()
    await message.answer(text='Введи telegram id водителя')


@dp.message_handler(check_admin, state=DeleteDriver.TELEGRAM_ID)
async def driver_delete_step(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        telegram_id = int(message.text)
    except ValueError:
        await message.answer(text='Неверный telegram id. Попробуй еще раз')
    else:
        result = DriverService().delete(telegram_id)
        if result:
            text = 'Водитель удален'
        else:
            text = 'Такого водителя нет'
        await message.answer(text=text)


@dp.message_handler(check_admin, commands=['avaliable_drivers'])
async def avaliable_drivers(message):
    drivers = DriverService().get_by_status(DriverStatus.avaliable)
    if drivers:
        for driver in drivers:
            text = 'ID: {} | Name: {}\nNumber: {} | Auto: {}'.format(
                driver.telegram_id,
                driver.name,
                driver.number,
                driver.auto
            )
            await message.answer(text=text)
    else:
        await message.answer(text='Нет доступных водителей')
