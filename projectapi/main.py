from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Cookie
from fastapi.param_functions import Query
from pydantic.types import Json
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
import uuid
import os

import db
import schema
from utils import user
import random


# Init db
db.Base.metadata.create_all(bind=db.engine)


app = FastAPI(
    docs_url='/projectapi/docs',
    openapi_url='/projectapi/openapi.json',
)


@app.get('/projectapi/')
async def index():
    return {'message': 'Hello, projectapi!'}


# CRUD Project

@app.get(
    '/projectapi/project/{id:int}',
    description='Get project',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': schema.Project,
            'description': 'Successful Response',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project not found',
        },
    },
)
async def get_project(id: int):
    with db.session_scope() as s:
        p: Optional[db.Project] = db.Project.get(s, id)
        if p is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        return schema.Project.from_db(p)


@app.post(
    '/projectapi/project',
    description='Create project',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'model': schema.Project,
            'description': 'Successful response (created)',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Login failed (token is wrong)',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'SkillTag not found.'
        }
    }
)
async def create_project(
    project: schema.ProjectCreate,
    token: Optional[str] = Cookie(None),
):
    # auth
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    username = user.auth(token)
    if username is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # tag check
    if False in [user.tag_exist(t) for t in project.skilltags]:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'SkillTag not found',
        )

    return project.create(username)


@app.patch(
    '/projectapi/project/{id:int}',
    description=f"""Update project\n
    changable_fields = {schema.ProjectUpdate.changable_fields}\n
    changable_sns_fields = {schema.ProjectUpdate.changable_sns_fields}\n
    """,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': schema.Project,
            'description': 'Successful response (updated)',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Resource not found.'
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'not logged in',
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            'description': 'Value error'
        }
    },
)
async def update_project(
    id: int,
    update_fields: Json,
    token: Optional[str] = Cookie(None),
):
    # Permission (admin only)
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if (username := user.auth(token)) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    with db.session_scope() as s:
        p = db.Project.get(s, id)
        if p is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                'Project is not found (id is wrong)',
            )
        if username not in [au.username for au in p.admin_users]:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

    # Update
    try:
        project_update = schema.ProjectUpdate(id, update_fields)
        result = project_update.update()
    except ValueError as e:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            str(e),
        )

    return result


@app.delete(
    '/projectapi/project/{id:int}',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Successful response (deleted)',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project not found',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'login failed'
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'forbidden (admin only)'
        },
    },
)
async def delete_project(id: int, token: Optional[str] = Cookie(None)):
    with db.session_scope() as s:
        p = db.Project.get(s, id)
        if p is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        # permission
        if token is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        if (username := user.auth(token)) is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        if username not in [au.username for au in p.admin_users]:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        p.is_active = False
        s.commit()


@app.get(
    '/projectapi/project',
    status_code=status.HTTP_200_OK,
    description='get projects with tag (OR)',
    responses={
        status.HTTP_200_OK: {
            'model': List[schema.Project],
            'description': 'Successful Response',
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Missing query'
        }
    },
)
async def get_project_with_tag(tags: List[int] = Query([]),
                               limit: Optional[int] = Query(None),
                               offset: Optional[int] = Query(None),
                               sortbydatetime: bool = Query(False),
                               reverse: bool = Query(False)):
    with db.session_scope() as s:
        projects = schema.ProjectSearchResult.get_with_tag(
            s, tags, limit, offset, sortbydatetime, reverse
        )
        return [schema.Project.from_db(p) for p in projects]


@app.get(
    '/projectapi/project/random',
    status_code=status.HTTP_200_OK,
    description='Get random project id',
    responses={
        status.HTTP_200_OK: {
            'model': int,
            'description': 'Successful response (only project-id)',
        },
    },
)
async def get_random_project_id():
    with db.session_scope() as s:
        all_id = list(s.query(db.Project.id).all())
        index = random.randint(0, len(all_id)-1)
        id = all_id[index]
        return id


# Project Background Image

@app.get(
    '/projectapi/projectimage/{filename:str}',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Successful response.',
            'content': {'image/*': {}},
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Not found',
        },
    },
)
async def get_projectimage(filename: str):
    fullpath = f'/projectimage/{filename}'
    if not os.path.exists(fullpath):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return FileResponse(fullpath)


@app.post(
    '/projectapi/projectimage/{id:int}',
    status_code=status.HTTP_201_CREATED,
    description='Upload project image',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Uploaded',
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Wrong filetype',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Token required',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'Admin required',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project not found.'
        },
    },
)
async def upload_image(
    id: int,
    file: UploadFile = File(...),
    token: Optional[str] = Cookie(None),
):
    # auth
    if None in [token, username := user.auth(token)]:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # check userlevel
    with db.session_scope() as s:
        p: Optional[db.Project] = s.query(db.Project).get(id)
        if p is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        # check userlevel
        if username not in [adu.username for adu in p.admin_users]:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        content_type = file.content_type
        if content_type not in ['image/png', 'image/jpeg']:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'file should be image/png or image/jpeg',
            )

        data = file.file.read()
        file.file.close()
        ext = file.filename.split('.')[-1]
        filename = str(uuid.uuid4())
        while os.path.exists(f'/projectimage/{filename}.{ext}'):
            filename = str(uuid.uuid4())
        full_filename = f'/projectimage/{filename}.{ext}'

        with open(full_filename, 'wb') as f:
            f.write(data)

        # delete previous image
        if p.bg_image is not None and os.path.exists(p.bg_image):
            os.remove(p.bg_image)

        p.bg_image = f'/projectapi/projectimage/{filename}.{ext}'
        s.commit()

        return p.bg_image


# Like

@app.get(
    '/projectapi/project/{id:int}/like',
    description='Get users who likes project',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': schema.Likes,
            'description': 'Successful response (liked)',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project not found',
        },
    },
)
def get_likes(id: int):
    with db.session_scope() as s:
        p = db.Project.get(s, id)
        if p is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        return schema.Likes.get_from_project(p)


@app.patch(
    '/projectapi/project/{id:int}/like',
    description='like to project',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Successful response (liked)',
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            'description': 'Already liked',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Cookie token is required.',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project not found.',
        },
    }
)
async def like(id: int, token: Optional[str] = Cookie(None)):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    username: Optional[str] = user.auth(token)
    if username is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    with db.session_scope() as s:
        p = db.Project.get(s, id)
        if p is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        user_proj_likes = s.query(db.Like).filter(
            db.Like.username == username
        ).filter(
            db.Like.project_id == id
        )
        if user_proj_likes.count() > 0:
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS)

        like = db.Like(username=username, project_id=p.id)
        s.add(like)
        s.commit()

        return


@app.delete(
    '/projectapi/project/{id:int}/like',
    description='unlike to project',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Successful response (unliked)',
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            'description': 'Already unliked/not liked yet',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Cookie token is required.',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project not found.',
        },
    }
)
def unlike(id: int, token: Optional[str] = Cookie(None)):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    username: Optional[str] = user.auth(token)
    if username is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    with db.session_scope() as s:
        likes = s.query(db.Like).filter(
            db.Like.username == username
        ).filter(
            db.Like.project_id == id
        )

        if likes.count() < 1:
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS)

        likes.delete()
        s.commit()

    return


# Member
@app.post(
    '/projectapi/project/{proj_id:int}/members',
    description='Set user as member_type',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': List[str],
            'description': 'Successful response (list of username)'
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'not logged in',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'permitted (only for admin user)',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project/User not found',
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            'description': 'already joined',
        },
    },
)
async def join_member(
    proj_id: int, project_join: schema.ProjectJoin,
    token: Optional[str] = Cookie(None),
):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if (username := user.auth(token)) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if user.exist(project_join.username) is False:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'User not found',
        )

    with db.session_scope() as s:
        if (p := db.Project.get(s, proj_id)) is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                'Project not found',
            )

        # permission (admin only)
        if username not in [au.username for au in p.admin_users]:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        # already joined?
        if project_join.type == schema.MemberType.MEMBER:
            if project_join.username in [x.username for x in p.members]:
                raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS)
        if project_join.type == schema.MemberType.ANNOUNCE:
            if project_join.username in [x.username for x in p.announce_users]:
                raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS)
        if project_join.type == schema.MemberType.ADMIN:
            if project_join.username in [x.username for x in p.admin_users]:
                raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS)

        # join
        all_type = [
            schema.MemberType.MEMBER,
            schema.MemberType.ANNOUNCE,
            schema.MemberType.ADMIN
        ]
        if project_join.type in all_type:
            # member, announce, admin
            mem_list = [x.username for x in p.members]
            if project_join.username not in mem_list:
                pu = db.ProjectUser(
                    project_id=proj_id,
                    username=project_join.username
                )
                s.add(pu)

                # delete from waitlist
                wl = s.query(db.JoinRequestUser).filter(
                    db.JoinRequestUser.project_id == proj_id
                ).filter(
                    db.JoinRequestUser.username == project_join.username
                )
                [s.delete(x) for x in wl]

        if project_join.type in all_type[1:]:
            # announce, admin
            au_list = [x.username for x in p.announce_users]
            if project_join.username not in au_list:
                au = db.ProjectAnnounceUser(
                    project_id=proj_id,
                    username=project_join.username,
                )
                s.add(au)

        if project_join.type in all_type[2:]:
            # admin
            adu_list = [x.username for x in p.admin_users]
            if project_join.username not in adu_list:
                adu = db.ProjectAdminUser(
                    project_id=proj_id,
                    username=project_join.username,
                )
                s.add(adu)

        s.commit()


# Member
@app.delete(
    '/projectapi/project/{proj_id:int}/members',
    description='Strip member_type from user',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Successful response (Stripped)'
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'not logged in',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'permitted (only for admin user)',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project/User not found',
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'User does\'nt have member_type',
        },
    },
)
async def strip_membertype(proj_id: int, project_strip: schema.ProjectJoin,
                           token: Optional[str] = Cookie(None)):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if (username := user.auth(token)) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if user.exist(project_strip.username) is False:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'User not found',
        )

    with db.session_scope() as s:
        if (p := db.Project.get(s, proj_id)) is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                'Project not found',
            )

        # permission (admin only)
        if username not in [au.username for au in p.admin_users]:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        # check
        if project_strip.type == schema.MemberType.MEMBER:
            if project_strip.username not in [x.username
                                              for x in p.members]:
                raise HTTPException(status.HTTP_400_BAD_REQUEST)
        if project_strip.type == schema.MemberType.ANNOUNCE:
            if project_strip.username not in [x.username
                                              for x in p.announce_users]:
                raise HTTPException(status.HTTP_400_BAD_REQUEST)
        if project_strip.type == schema.MemberType.ADMIN:
            if project_strip.username not in [x.username
                                              for x in p.admin_users]:
                raise HTTPException(status.HTTP_400_BAD_REQUEST)

        # join
        if project_strip.type == schema.MemberType.ADMIN:
            # adminだけ消す
            au = s.query(db.ProjectAdminUser).filter(
                db.ProjectAdminUser.project_id == proj_id
            ).filter(
                db.ProjectAdminUser.username == project_strip.username
            )
            [s.delete(x) for x in au]

        elif project_strip.type == schema.MemberType.ANNOUNCE:
            # adminとannounceだけ消す
            adu = s.query(db.ProjectAdminUser).filter(
                db.ProjectAdminUser.project_id == proj_id
            ).filter(
                db.ProjectAdminUser.username == project_strip.username
            )
            [s.delete(x) for x in adu]

            au = s.query(db.ProjectAnnounceUser).filter(
                db.ProjectAnnounceUser.project_id == proj_id
            ).filter(
                db.ProjectAnnounceUser.username == project_strip.username
            )
            [s.delete(x) for x in au]

        elif project_strip.type == schema.MemberType.MEMBER:
            # admin, announce, member全消し
            adu = s.query(db.ProjectAdminUser).filter(
                db.ProjectAdminUser.project_id == proj_id
            ).filter(
                db.ProjectAdminUser.username == project_strip.username
            )
            [s.delete(x) for x in adu]

            au = s.query(db.ProjectAnnounceUser).filter(
                db.ProjectAnnounceUser.project_id == proj_id
            ).filter(
                db.ProjectAnnounceUser.username == project_strip.username
            )
            [s.delete(x) for x in au]

            u = s.query(db.ProjectUser).filter(
                db.ProjectUser.project_id == proj_id
            ).filter(
                db.ProjectUser.username == project_strip.username
            )
            [s.delete(x) for x in u]

        s.commit()


@app.post(
    '/projectapi/project/{proj_id:int}/join-request',
    description='Join request',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Added to waitlist',
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            'description': 'Already joined',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project/User not found',
        },
    },
)
async def join_request(proj_id: int, token: Optional[str] = Cookie(None)):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if (username := user.auth(token)) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    with db.session_scope() as s:
        p: Optional[db.Project] = s.query(db.Project).get(proj_id)
        if p is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        if len([m for m in p.members if m.username == username]) > 0:
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS,
                                "Already joined to project")

        if len([ju for ju in p.waitlist if ju.username == username]) > 0:
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS,
                                "Already added to waitlist")

        u = db.JoinRequestUser(
            project_id=proj_id,
            username=username,
        )
        s.add(u)
        s.commit()

    return "Added to waitlist"


@app.get(
    '/projectapi/project/waitlist',
    description='Waitlist per user',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Successful Response (List of waiting project id)',
            'model': List[schema.Project],
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Invalid user token.'
        },
    },
)
async def user_waitlist(token: Optional[str] = Cookie(None)):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if (username := user.auth(token)) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    with db.session_scope() as s:
        waiting_projects = s.query(db.JoinRequestUser).filter(
            db.JoinRequestUser.username == username
        )

        result: List[schema.Project] = []
        for wp in waiting_projects:
            p = db.Project.get(s, wp.project_id)
            if p is None:
                continue

            result.append(schema.Project.from_db(p))

        return result


@app.get(
    '/projectapi/project/{proj_id:int}/waitlist',
    description='Waitlist per project',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Successful Response (List of waiting username)',
            'model': List[str],
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Invalid user token.'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project/User not found',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'Permission denied (Admin only)'
        }
    },
)
async def waitlist(proj_id: int, token: Optional[str] = Cookie(None)):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if (username := user.auth(token)) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    with db.session_scope() as s:
        if (p := db.Project.get(s, proj_id)) is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                'Project not found',
            )

        # permission (admin only)
        if username not in [au.username for au in p.admin_users]:
            raise HTTPException(status.HTTP_403_FORBIDDEN,
                                'Admin only')

        return [ju.username for ju in p.waitlist]


@app.delete(
    '/projectapi/project/{proj_id:int}/join-request',
    description='Delete join request (by admin or requested user)',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Successful response (deleted)',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project/User not found.',
        },
    },
)
async def delete_join_request(
    proj_id: int,
    username: Optional[str] = Query(None),
    token: Optional[str] = Cookie(None),
):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if (req_username := user.auth(token)) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    with db.session_scope() as s:
        p: Optional[db.Project] = s.query(db.Project).get(proj_id)
        if p is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        if username is not None:  # by Admin
            if user.exist(username) is False:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    'User not found',
                )

            # permission
            if req_username not in [au.username for au in p.admin_users]:
                raise HTTPException(status.HTTP_403_FORBIDDEN,
                                    'Admin only')

            for wu in p.waitlist:
                if wu.username == username:
                    s.delete(wu)
                    s.commit()
                    return "deleted"

            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                'username not in waitlist')

        else:
            # by User
            if user.exist(req_username) is False:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    'User not found.'
                )

            wl = [wu for wu in p.waitlist if wu.username == req_username]
            if len(wl) == 0:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    'User not in waitlist',
                )

            for w in wl:
                s.delete(w)
        s.commit()
        return "deleted"


# Search
@app.get(
    '/projectapi/project/search',
    description='Search Project',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': schema.ProjectSearchResult,
            'description':
                'Successful Response (sorted by levenshtein distance)',
        },
    },
)
async def search_project(
    title: str,
    limit: int,
    offset: int,
):
    return schema.ProjectSearchResult.search(title, limit, offset)


# User
@app.get(
    '/projectapi/project/{username:str}',
    description='Projects in which the user joins',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': List[schema.Project],
            'description': 'Successful response',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'User not found',
        },
    },
)
async def projects_of_user(username: str):
    with db.session_scope() as s:
        proj_list = s.query(db.ProjectUser).filter(
            db.ProjectUser.username == username
        )
        return [
            schema.Project.from_db(pu.project)
            for pu in proj_list
            if pu.project.is_active
        ]
