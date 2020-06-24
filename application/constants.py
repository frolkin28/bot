import enum


class DriverStatus(enum.Enum):
    avaliable = enum.auto()
    processing_order = enum.auto()
    unavaliable = enum.auto()


class UserStatus(enum.Enum):
    start = enum.auto()
    destination = enum.auto()
    phone = enum.auto()
    confirmation = enum.auto()
