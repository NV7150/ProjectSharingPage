from fastapi import FastAPI

app = FastAPI(
    docs_url='/recommendapi/docs',
    openapi_url='/recommendapi/openapi.json',
)


@app.get('/recommendapi/')
async def index():
    return {'message': 'Hello, recommendapi!'}
