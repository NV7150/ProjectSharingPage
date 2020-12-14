from fastapi import FastAPI, HTTPException

app = FastAPI(
    docs_url="/userapi/docs",
    openapi_url="/userapi/openapi.json",
)

@app.get("/userapi/")
async def index():
    return {"message": "Hello, userapi!"}
