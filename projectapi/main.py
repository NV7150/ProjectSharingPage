from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Cookie
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
import db
import schema
from utils import auth


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
    }
)
async def create_project(
    project: schema.ProjectCreate,
    token: Optional[str] = Cookie(None),
):
    # auth
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    username = auth.auth(token)
    if username is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return project.create(username)


@app.patch(
    '/projectapi/project',
    description='Update project',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': schema.Project,
            'description': 'Successful response (updated)',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project is not found (id is wrong)'
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'not logged in',
        },
    },
)
async def update_project(
    project_update: schema.ProjectUpdate,
    token: Optional[str] = Cookie(None),
):
    # Permission (admin only)
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if (username := auth.auth(token)) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    with db.session_scope() as s:
        p = db.Project.get(s, project_update.id)
        if p is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        if username not in [au.username for au in p.admin_users]:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

    # Update
    result = project_update.update()
    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

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

        # p.
        # TODO: token auth, permission

        p.is_active = False
        s.commit()


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
    username: Optional[str] = auth.auth(token)
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
    username: Optional[str] = auth.auth(token)
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
