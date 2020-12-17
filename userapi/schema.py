from pydantic import BaseModel
from typing import Optional, List
import db


class SkillTag(BaseModel):
    id: int
    name: str
    parents: List  # List[SkillTag]

    @staticmethod
    def from_db(db_skilltag: db.SkillTag):
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

        return SkillTag(
            id=db_skilltag.id,
            name=db_skilltag.name,
            parents=parents
        )


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

    skilltags: List[SkillTag]

    @staticmethod
    def from_db(db_user: db.User):
        skilltags_db = db_user.skilltags
        skilltags = [
            SkillTag.from_db(x)
            for x in skilltags_db
        ]
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
            skilltags=skilltags
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

    skilltags: List[int]

    def create(self) -> User:
        db_skilltags = []
        with db.session_scope() as s:
            for tagid in self.skilltags:
                tag = s.query(db.SkillTag).get(tagid)
                if tag is not None:
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
