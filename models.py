from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///admins.db')
Base = declarative_base()
session = sessionmaker(bind=engine)()


class Admin(Base):
    __tablename__ = 'admins'

    id = Column('id', Integer, primary_key=True)
    telegram_id = Column('telegram_id', Integer, unique=True, nullable=False)
    name = Column('name', String(255))
    username = Column('username', String)
    creator = Column('creator', Boolean, nullable=False)


class Driver(Base):
    __tablename__ = 'drivers'

    id = Column('id', Integer, primary_key=True)
    telegram_id = Column('telegram_id', Integer, unique=True, nullable=False)
    name = Column('name', String(255))
    username = Column('username', String, nullable=True)
    number = Column('number', String(60), nullable=False)
    auto = Column('auto', String(255))


class User_state(Base):
    __tablename__ = 'user_state'

    id = Column('id', Integer, primary_key=True)
