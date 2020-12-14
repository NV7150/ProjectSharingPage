from pydantic import BaseModel
from typing import Optional
import bcrypt
from pydantic.typing import display_as_type
import db


class User(BaseModel):
    username: str
    display_name: str
    icon: Optional[str]
    bio: Optional[str]

    # SNS
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

    @staticmethod
    def from_db(db_user: db.User):
        return User(
            username=db_user.username,
            display_name=db_user.display_name,
            icon=db_user.icon,
            bio=db_user.bio,
            twitter=db_user.twitter,
            instagram=db_user.instagram,
            github=db_user.github,
            youtube=db_user.youtube,
            vimeo=db_user.vimeo,
            facebook=db_user.facebook,
            tiktok=db_user.tiktok,
            linkedin=db_user.linkedin,
            wantedly=db_user.wantedly,
            url=db_user.linkedin,
        )


class UserCreate(BaseModel):
    username: str
    email: str
    raw_password: str
    display_name: str
    icon: Optional[str]
    bio: Optional[str]

    # SNS
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

    def create(self) -> User:
        user = db.User.create(
            raw_password=self.raw_password,
            username=self.username,
            email=self.email,
            display_name=self.display_name,
            icon=self.icon,
            bio=self.bio,
            twitter=self.twitter,
            instagram=self.instagram,
            github=self.github,
            youtube=self.youtube,
            vimeo=self.vimeo,
            facebook=self.facebook,
            tiktok=self.tiktok,
            linkedin=self.linkedin,
            wantedly=self.wantedly,
            url=self.url
        )
        with db.session_scope() as s:
            s.add(user)
            s.commit()
            return User.from_db(user)
