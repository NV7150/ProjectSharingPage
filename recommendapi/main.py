from typing import Dict, Optional, List
from fastapi import FastAPI, Cookie, HTTPException, status
import requests
import schema
import math


app = FastAPI(
    docs_url='/recommendapi/docs',
    openapi_url='/recommendapi/openapi.json',
)


@app.get('/recommendapi/')
async def index():
    return {'message': 'Hello, recommendapi!'}


class Recommend(object):
    # TODO: 1. 点数付け. ソート.
    # TODO: 2. ランダムなプロジェクトを取ってくる. ランダムに挿入

    def __init__(self, token: str) -> None:
        self.token = token
        self.__get_user()  # get user
        self.raw_user_skilltags: List[Dict] = self.user['skilltags']

        # 持っているタグ
        self.tags: List[int] = [t['id'] for t in self.raw_user_skilltags]

        # 親タグ (父母まで。祖父母までは今の所遡らない)
        self.parent_tags: List[int] = []
        for t in self.raw_user_skilltags:
            for p in t['parents']:
                self.parent_tags.append(p['id'])

        self.child_tags: List[int] = []
        self.bro_tags: List[int] = []
        self.__get_children()  # 子タグ
        self.__get_bros()  # 兄弟タグ(親タグが共通)

        self.tag_projects: List[Dict] = []
        self.parent_tag_projects: List[Dict] = []
        self.child_tag_projects: List[Dict] = []
        self.bro_tag_projects: List[Dict] = []

        self.points: Dict[int, int] = dict()  # k: project.id, v: point

    def gather_projects(self):
        pairs = [
            (self.tags, self.tag_projects),
            (self.parent_tags, self.parent_tag_projects),
            (self.child_tags, self.child_tag_projects),
            (self.bro_tags, self.bro_tag_projects),
        ]
        for tags, projects in pairs:
            query = {'tags': tags}
            resp = requests.get('http://projectapi:8000/projectapi/project',
                                params=query)
            if resp.status_code != 200:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
            projects.clear()
            for p in resp.json():
                projects.append(p)

    def calc_point(self):
        # tag-distance
        point_table = [
            (1, self.tag_projects),
            (0.4, self.child_tag_projects),
            (0.4, self.parent_tag_projects),
            (0.2, self.bro_tag_projects),
        ]
        for point, projects in point_table:
            for project in projects:
                p_id = project['id']
                current = self.points.get(p_id)
                if current is None:
                    likes = project['likes']
                    if likes < 1:
                        likes = 1
                    like_point = math.log(likes, 5)
                    self.points[p_id] = point + like_point
                else:
                    self.points[p_id] += point

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

    def __get_children(self):
        cookies = {'token': self.token}
        for t in self.tags:
            resp = requests.get(
                f'http://userapi:8000/userapi/skilltag/{t}/children',
                cookies=cookies
            )
            if resp.status_code != 200:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    f'Can\'t get child tags (tag={t})')
            children: List[Dict] = resp.json()
            for c in children:
                self.child_tags.append(c['id'])

    def __get_bros(self):
        cookies = {'token': self.token}
        for t in self.tags:
            resp = requests.get(
                f'http://userapi:8000/userapi/skilltags/{t}/bros',
                cookies=cookies
            )

            if resp.status_code != 200:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    f'Can\'t get bros (tag={t})')
            bros: List[Dict] = resp.json()
            for b in bros:
                self.bro_tags.append(b['id'])


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
    r.gather_projects()
    r.calc_point()
    
    return r  # DEBUG
