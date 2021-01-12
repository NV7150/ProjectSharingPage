import requests
from typing import Optional


class UserAPIError(Exception):
    pass


def auth(token: str) -> Optional[str]:
    """Auth
    Parameters
    ----------
    token: str
        User token

    Returns
    -------
    username: Optional[str]
        if success:
            return username
        else:
            None
    """
    cookies = {'token': token}
    resp = requests.get(
        'http://userapi:8000/userapi/user',
        cookies=cookies,
    )
    if resp.status_code not in [200, 401, 404]:
        # failed
        raise UserAPIError

    if resp.status_code != 200:
        return None

    result = resp.json()
    username: Optional[str] = None
    try:
        username = result['username']
    except KeyError:
        raise UserAPIError

    if type(username) != str:
        raise UserAPIError

    return username


def exist(username: str) -> bool:
    resp = requests.get(
        f'http://userapi:8000/userapi/user/{username}',
    )
    if resp.status_code not in [200, 404]:
        raise UserAPIError
    if resp.status_code != 200:
        return False

    return True


def tag_exist(tag_id: int) -> bool:
    resp = requests.get(
        f'http://userapi:8000/userapi/skilltag/{tag_id}'
    )
    if resp.status_code not in [200, 404]:
        raise UserAPIError
    if resp.status_code != 200:
        return False

    return True
