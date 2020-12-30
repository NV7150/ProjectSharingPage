from fastapi import FastAPI, HTTPException, status
import schema
import db

# Init db
db.Base.metadata.create_all(bind=db.engine)


app = FastAPI(
    docs_url='/chatapi/docs',
    openapi_url='/chatapi/openapi.json',
)


@app.get('/chatapi/')
async def index():
    return {'message': 'Hello, chatapi!'}


@app.post(
    '/chatapi/thread',
    description='Create thread',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'message': 'Successful Response (created)',
            'model': schema.Thread,
        },
    },
)
async def create_thread(t: schema.ThreadCreate):
    return t.create()
