'''Hendlers for regular users'''

from aiogram import types

from application import dp
from application.keyboards import from_location_keyboard, to_location_keyboard
from application.states import MakeOrder
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(text='Я помогу тебе вызвать такси')


@dp.message_handler(commands=['make_order'])
async def make_order(message: types.Message):
    await MakeOrder.FROM.set()
    await message.answer(text='Откуда едем?', reply_markup=from_location_keyboard)


@dp.message_handler(state=MakeOrder.FROM, content_types=types.ContentType.LOCATION)
async def from_location(message: types.Message, state: FSMContext):
    async with state.proxy() as state:
        state['order'] = {'from_location': message.location}

    await MakeOrder.TO.set()
    await message.answer('Геолокация получена.\nКуда едем?', reply_markup=to_location_keyboard)


@dp.message_handler(state=MakeOrder.TO, content_types=types.ContentType.LOCATION)
async def share_to_location(message: types.Message, state: FSMContext):
    print(message.location)
    # async with state.proxy() as state:
    #     state['order']['to_location'] = message.get('location')

    await message.answer('Геолокация получена', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state='*', text='Отмена заказа')
async def cancel_order(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text='Заказ отменен', reply_markup=types.ReplyKeyboardRemove())
