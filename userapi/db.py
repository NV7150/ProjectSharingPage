from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta

import os
from contextlib import contextmanager


PG_USER = os.environ.get('POSTGRES_USER')
PG_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_URL = f'postgresql://{PG_USER}:{PG_PASSWORD}@db'
DB_ECHO = (os.environ.get('DB_ECHO') != 'False')

engine = create_engine(
    DB_URL,
    echo=DB_ECHO
)

Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=True, bind=engine)
)


@contextmanager
def session_scope() -> scoped_session:
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


Base: DeclarativeMeta = declarative_base()
