from fastapi import FastAPI
import db


app = FastAPI(
    docs_url="/userapi/docs",
    openapi_url="/userapi/openapi.json",
)


# Init db
db.Base.metadata.create_all(bind=db.engine)


@app.get("/userapi/")
async def index():
    return {"message": "Hello, userapi!"}
