from fastapi import FastAPI, HTTPException, status, Cookie
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
import schema
import db
from utils import project, user
from typing import Optional

# Init db
db.Base.metadata.create_all(bind=db.engine)


app = FastAPI(
    docs_url='/chatapi/docs',
    openapi_url='/chatapi/openapi.json',
)


@app.get('/chatapi/')
async def index():
    return {'message': 'Hello, chatapi!'}


# Thread

@app.get(
    '/chatapi/thread/{id:int}',
    description='Get thread',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Successful Response',
            'model': schema.Thread,
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Thread not found',
        },
    },
)
async def get_thread(id: int):
    with db.session_scope() as s:
        t = s.query(db.Thread).get(id)
        if t is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return schema.Thread.from_db(t)


@app.post(
    '/chatapi/thread',
    description='Create thread',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Successful Response (created)',
            'model': schema.Thread,
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Authentication is required.',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Project not found (project_id is wrong)',
        },
    },
)
async def create_thread(
    t: schema.ThreadCreate,
    token: Optional[str] = Cookie(None),
):
    # auth
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if user.auth(token) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # project_id check
    if project.project_exist_check(t.project_id) is False:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return t.create()


# Message

@app.post(
    '/chatapi/message',
    description='Create Message',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Successful Response (created)',
            'model': schema.Message,
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Authorization is required',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Thread is not found (thread_id is wrong)',
        },
    }
)
async def create_message(
    msg: schema.MessageCreate,
    token: Optional[str] = Cookie(None),
):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    username = user.auth(token)
    if username is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        return msg.create(username)
    except schema.ForeignKeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
