import requests
from typing import Optional


class ProjectAPIError(Exception):
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
    if resp.status_code != 200:
        # failed
        return None

    result = resp.json()
    username: Optional[str] = None
    try:
        username = result['username']
    except KeyError:
        return None

    if type(username) != str:
        return None

    return username


def check_proj_member(proj_id: int, username: str) -> Optional[bool]:
    """Check user in project as member
    Parameters
    ----------
    proj_id: int
    username: str

    Returns
    -------
    result: Optional[bool]
        if proj_id not found:
            return None
        else:
            True or False
    """
    resp = requests.get(
        f'http://projectapi:8000/projectapi/project/{proj_id}'
    )

    if resp.status_code not in [404, 200]:
        raise ProjectAPIError

    if resp.status_code == 400:
        return None

    resp_json = resp.json()
    if username not in resp_json['members']:
        return False

    return True
