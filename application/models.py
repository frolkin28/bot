from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base

from application.constants import DriverStatus, UserStatus


Base = declarative_base()


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(255))
    username = Column(String(60))
    creator = Column(Boolean, nullable=False, default=False)


class Driver(Base):
    __tablename__ = 'driver'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(255))
    username = Column(String(60), nullable=True)
    number = Column(String(60), nullable=False)
    auto = Column(String(255))
    phone = Column(String(20))
    status = Column(Enum(DriverStatus), nullable=False,
                    default=DriverStatus.unavaliable)


# class User(db.Model):
#     id = Column(Integer, primary_key=True)
#     telegram_id = Column(Integer, unique=True, nullable=False)
#     username = Column(String(60))
#     status = Column(Enum)
