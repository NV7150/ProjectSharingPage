from typing import Optional
from fastapi import FastAPI, HTTPException, status, Response
from fastapi import Cookie


app = FastAPI(
    docs_url='/projectapi/docs',
    openapi_url='/projectapi/openapi.json',
)

@app.get('/projectapi/')
async def index():
    return {'message': 'Hello, projectapi!'}
