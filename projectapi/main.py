from fastapi import FastAPI, HTTPException, status
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
