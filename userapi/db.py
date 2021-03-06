from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
import bcrypt

import os
from contextlib import contextmanager
import uuid
from typing import Optional, Any


PG_USER = os.environ.get('POSTGRES_USER')
PG_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_URL = f'postgresql://{PG_USER}:{PG_PASSWORD}@userdb'
DB_ECHO = (os.environ.get('DB_ECHO') != 'False')

engine = create_engine(
    DB_URL,
    echo=DB_ECHO
)

Session = scoped_session(
    sessionmaker(
        autocommit=False, autoflush=True,
        bind=engine, expire_on_commit=False
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


class SkillTagUser(Base):
    """
    Association Object
    """
    __tablename__ = 'skill_user'
    user_id = Column(
        Integer, ForeignKey('user.id'),
        primary_key=True, nullable=False,
    )
    tag_id = Column(
        Integer, ForeignKey('skilltag.id'),
        primary_key=True, nullable=False,
    )


class User(Base):
    """[DB] User class

    Parameters
    ----------
    id: int (auto)
    username: str
        unique username
    email: str
        unique email
    hashed_password: str
        hashed with bcrypt
    display_name:
        non-unique
    icon: Optional[str]
        icon image url
    bio: Optional[str]
        description of user

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

    skilltags: List[SkillTag]

    is_admin: bool
    is_active: bool
        Set to False when the account has been logically deleted
    """
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True)
    username = Column('username', String, nullable=False, unique=True)
    email = Column('email', String, nullable=False, unique=True)
    hashed_password = Column('hashed_password', String, nullable=False)
    display_name = Column('display_name', String, nullable=False)
    icon = Column('icon', String, nullable=True)
    bio = Column('bio', String, nullable=True)

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

    # Skill
    skilltags = relationship(
        'SkillTag', secondary=SkillTagUser.__tablename__,
        back_populates='users',
    )

    # Flag
    is_admin = Column('is_admin', Boolean, nullable=False, default=False)
    is_active = Column('is_active', Boolean, nullable=False, default=True)

    tokens = relationship("Token", backref='user')

    @staticmethod
    def create(raw_password: str, **kwargs):
        """Create new user
        Parameters
        ----------
        raw_password: str
        **kwargs:
            User class args without is_admin, is_active

        Return
        ------
        new_user: User
            new_user.is_admin == False
            new_user.is_active == True
        """
        salt = bcrypt.gensalt(rounds=12, prefix=b'2b')
        hashed_password = bcrypt.hashpw(raw_password.encode(), salt)

        return User(
            hashed_password=hashed_password.decode(),
            is_admin=False,
            is_active=True,
            **kwargs,
        )

    def login(self, raw_password: str) -> bool:
        """Login user
        Parameters
        ----------
        raw_password: str

        Return
        ------
        success: bool
        """
        if self.is_active is False:
            return False

        hashed_password = str(self.hashed_password)
        return bcrypt.checkpw(
            raw_password.encode(),
            hashed_password.encode(),
        )

    def set_password(self, new_password: str) -> bool:
        """Set new password
        WARNING: THIS METHOD DOESN'T CHECK OLD PASSWORD
        WARNING: This method doen't commit changes

        Parameters
        ----------
        new_password: str

        Returns
        -------
        result: bool
            if True, user is not active
        """
        if self.is_active is False:
            return False

        salt = bcrypt.gensalt(rounds=12, prefix=b'2b')
        hashed_password = bcrypt.hashpw(new_password.encode(), salt)

        self.hashed_password = hashed_password.decode()
        return True

    def delete(self) -> None:
        """Set False to is_active
        WARNING: This method doesn't commit changes
        """
        self.is_active = False


class Token(Base):
    """[DB]User Token
    Parameters
    ----------
    hashed_token: str
        hashed with bcrypt
    user_id: int
        user id
    is_active: bool
        Set to False when key has been expired.
    """
    __tablename__ = "token"
    hashed_token = Column('token', String, primary_key=True)
    user_id = Column("user_id", ForeignKey('user.id'))
    is_active = Column('is_active', Boolean, default=True)

    @staticmethod
    def issue_token(user: User) -> Optional[str]:
        token_salt = bcrypt.gensalt(rounds=4, prefix=b'2b')
        raw_token = str(uuid.uuid4()) + f'@{user.id}'
        hashed_token = bcrypt.hashpw(raw_token.encode(), token_salt)

        with session_scope() as s:
            token = Token(
                hashed_token=hashed_token.decode(),
                user_id=user.id,
            )
            s.add(token)
            s.commit()
        # TODO: Expire token
        return raw_token

    def _check_token(self, raw_token: str) -> bool:
        hashed: str = self.hashed_token
        return bcrypt.checkpw(
            raw_token.encode(), hashed.encode()
        )

    @staticmethod
    def get_userid(raw_token: str) -> Optional[int]:
        """Get userif from token
        WARNING: This method not check the validity of the token
        """
        id: Optional[int] = None
        try:
            id = int(raw_token.split('@')[-1])
        except (ValueError, IndexError):
            return None

        return id

    @staticmethod
    def get_token(raw_token) -> Optional[Any]:
        userid = Token.get_userid(raw_token)
        with session_scope() as s:
            user = s.query(User).get(userid)
            if user is None:
                return None
            for token in user.tokens:
                if token.is_active is False:
                    continue
                if token._check_token(raw_token):
                    return token
        return None

    def expire(self) -> None:
        with session_scope() as s:
            self.is_active = False
            s.commit()


class SkillTag(Base):
    """[DB] User skill tag
    Parameters
    ----------
    id: int (auto)
        primary key
    name: str
        unique skill name
    parent_id: Option[int]
        parent skilltag id
    users: List[User]
        tagged user
    """
    __tablename__ = "skilltag"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False, unique=True)
    parent_id = Column('parent_id', ForeignKey('skilltag.id'), nullable=True)

    users = relationship(
        'User', secondary=SkillTagUser.__tablename__,
        back_populates='skilltags',
    )
