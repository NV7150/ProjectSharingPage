from typing import Optional, List
from fastapi import FastAPI, Cookie, HTTPException, status
import random
from fastapi.param_functions import Query
import requests

import recommend


app = FastAPI(
    docs_url='/recommendapi/docs',
    openapi_url='/recommendapi/openapi.json',
)


@app.get('/recommendapi/')
async def index():
    return {'message': 'Hello, recommendapi!'}


@app.get(
    '/recommendapi/project',
    description='recommend project',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': List[int],
            'description': 'Successful Response (list of project-id)',
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
async def recommend_projects_with_usertoken(
    token: Optional[str] = Cookie(None),
    limit: Optional[int] = Query(None), offset: Optional[int] = Query(None)
):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    r = recommend.RecommendWithUsertoken(token)
    r.gather_projects()
    r.calc_point()

    sorted_projects = sorted(r.points.items(), key=lambda x: x[1],
                             reverse=True)

    result = []
    for p_id, _ in sorted_projects:
        # random project
        if random.randint(0, 9) % 3 == 0:
            resp = requests.get(
                'http://projectapi:8000/projectapi/project/random'
            )
            if resp.status_code != 200:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
            rand_id = resp.json()[0]
            if rand_id not in [x for x, _ in sorted_projects]:
                result.append(rand_id)

        result.append(p_id)

    if offset is None:
        return result[:limit]

    if limit is None:
        return result[offset:]

    return result[offset:offset+limit]


@app.get(
    '/recommendapi/project/no-user',
    description='Recommend projects without user-token',
    status_code=status.HTTP_200_OK,
)
async def recommend_projects_without_usertoken(
    limit: Optional[int] = Query(None), offset: Optional[int] = Query(None)
):
    endpoint = 'http://projectapi:8000/projectapi/project/all'
    sorted_by_like_resp = requests.get(
        f'{endpoint}?sort_by=LIKE&reverse=false'
    )
    if sorted_by_like_resp.status_code != 200:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    sorted_by_like: List[int] = sorted_by_like_resp.json()

    sorted_by_date_resp = requests.get(
        f'{endpoint}?sort_by=DATETIME&reverse=false'
    )
    if sorted_by_date_resp.status_code != 200:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    sorted_by_date: List[int] = sorted_by_date_resp.json()

    result: List[int] = []
    if len(sorted_by_date) != len(sorted_by_like):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    len_sorted_by_date = len(sorted_by_date)
    while len(result) < len_sorted_by_date:
        c = random.choice(['like', 'like', 'date'])  # like:date = 2:1
        print(c)
        if len(sorted_by_like) > 0 and c == 'like':
            p = sorted_by_like.pop()
            if p not in result:
                result.append(p)
        elif len(sorted_by_date) > 0 and c == 'date':
            p = sorted_by_date.pop()
            if p not in result:
                result.append(p)
        else:
            continue

    if offset is None:
        return result[:limit]

    if limit is None:
        return result[offset:]

    return result[offset:offset+limit]
