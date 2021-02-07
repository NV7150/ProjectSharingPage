from typing import Dict, Optional, List
from fastapi import FastAPI, Cookie, HTTPException, status
import requests
import schema


app = FastAPI(
    docs_url='/recommendapi/docs',
    openapi_url='/recommendapi/openapi.json',
)


@app.get('/recommendapi/')
async def index():
    return {'message': 'Hello, recommendapi!'}


class Recommend(object):
    def __init__(self, token: str) -> None:
        self.__get_user()  # get user
        self.__get_userskilltags()  # get skilltags

        # 持っているタグ
        self.tags: List[int] = [t['id'] for t in self.raw_user_skilltags]

        # 親タグ (父母まで。祖父母までは今の所遡らない)
        self.parent_tags: List[int] = []
        for t in self.raw_user_skilltags:
            self.parent_tags.append(
                *[t.id for t in t['parents']]
            )

        # 子タグ

        # 兄弟タグ(親タグが共通)

    def __get_user(self):
        cookies = {'token': self.token}
        userresp = requests.get('http://userapi:8000/userapi/user',
                                cookies=cookies)
        if userresp.status_code != 200:
            if userresp.status_code == 404:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    'User not found.')
            else:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    'Can\'t get user info')
        user = userresp.json()
        self.user = user

    def __get_userskilltags(self):
        cookies = {'token': self.token}
        userresp = requests.get('http://userapi:8000/userapi/user',
                                cookies=cookies)
        if userresp.status_code != 200:
            if userresp.status_code == 404:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    'User not found.')
            else:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    'Can\'t get user info')
        user = userresp.json()
        skilltags: List[Dict] = user['skilltags']
        self.raw_user_skilltags = skilltags


@app.get(
    '/recommendapi/project',
    description='recommend project',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': List[schema.Project],
            'description': 'Successful Response',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Not logged in (cookie token is required)'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'User not found.',
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Internal server error'
        }
    },
)
async def project(token: Optional[str] = Cookie(None)):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    r = Recommend(token)
