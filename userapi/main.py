from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.responses import FileResponse
from fastapi import File, UploadFile
from fastapi import Cookie
import uuid
import os
import traceback

from pydantic.types import Json
from starlette.status import HTTP_404_NOT_FOUND

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

@app.get(
    '/userapi/user',
    description='Get login user',
    status_code=200,
    responses={
        status.HTTP_200_OK: {
            'model': schema.LoginUser,
            'description': 'Successful response',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Not logged in (cookie token is required)'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'User not found'
        }
    }
)
async def get_login_user(token: Optional[str] = Cookie(None)):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    u: Optional[schema.LoginUser] = schema.LoginUser.from_token(token)
    if u is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return u


@app.post(
    '/userapi/user',
    description='Create User',
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


@app.patch(
    '/userapi/user',
    summary='Update User',
    status_code=status.HTTP_200_OK,
    description=f"""Update user\n
    changable_fields = {schema.UserUpdate.changable_fields}\n
    changable_sns_fields = {schema.UserUpdate.changable_sns_fields}\n
    """,
    responses={
        status.HTTP_200_OK: {
            'model': schema.User,
            'description': 'Updated user info',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Token was broken.'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'User not found.'
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            'description': 'Wrong request (Unprocessable entity)',
        },
    },
)
async def update_user(json_data: Json, token: Optional[str] = Cookie(None)):
    # auth
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if db.Token.get_token(token) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    userid = db.Token.get_userid(token)
    if userid is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        userupdate = schema.UserUpdate(userid, json_data)
    except ValueError as e:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            traceback.format_exception_only(type(e), e)  # ValueError Message
        )

    result = userupdate.update()
    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return result


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


@app.patch(
    '/userapi/password',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_403_FORBIDDEN: {
            'description': 'Invalid token was given',
        },
        status.HTTP_400_BAD_REQUEST: {
            'descripiton': 'old/new password is incorrect',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'User not found.',
        },
    }
)
async def update_password(
    request: schema.UserPasswordUpdate,
    token: Optional[str] = Cookie(None),
):
    if token is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    if schema.UserToken(raw_token=token).auth() is False:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    result = request.update(token)
    if result == schema.PasswordUpdateResult.TOKEN_WRONG:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    if result == schema.PasswordUpdateResult.OLD_PASSWORD_WRONG:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Old password is wrong',
        )
    if result == schema.PasswordUpdateResult.USER_NOT_FOUND:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'User not found.'
        )
    if result == schema.PasswordUpdateResult.SUCCESS:
        return

    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.delete(
    '/userapi/user',
    description='Delete user',
    responses={
        status.HTTP_200_OK: {
            'description': 'Successful response (deleted)'
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'not logged in'
        },
    }
)
async def delete_user(
    user: schema.UserDelete, token: Optional[str] = Cookie(None)
):
    if token is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    result = user.delete(token)
    if result is False:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    cookie = 'token=xxx; Max-Age=0; path=/'
    headers = {'Set-Cookie': cookie}
    return Response(None, status.HTTP_200_OK, headers)


@app.get(
    '/userapi/user/search',
    responses={
        status.HTTP_200_OK: {
            'model': schema.UserSearchResult,
            'description': 'Successful Response',
        }
    }
)
async def search_user(keyword: str, limit: int, offset: int):
    return schema.UserSearchResult.search(keyword, limit, offset)


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

        user = users[0]
        if user.is_active is False:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 'User not found.')

        return schema.User.from_db(user)


# SkillTag

@app.post(
    '/userapi/skilltag',
    description='Create SkillTag',
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


@app.get(
    '/userapi/skilltag/{id:int}',
    description='Get skilltag',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': schema.SkillTag,
            'description': 'Successful response',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'skilltag not found.',
        },
    },
)
async def get_skilltag(id: int):
    t = schema.SkillTag.get(id)
    if t is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return t


@app.get(
    '/userapi/skilltag/{id:int}/children',
    description='Get child tags',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': List[schema.SkillTag],
            'description': 'Successful response.',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'parent tag not found'
        },
    },
)
async def get_children(id: int):
    children = schema.SkillTag.get_children(id)
    if children is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return children


@app.get(
    '/userapi/skilltag/list',
    description='Skilltag list',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': schema.SkillTagLookup
        }
    }
)
async def skilltag_list(
    limit: Optional[int] = None, offset: Optional[int] = None
):
    return schema.SkillTagLookup.get_list(limit, offset)


@app.get(
    '/userapi/skilltag/search',
    description='Search Skilltag',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Successful response',
            'model': List[schema.SkillTag],
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Not found',
        },
    },
)
async def search_skilltag(
    keyword: str,
    limit: Optional[int] = None, offset: Optional[int] = None,
):
    return schema.SkillTagLookup.search(
        keyword, limit, offset
    )


# User Icon

@app.get(
    '/userapi/usericon/{filename:str}',
    description='Get User-icon',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Image',
            'content': {'image/*': {}},
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Not found'
        }
    }
)
async def get_usericon(filename: str):
    full_filepath = f'/usericon/{filename}'
    if not os.path.exists(full_filepath):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return FileResponse(f'/usericon/{filename}')


@app.post(
    '/userapi/usericon',
    description='Upload User-icon',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'model': str,
            'description': 'Successful response (Icon URL)',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'token is required',
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Wrong Request'
        }
    },
)
async def upload_usericon(
    file: Optional[UploadFile] = File(None),
    token: Optional[str] = Cookie(None)
):
    # auth
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if schema.LoginUser.from_token(token) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if file is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    # mime check
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'File should be image/jpeg or image/png',
        )

    data: bytes = file.file.read()
    ext = file.filename.split('.')[-1]
    filename = str(uuid.uuid4())
    file.file.close()

    # while filename exists, re-generate filename
    while os.path.exists(f'/usericon/{filename}.{ext}'):
        filename = str(uuid.uuid4())

    # save icon
    full_filename = f'/usericon/{filename}.{ext}'
    with open(full_filename, 'wb') as f:
        f.write(data)

    # save icon url to database
    url = f'/userapi/usericon/{filename}.{ext}'
    user_id = db.Token.get_userid(token)
    old_icon: Optional[str] = None
    with db.session_scope() as s:
        u: Optional[db.User] = s.query(db.User).get(user_id)
        if u is None:
            # user is missing
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        old_icon = u.icon.split('/')[-1]
        u.icon = url
        s.commit()

    old_icon_full = f'/usericon/{old_icon}' if old_icon is not None else None
    if old_icon_full and os.path.exists(old_icon_full):
        os.remove(old_icon_full)

    return url
