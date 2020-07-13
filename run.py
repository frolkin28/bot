'''Entrypoint to the application'''

from aiogram import executor

from application import dp


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
