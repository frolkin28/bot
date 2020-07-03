from aiogram.dispatcher.filters.state import StatesGroup, State


class AddAdmin(StatesGroup):
    TELEGRAM_ID = State()
    NAME = State()
    USERNAME = State()


class DeleteAdmin(StatesGroup):
    TELEGRAM_ID = State()


class AddDriver(StatesGroup):
    TELEGRAM_ID = State()
    NAME = State()
    USERNAME = State()
    NUMBER = State()
    AUTO = State()
    PHONE = State()


class DeleteDriver(StatesGroup):
    TELEGRAM_ID = State()
