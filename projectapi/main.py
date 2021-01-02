from typing import Optional
from fastapi import FastAPI, HTTPException, status, Cookie
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
        status.HTTP_400_BAD_REQUEST: {
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
    }
)
async def create_project(project: schema.ProjectCreate):
    return project.create()


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
    },
)
async def update_project(project: schema.Project):
    result = project.update()
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
    },
)
async def delete_project(id: int):
    with db.session_scope() as s:
        p: Optional[db.Project] = s.query(db.Project).get(id)
        if p is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        p.is_active = False
        s.commit()


# Like

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
        p: Optional[db.Project] = s.query(db.Project).get(id)
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
