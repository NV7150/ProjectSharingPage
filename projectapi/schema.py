from pydantic import BaseModel
import db
from utils.func import levenshtein_distance
from sqlalchemy import func
from typing import Optional, List
import enum


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
    announce_users: List[str]
    admin_users: List[str]
    likes: int
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
            members=[pu.username for pu in db_proj.members],
            announce_users=[au.username for au in db_proj.announce_users],
            admin_users=[au.username for au in db_proj.admin_users],
            likes=len(db_proj.likes),
            sns=sns,
            skilltags=db_proj.skilltags,
        )


class ProjectUpdate(BaseModel):
    id: int
    title: str
    subtitle: Optional[str]
    bg_image: Optional[str]
    description: str
    sns: Sns
    skilltags: List[int]

    def update(self) -> Optional[Project]:
        with db.session_scope() as s:
            p = db.Project.get(s, self.id)
            if p is None:
                return None

            p.title = self.title
            p.subtitle = self.subtitle
            p.bg_image = self.bg_image
            p.description = self.description
            p.skilltags = self.skilltags
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
            return Project.from_db(p)


class ProjectCreate(BaseModel):
    title: str
    subtitle: Optional[str]
    bg_image: Optional[str]
    description: str
    sns: Sns
    skilltags: List[int]

    def create(self, username: str) -> Project:
        with db.session_scope() as s:
            p = db.Project()
            p.title = self.title
            p.subtitle = self.subtitle
            p.bg_image = self.bg_image
            p.description = self.description
            p.skilltags = self.skilltags
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

            s.add(p)
            s.commit()

            pu = db.ProjectUser(
                project_id=p.id,
                username=username,
            )
            au = db.ProjectAnnounceUser(
                project_id=p.id,
                username=username,
            )
            adu = db.ProjectAdminUser(
                project_id=p.id,
                username=username,
            )
            s.add(pu)
            s.add(au)
            s.add(adu)
            s.commit()

            return Project.from_db(p)


class MemberType(str, enum.Enum):
    MEMBER = 'MEMBERTYPE_MEMBER'
    ANNOUNCE = 'MEMBERTYPE_ANNOUNCE'
    ADMIN = 'MEMBERTYPE_ADMIN'


class ProjectJoin(BaseModel):
    username: str
    type: MemberType


class Likes(BaseModel):
    users: List[str]

    @classmethod
    def get_from_project(cls, p: db.Project):
        return cls(
            users=[like.username for like in p.likes]
        )


class ProjectSearchResult(BaseModel):
    """Project search result

    Parameters
    ----------
    projects: List[Project]
        List of search result
    limit, offset: Optional[int]
        index slice
    next_exist: bool
        Search results still exist after index slice
    """
    projects: List[Project]
    limit: Optional[int]
    offset: Optional[int]
    next_exist: bool

    @classmethod
    def search(
        cls,
        title: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        with db.session_scope() as s:
            q = s.query(db.Project).filter(
                func.upper(db.Project.title).like(
                    f"%{title.upper()}%"
                )
            )
            length = q.count()
            db_projects = q.all()
            db_projects.sort(
                key=lambda x: levenshtein_distance(x.title, title)
            )
            if offset is not None:
                db_projects = db_projects[offset:]
            if limit is not None:
                db_projects = db_projects[:limit]

            projects = [
                Project.from_db(p)
                for p in db_projects
            ]
            next_exist = len(projects) + (offset if offset else 0) < length

            return cls(
                projects=projects,
                limit=limit,
                offset=offset,
                next_exist=next_exist,
            )
