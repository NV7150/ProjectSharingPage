from fastapi import FastAPI, HTTPException, status
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


# User

@app.post("/userapi/create", response_model=schema.User)
async def create_user(c_user: schema.UserCreate):
    return c_user.create()


@app.get("/userapi/user/{username:str}", response_model=schema.User)
async def get_user(username: str):
    with db.session_scope() as s:
        users_query = s.query(db.User).filter(
            db.User.username == username
        )
        users = list(users_query)
        if len(users) != 1:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")

        return schema.User.from_db(users[0])


# SkillTag

@app.post('/userapi/skilltag/create', response_model=schema.SkillTag)
async def create_skilltag(tag: schema.SkillTagCreate):
    result = tag.create()
    if result is None:
        HTTPException(status.HTTP_400_BAD_REQUEST)
    return result
