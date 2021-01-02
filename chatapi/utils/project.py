import requests


class ProjectAPIException(Exception):
    pass


def project_exist_check(proj_id: int) -> bool:
    resp = requests.get(
        f'http://projectapi:8000/projectapi/project/{proj_id}',
    )
    if resp.status_code == 200:
        return True
    elif resp.status_code == 404:
        return False
    else:
        raise ProjectAPIException
