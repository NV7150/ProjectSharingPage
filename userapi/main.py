from typing import Optional
from fastapi import FastAPI, HTTPException, status, Response
from fastapi import Cookie
import db
import schema


app = FastAPI(
    docs_url='/userapi/docs',
    openapi_url='/userapi/openapi.json',
)


# Init db
db.Base.metadata.create_all(bind=db.engine)


@app.get('/userapi/')
async def index():
    return {'message': 'Hello, userapi!'}


# User

@app.post(
    '/userapi/create',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'model': schema.User,
            'description': 'Successful response',
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Bad request'
        }
    }
)
async def create_user(c_user: schema.UserCreate):
    user: Optional[schema.User] = c_user.create()
    if user is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return user


@app.post(
    '/userapi/login',
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {
            'description': 'login accepted'
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'unauthorized'
        },
    },
)
async def login_user(login_request: schema.UserLogin):
    token: Optional[str] = login_request.login()
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    maxage = ''
    if login_request.remember_password:
        maxage = 'Max-Age=7776000;'

    cookie = f'token={token}; HttpOnly; '
    cookie += f'SameSite=Strict; Secure; {maxage} path=/;'
    headers = {'Set-Cookie': cookie}
    return Response(None, status.HTTP_202_ACCEPTED, headers=headers)


@app.post(
    '/userapi/logout',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_403_FORBIDDEN: {
            'description': 'Not logged in or used wrong token',
        }
    }
)
async def logout_user(token: Optional[str] = Cookie(None)):
    if token is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    t = schema.UserToken(raw_token=token)
    result = t.expire()

    if result is False:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    
    cookie = 'token=xxx; Max-Age=0; path=/'
    headers = {'Set-Cookie': cookie}
    return Response(None, status.HTTP_200_OK, headers)


@app.get(
    '/userapi/user/{username:str}',
    responses={
        status.HTTP_200_OK: {
            'model': schema.User,
            'descrption': 'Successful response'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'User not found'
        }
    }
)
async def get_user(username: str):
    with db.session_scope() as s:
        users_query = s.query(db.User).filter(
            db.User.username == username
        )
        users = list(users_query)
        if len(users) != 1:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 'User not found.')

        return schema.User.from_db(users[0])


# SkillTag

@app.post(
    '/userapi/skilltag/create',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'model': schema.SkillTag,
            'description': 'Successful response',
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Bad request',
        }
    }
)
async def create_skilltag(tag: schema.SkillTagCreate):
    result = tag.create()
    if result is None:
        HTTPException(status.HTTP_400_BAD_REQUEST)
    return result
