import pydantic
import typing

from application import constants


class AdminEntity(pydantic.BaseModel):
    id: typing.Optional[int]
    telegram_id: int
    name: str
    username: str
    creator: bool

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
