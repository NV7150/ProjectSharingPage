from fastapi import FastAPI


app = FastAPI(
    docs_url='/chatapi/docs',
    openapi_url='/chatapi/openapi.json',
)


@app.get('/chatapi/')
async def index():
    return {'message': 'Hello, chatapi!'}
