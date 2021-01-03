from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

import os
from contextlib import contextmanager
from typing import Any, List, Optional


PG_USER = os.environ.get('POSTGRES_USER')
PG_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_URL = f'postgresql://{PG_USER}:{PG_PASSWORD}@projectdb'
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


class Like(Base):
    """[DB] Like for Project

    Parametes
    ---------
    id: int (auto)
    username: str
    project: int
        foreign key (Project)
    """
    __tablename__ = 'like'
    id = Column('id', Integer, primary_key=True)
    username = Column('username', String, nullable=False)
    project_id = Column('project_id', ForeignKey('project.id'))


class ProjectUser(Base):
    """Association object
    """
    __tablename__ = 'project_user'
    project_id = Column(
        Integer, ForeignKey('project.id'),
        primary_key=True, nullable=False,
    )
    username = Column(
        'username', String, nullable=False,
        primary_key=True,
    )


class ProjectAnnounceUser(Base):
    """Association object
    """
    __tablename__ = 'project_announce_user'
    project_id = Column(
        Integer, ForeignKey('project.id'),
        primary_key=True, nullable=False,
    )
    username = Column(
        'username', String, nullable=False,
        primary_key=True,
    )


class ProjectAdminUser(Base):
    """Association object
    """
    __tablename__ = 'project_admin_user'
    project_id = Column(
        Integer, ForeignKey('project.id'),
        primary_key=True, nullable=False,
    )
    username = Column(
        'username', String, nullable=False,
        primary_key=True,
    )


class Project(Base):
    """[DB] Project Class

    Parameters
    ----------
    id: int (auto)
    title: str
    subtitle: Optional[str]
    bg_image: Optional[str]
    description: str
    members: List[str]
        list of username
    likes: List[Like]
        list of username

    twitter: Optional[str]
    instagram: Optional[str]
    github: Optional[str]
    youtube: Optional[str]
    vimeo: Optional[str]
    facebook: Optional[str]
    tiktok: Optional[str]
    linkedin: Optional[str]
    wantedly: Optional[str]
    url: Optional[str]

    skilltags: List[int]
        list of skilltag id
    is_active: bool (default: True)
        set false when logically deleted
    """
    __tablename__ = 'project'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, nullable=False)
    subtitle = Column('subtitle', String, nullable=True)
    bg_image = Column('bg_image', String, nullable=True)
    description = Column('description', String, nullable=False)
    members = relationship('ProjectUser', backref='project')
    announce_users = relationship('ProjectAnnounceUser', backref='project')
    admin_users = relationship('ProjectAdminUser', backref='project')
    likes = relationship('Like', backref='project')

    # SNS
    twitter = Column('twitter', String, nullable=True)
    instagram = Column('instagram', String, nullable=True)
    github = Column('github', String, nullable=True)
    youtube = Column('youtube', String, nullable=True)
    vimeo = Column('vimeo', String, nullable=True)
    facebook = Column('facebook', String, nullable=True)
    tiktok = Column('tiktok', String, nullable=True)
    linkedin = Column('linkedin', String, nullable=True)
    wantedly = Column('wantedly', String, nullable=True)
    url = Column('url', String, nullable=True)

    # skill
    __skilltags = Column('skilltags', String, nullable=False)
    is_active = Column('is_active', Boolean, nullable=False, default=True)

    @property
    def skilltags(self) -> List[int]:
        return [
            int(tag.replace(' ', ''))
            for tag in self.__skilltags.split(',')
            if tag not in ['', ' ']
        ]

    @skilltags.setter
    def skilltags(self, tagid_list: List[int]):
        s = ','.join([str(t) for t in tagid_list])
        self.__skilltags = s

    @classmethod
    def get(cls, s: scoped_session, id: int) -> Optional[Any]:
        p = s.query(cls).get(id)
        if p is None:
            return None

        if p.is_active is False:
            return None

        return p
