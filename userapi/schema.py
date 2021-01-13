import enum
from pydantic import BaseModel
from typing import Optional, List, Any
import db


class SkillTag(BaseModel):
    id: int
    name: str
    parents: List  # List[SkillTag]

    @classmethod
    def from_db(cls, db_skilltag: db.SkillTag):
        # Tracing back the family tree
        print('DB_SKILLTAG', db_skilltag)
        db_parents: List[db.SkillTag] = []
        ds = db_skilltag
        while True:
            with db.session_scope() as s:
                parent_id = ds.parent_id
                parent = s.query(db.SkillTag).get(parent_id)

            if parent is None:
                break
            db_parents.append(parent)
            ds = parent

        parents = [
            SkillTag(id=dp.id, name=dp.name, parents=[])
            for dp in db_parents
        ]
        parents.reverse()

        return cls(
            id=db_skilltag.id,
            name=db_skilltag.name,
            parents=parents
        )

    @staticmethod
    def get(id: int) -> Optional[Any]:  # Optional[SkillTag]
        with db.session_scope() as s:
            t = s.query(db.SkillTag).get(id)
            if t is None:
                return None

            return SkillTag.from_db(t)


class SkillTagCreate(BaseModel):
    name: str
    parent_id: Optional[int]

    def create(self) -> Optional[SkillTag]:
        with db.session_scope() as s:
            parent = None
            if self.parent_id is not None:
                parent = s.query(db.SkillTag).get(self.parent_id).id

            skilltag = db.SkillTag(
                name=self.name,
                parent_id=parent,
            )
            s.add(skilltag)
            s.commit()
            return SkillTag.from_db(skilltag)


class Sns(BaseModel):
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


class User(BaseModel):
    username: str
    display_name: str
    icon: Optional[str]
    bio: Optional[str]

    sns: Sns

    skilltags: List[SkillTag]

    @staticmethod
    def from_db(db_user: db.User):
        skilltags_db = db_user.skilltags
        skilltags = [
            SkillTag.from_db(x)
            for x in skilltags_db
        ]
        sns = Sns(
            twitter=db_user.twitter,
            instagram=db_user.instagram,
            github=db_user.github,
            youtube=db_user.youtube,
            vimeo=db_user.vimeo,
            facebook=db_user.facebook,
            tiktok=db_user.tiktok,
            linkedin=db_user.linkedin,
            wantedly=db_user.wantedly,
            url=db_user.url,
        )
        return User(
            username=db_user.username,
            display_name=db_user.display_name,
            icon=db_user.icon,
            bio=db_user.bio,
            sns=sns,
            skilltags=skilltags
        )


class LoginUser(User):
    email: str

    @staticmethod
    def from_db(db_user: db.User):
        skilltags_db = db_user.skilltags
        skilltags = [
            SkillTag.from_db(x)
            for x in skilltags_db
        ]
        sns = Sns(
            twitter=db_user.twitter,
            instagram=db_user.instagram,
            github=db_user.github,
            youtube=db_user.youtube,
            vimeo=db_user.vimeo,
            facebook=db_user.facebook,
            tiktok=db_user.tiktok,
            linkedin=db_user.linkedin,
            wantedly=db_user.wantedly,
            url=db_user.url,
        )
        return LoginUser(
            username=db_user.username,
            email=db_user.email,
            display_name=db_user.display_name,
            icon=db_user.icon,
            bio=db_user.bio,
            sns=sns,
            skilltags=skilltags
        )

    @classmethod
    def from_token(cls, token: str) -> Optional[Any]:
        with db.session_scope() as s:
            # check token
            t: Optional[db.Token] = db.Token.get_token(token)
            if t is None:
                return None

            user: Optional[db.User] = s.query(db.User).get(t.user_id)
            if user is None:
                return None

            return cls.from_db(user)


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

    skilltags: List[int]

    def create(self) -> Optional[User]:
        db_skilltags = []
        with db.session_scope() as s:
            for tagid in self.skilltags:
                tag = s.query(db.SkillTag).get(tagid)
                if tag is None:
                    return None
                db_skilltags.append(tag)

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
            url=self.url,
            skilltags=db_skilltags,
        )
        with db.session_scope() as s:
            s.add(user)
            s.commit()
            return User.from_db(user)


class UserToken(BaseModel):
    raw_token: str

    def auth(self) -> bool:
        t = db.Token.get_token(self.raw_token)
        if t is None:
            return False
        return True

    def expire(self) -> bool:
        token: Optional[db.Token] = db.Token.get_token(self.raw_token)
        if token is None:
            return False
        token.expire()
        return True


class UserLogin(BaseModel):
    username: str
    raw_password: str
    remember_password: bool

    def login(self) -> Optional[str]:
        with db.session_scope() as s:
            users: List[db.User] = list(
                s.query(db.User).filter(
                    db.User.username == self.username
                )
            )
            if len(users) != 1:
                return None

            user: db.User = users[0]
            if user.login(self.raw_password) is False:
                return None

            token = db.Token.issue_token(user)
            return token


class UserDelete(BaseModel):
    username: str
    raw_password: str

    def delete(self, token: str) -> bool:
        userid = db.Token.get_userid(token)
        with db.session_scope() as s:
            user = s.query(db.User).get(userid)
            if user.username != self.username:
                return False
            if user.login(self.raw_password) is False:
                return False

            user.delete()
            s.commit()

        return True


class PasswordUpdateResult(enum.Enum):
    TOKEN_WRONG = enum.auto()
    OLD_PASSWORD_WRONG = enum.auto()
    USER_NOT_FOUND = enum.auto()
    SUCCESS = enum.auto()


class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str

    def update(self, token: str) -> PasswordUpdateResult:
        t = db.Token.get_token(token)
        if t is None:
            return PasswordUpdateResult.TOKEN_WRONG

        with db.session_scope() as s:
            userid = db.Token.get_userid(token)
            user = s.query(db.User).get(userid)

            if user.is_active is False:
                return PasswordUpdateResult.USER_NOT_FOUND

            if user.login(self.old_password) is False:
                return PasswordUpdateResult.OLD_PASSWORD_WRONG
            result = user.set_password(self.new_password)
            if result is False:
                return PasswordUpdateResult.USER_NOT_FOUND
            s.commit()

        return PasswordUpdateResult.SUCCESS
