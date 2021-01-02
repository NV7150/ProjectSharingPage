from pydantic import BaseModel
import db
from typing import Any, Optional, List


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


class Project(BaseModel):
    id: int
    title: str
    subtitle: Optional[str]
    bg_image: Optional[str]
    description: str
    members: List[str]
    sns: Sns
    skilltags: List[int]

    @staticmethod
    def from_db(db_proj: db.Project):
        sns = Sns(
            twitter=db_proj.twitter,
            instagram=db_proj.instagram,
            github=db_proj.github,
            youtube=db_proj.youtube,
            vimeo=db_proj.vimeo,
            facebook=db_proj.facebook,
            tiktok=db_proj.tiktok,
            linkedin=db_proj.linkedin,
            wantedly=db_proj.wantedly,
            url=db_proj.url,
        )
        return Project(
            id=db_proj.id,
            title=db_proj.title,
            subtitle=db_proj.subtitle,
            bg_image=db_proj.bg_image,
            description=db_proj.description,
            skilltags=db_proj.skilltags,
            members=db_proj.members,
            sns=sns,
        )

    def update(self) -> Optional[Any]:
        with db.session_scope() as s:
            p = db.Project.get(s, self.id)
            if p is None:
                return None

            p.title = self.title
            p.subtitle = self.subtitle
            p.bg_image = self.bg_image
            p.description = self.description
            p.skilltags = self.skilltags
            p.members = self.members
            p.twitter = self.sns.twitter
            p.instagram = self.sns.instagram
            p.github = self.sns.github
            p.youtube = self.sns.youtube
            p.vimeo = self.sns.vimeo
            p.facebook = self.sns.facebook
            p.tiktok = self.sns.tiktok
            p.linkedin = self.sns.linkedin
            p.wantedly = self.sns.wantedly
            p.url = self.sns.url

            s.commit()
            return self.from_db(p)


class ProjectCreate(BaseModel):
    title: str
    subtitle: Optional[str]
    bg_image: Optional[str]
    description: str
    members: List[str]
    sns: Sns
    skilltags: List[int]

    def create(self) -> Project:
        p = db.Project()
        p.title = self.title
        p.subtitle = self.subtitle
        p.bg_image = self.bg_image
        p.description = self.description
        p.skilltags = self.skilltags
        p.members = self.members
        p.twitter = self.sns.twitter
        p.instagram = self.sns.instagram
        p.github = self.sns.github
        p.youtube = self.sns.youtube
        p.vimeo = self.sns.vimeo
        p.facebook = self.sns.facebook
        p.tiktok = self.sns.tiktok
        p.linkedin = self.sns.linkedin
        p.wantedly = self.sns.wantedly
        p.url = self.sns.url
        with db.session_scope() as s:
            s.add(p)
            s.commit()
            return Project.from_db(p)
