from typing import Optional
from fastapi import FastAPI, HTTPException, status, Response
from fastapi import Cookie
import db
import schema


# Init db
db.Base.metadata.create_all(bind=db.engine)


app = FastAPI(
    docs_url='/projectapi/docs',
    openapi_url='/projectapi/openapi.json',
)

@app.get('/projectapi/')
async def index():
    return {'message': 'Hello, projectapi!'}


@app.post(
    '/projectapi/project',
    description='Create project',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': schema.Project,
            'description': 'Successful response (created)',
        },
    }
)
async def create_project(project: schema.ProjectCreate):
    return project.create()
