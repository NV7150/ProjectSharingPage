from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import enum

import os
from contextlib import contextmanager


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


class ThreadType(str, enum.Enum):
    OPENCHAT = 'THREADTYPE_OPENCHAT'
    ANNOUNCE = 'THREADTYPE_ANNOUNCE'
    PROBLEMS = 'THREADTYPE_PROBLEMS'


class ThreadStatus(str, enum.Enum):
    OPEN = 'THREADSTATUS_OPEN'
    CLOSED = 'THREADSTATUS_CLOSED'


class Thread(Base):
    """[DB] Thread Class

    Parameters
    ----------
    id: int (auto)
    type: ThreadType (str)
    status: ThreadStatus (str)
    project_id: int
    title: str
    """
    __tablename__ = 'thread'
    id = Column('id', Integer, primary_key=True)
    type = Column('type', String, nullable=False, default=ThreadType.OPENCHAT)
    status = Column(
        'status', String, nullable=False, default=ThreadStatus.OPEN
    )
    project_id = Column('project_id', Integer, nullable=False)
    title = Column('title', String, nullable=False)
    messages = relationship('Message', backref='thread')


class Message(Base):
    """[DB] Message (in Thread) Class

    Parameters
    ----------
    id: int
    thread: Thread
    username: str
    content: str
    created_at: datetime
    """
    __tablename__ = 'message'
    id = Column('id', Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey('thread.id'))
    username = Column('username', String, nullable=False)
    content = Column('content', String, nullable=False)
    created_at = Column('created_at', DateTime, nullable=False)
