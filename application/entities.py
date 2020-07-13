'''This module contains classes for representation database models and making data validation'''

import pydantic
import typing
import re

from application import constants


class AdminEntity(pydantic.BaseModel):
    id: typing.Optional[int]
    telegram_id: int
    name: str
    username: str
    creator: bool = False

    class Config:
        orm_mode = True


class DriverEntity(pydantic.BaseModel):
    id: typing.Optional[int]
    telegram_id: int
    name: str
    username: str
    number: str
    auto: str
    phone: str
    status: constants.DriverStatus = constants.DriverStatus.unavaliable

    class Config:
        orm_mode = True

    @pydantic.validator('phone')
    def check_phone(cls, value):
        pattern = re.compile(r'\+380\d{9}')
        phone = pattern.fullmatch(value)
        if not phone:
            raise ValueError('Should be an Ukrainian number')
        return value

