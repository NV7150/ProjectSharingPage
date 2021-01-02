from fastapi import FastAPI, HTTPException, status
import schema
import db
from utils import project

# Init db
db.Base.metadata.create_all(bind=db.engine)


app = FastAPI(
    docs_url='/chatapi/docs',
    openapi_url='/chatapi/openapi.json',
)


@app.get('/chatapi/')
async def index():
    return {'message': 'Hello, chatapi!'}


@app.get(
    '/chatapi/thread/{id:int}',
    description='Get thread',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'message': 'Successful Response',
            'model': schema.Thread,
        },
        status.HTTP_404_NOT_FOUND: {
            'message': 'Thread not found',
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
            'message': 'Successful Response (created)',
            'model': schema.Thread,
        },
        status.HTTP_404_NOT_FOUND: {
            'message': 'Project not found (project_id is wrong)',
        },
    },
)
async def create_thread(t: schema.ThreadCreate):
    if project.project_exist_check(t.project_id) is False:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return t.create()
