from fastapi import FastAPI
import db
import schema


app = FastAPI(
    docs_url="/userapi/docs",
    openapi_url="/userapi/openapi.json",
)


# Init db
db.Base.metadata.create_all(bind=db.engine)


@app.get("/userapi/")
async def index():
    return {"message": "Hello, userapi!"}


@app.post("/userapi/create", response_model=schema.User)
async def create_user(c_user: schema.UserCreate):
    return c_user.create()
