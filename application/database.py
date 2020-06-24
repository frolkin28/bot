import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config


engine = create_engine(config.DATABASE_URI)

Session = sessionmaker(bind=engine)


@contextmanager
def current_session():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
