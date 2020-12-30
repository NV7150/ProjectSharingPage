from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
import enum

import os
from contextlib import contextmanager
from typing import Any, List, Optional


PG_USER = os.environ.get('POSTGRES_USER')
PG_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_URL = f'postgresql://{PG_USER}:{PG_PASSWORD}@chatdb'
DB_ECHO = (os.environ.get('DB_ECHO') != 'False')

engine = create_engine(
    DB_URL,
    echo=DB_ECHO,
)

Session = scoped_session(
    sessionmaker(
        autocommit=False, autoflush=True,
        bind=engine, expire_on_commit=False,
    )
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


class ThreadType(int, enum.Enum):
    OPENCHAT = 1
    ANNOUNCE = 2
    PROBLEMS = 3


class ThreadStatus(int, enum.Enum):
    OPEN = 1
    CLOSED = 2


class Thread(Base):
    """[DB] Thread Class

    Parameters
    ----------
    id: int (auto)
    type: ThreadType (int)
    status: ThreadStatus (int)
    title: str
    """
    __tablename__ = 'thread'
    id = Column('id', Integer, primary_key=True)
    type = Column('type', Integer, nullable=False)
    status = Column(
        'status', Integer, nullable=False, default=ThreadStatus.OPEN
    )
    title = Column('title', String, nullable=False)
    messages = relationship('Message', backref='thread')


class Message(Base):
    """[DB] Message (in Thread) Class

    Parameters
    ----------
    id: int
    thread: Thread
    content: str
    created_at: datetime
    """
    __tablename__ = 'message'
    id = Column('id', Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey('thread.id'))
    content = Column('content', String, nullable=False)
    created_at = Column('created_at', DateTime, nullable=False)
