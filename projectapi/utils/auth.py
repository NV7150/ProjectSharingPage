import requests
from typing import Optional


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
