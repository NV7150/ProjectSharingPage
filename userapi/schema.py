import enum
from pydantic import BaseModel
from fastapi import HTTPException, status
from typing import Optional, List, Any, Dict
import db
from functools import lru_cache


STANDARD_ICON = '/img/basic-user-icon.png'


@lru_cache(maxsize=4096)
def levenshtein_distance(s: str, t: str) -> int:
    s = s.upper()
    t = t.upper()
    if not s:
        return len(t)
    if not t:
        return len(s)
    if s[0] == t[0]:
        return levenshtein_distance(s[1:], t[1:])

    l1 = levenshtein_distance(s, t[1:])
    l2 = levenshtein_distance(s[1:], t)
    l3 = levenshtein_distance(s[1:], t[1:])
    return 1 + min(l1, l2, l3)


class SkillTag(BaseModel):
    id: int
    name: str
    parents: List  # List[SkillTag]

    @classmethod
    def from_db(cls, db_skilltag: db.SkillTag):
        # Tracing back the family tree
        print('DB_SKILLTAG', db_skilltag)
        db_parents: List[db.SkillTag] = []
        ds = db_skilltag
        while True:
            with db.session_scope() as s:
                parent_id = ds.parent_id
                parent = s.query(db.SkillTag).get(parent_id)

            if parent is None:
                break
            db_parents.append(parent)
            ds = parent

        parents = [
            SkillTag(id=dp.id, name=dp.name, parents=[])
            for dp in db_parents
        ]
        parents.reverse()

        return cls(
            id=db_skilltag.id,
            name=db_skilltag.name,
            parents=parents
        )

    @staticmethod
    def get(id: int) -> Optional[Any]:  # Optional[SkillTag]
        with db.session_scope() as s:
            t = s.query(db.SkillTag).get(id)
            if t is None:
                return None

            return SkillTag.from_db(t)

    @staticmethod
    def get_children(id: int) -> Optional[List[Any]]:
        with db.session_scope() as s:
            me = s.query(db.SkillTag).get(id)
            if me is None:
                return None

            t_l = s.query(db.SkillTag).filter(
                db.SkillTag.parent_id == me.id
            )
            return [SkillTag.from_db(t) for t in t_l]

    @staticmethod
    def get_bros(id: int) -> Optional[List[Any]]:
        # 兄弟タグ: 自身のparent_idと、parent_idが一致するタグたちを探す
        with db.session_scope() as s:
            me = s.query(db.SkillTag).get(id)
            if me is None:
                return None

            bros = s.query(db.SkillTag).filter(
                db.SkillTag.parent_id == me.parent_id
            )
            return [SkillTag.from_db(b) for b in bros if b.id != me.id]


class SkillTagLookup(BaseModel):
    result: List[SkillTag]
    is_next: bool

    @classmethod
    def get_list(
        cls, limit: Optional[int], offset: Optional[int]
    ):
        with db.session_scope() as s:
            q = s.query(db.SkillTag)
            count = q.count()
            if offset is not None:
                q = q.offset(offset)
            if limit is not None:
                q = q.limit(limit)

            s_count = q.count()
            if offset is not None:
                s_count += offset

            print(f'COUNT: {count}, S_COUNT: {s_count}, {count > s_count }')
            q = q.all()

            ins = cls(
                result=list(map(SkillTag.from_db, q)),
                is_next=count > s_count
            )
            return ins

    @classmethod
    def search(
        cls, keyword: str, limit: Optional[int], offset: Optional[int]
    ):
        with db.session_scope() as s:
            q = s.query(db.SkillTag).filter(
                db.SkillTag.name.like(f'%{keyword}%')
            )
            count = q.count()
            if offset is not None:
                q = q.offset(offset)
            if limit is not None:
                q = q.limit(limit)
            s_count = q.count()
            if offset is not None:
                s_count += offset

            q = q.all()

            ins = cls(
                result=list(map(SkillTag.from_db, q)),
                is_next=count > s_count
            )
            return ins


class SkillTagCreate(BaseModel):
    name: str
    parent_id: Optional[int]

    def create(self) -> Optional[SkillTag]:
        with db.session_scope() as s:
            # check name
            exists = s.query(db.SkillTag).filter(db.SkillTag.name == self.name)
            if exists.count() > 0:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)

            parent = None
            if self.parent_id is not None:
                parent = s.query(db.SkillTag).get(self.parent_id)
                if parent is None:
                    raise HTTPException(
                        status.HTTP_404_NOT_FOUND,
                        'Parent id not found'
                    )

                parent = parent.id

            already_exists = s.query(db.SkillTag).filter(
                db.SkillTag.name == self.name
            ).count()
            if already_exists > 0:
                raise HTTPException(
                    status.HTTP_429_TOO_MANY_REQUESTS,
                    'Tag already exists'
                )

            skilltag = db.SkillTag(
                name=self.name,
                parent_id=parent,
            )
            s.add(skilltag)
            s.commit()
            return SkillTag.from_db(skilltag)


class Sns(BaseModel):
    # SNS
    twitter: Optional[str]
    instagram: Optional[str]
    github: Optional[str]
    youtube: Optional[str]
    vimeo: Optional[str]
    facebook: Optional[str]
    tiktok: Optional[str]
    linkedin: Optional[str]
    wantedly: Optional[str]
    url: Optional[str]


class User(BaseModel):
    username: str
    display_name: str
    icon: Optional[str]
    bio: Optional[str]

    sns: Sns

    skilltags: List[SkillTag]

    @classmethod
    def from_db(cls, db_user: db.User):
        skilltags_db = db_user.skilltags
        skilltags = [
            SkillTag.from_db(x)
            for x in skilltags_db
        ]
        sns = Sns(
            twitter=db_user.twitter,
            instagram=db_user.instagram,
            github=db_user.github,
            youtube=db_user.youtube,
            vimeo=db_user.vimeo,
            facebook=db_user.facebook,
            tiktok=db_user.tiktok,
            linkedin=db_user.linkedin,
            wantedly=db_user.wantedly,
            url=db_user.url,
        )

        icon = db_user.icon
        if icon is None:
            icon = STANDARD_ICON
        print('ICON', icon)
        return cls(
            username=db_user.username,
            display_name=db_user.display_name,
            icon=icon,
            bio=db_user.bio,
            sns=sns,
            skilltags=skilltags
        )

    @classmethod
    def from_id(cls, id: int):
        with db.session_scope() as s:
            u = s.query(db.User).get(id)
            if u is None:
                raise ValueError('User not found.')

            return cls.from_db(u)


class UserUpdate():
    changable_fields = ['display_name', 'bio', 'email', 'sns', 'skilltags']
    changable_sns_fields = [
        'twitter', 'instagram', 'github', 'youtube',
        'vimeo', 'facebook', 'tiktok', 'linkedin',
        'wantedly', 'url',
    ]

    def __init__(self, userid: int, json):
        parsed_json: Dict = dict(json)
        # field check
        cf = self.changable_fields
        if len([x for x in parsed_json.keys() if x not in cf]) > 0:
            raise ValueError('Unnecessary filed(s) included')

        # sns field check
        if 'sns' in parsed_json.keys():
            if (sns := parsed_json['sns']) is not None:
                if type(sns) != dict:
                    raise ValueError('"sns" should be object')
                cf = self.changable_sns_fields
                if len([x for x in sns.keys() if x not in cf]) > 0:
                    raise ValueError(
                        'Unnecessary filed(s) included at sns field'
                    )

        # skilltags field check
        if 'skilltags' in parsed_json.keys():
            if (skilltags := parsed_json['skilltags']) is not None:
                if type(skilltags) != list:
                    raise ValueError('"skilltags" should be list')
                if len([x for x in skilltags if type(x) != int]) > 0:
                    raise ValueError('"skilltags" should be int list')

        self.userid = userid
        self.parsed_json = parsed_json

    def update(self) -> Optional[User]:
        with db.session_scope() as s:
            u: Optional[db.User] = s.query(db.User).get(self.userid)
            if u is None:
                return None

            update_ = {
                'display_name': 'u.display_name = v',
                'email': 'u.email = v',
                'bio': 'u.bio = v',
            }
            sns_ = {
                'twitter': 'u.twitter = sv',
                'instagram': 'u.instagram = sv',
                'github': 'u.github = sv',
                'youtube': 'u.youtube = sv',
                'vimeo': 'u.vimeo = sv',
                'facebook': 'u.facebook = sv',
                'tiktok': 'u.tiktok = sv',
                'linkedin': 'u.linkedin = sv',
                'wantedly': 'u.wantedly = sv',
                'url': 'u.url = sv',
            }
            for k, v in self.parsed_json.items():
                if k == 'sns':
                    if v is None:
                        u.twitter = None
                        u.instagram = None
                        u.github = None
                        u.youtube = None
                        u.vimeo = None
                        u.facebook = None
                        u.tiktok = None
                        u.linkedin = None
                        u.wantedly = None
                        u.url = None
                    else:
                        for sk, sv in v.items():
                            exec(sns_[sk])
                elif k == 'skilltags':
                    if v is None:
                        u.skilltags = []
                    else:
                        u.skilltags = []
                        for i in map(int, v):
                            t = s.query(db.SkillTag).get(i)
                            if t is None:
                                return None
                            u.skilltags.append(t)
                else:
                    exec(update_[k])

            s.commit()

            return User.from_db(u)


class UserSearchResult(BaseModel):
    all_result: List[User]
    username: List[User]
    display_name: List[User]
    all_result_total: int
    username_total: int
    display_name_total: int

    @classmethod
    def search(cls, keyword, limit: Optional[int], offset: Optional[int]):
        with db.session_scope() as s:
            username_list = s.query(db.User).filter(
                db.User.username.like(f'%{keyword}%')
            ).all()
            displayname_list = s.query(db.User).filter(
                db.User.display_name.like(f'%{keyword}%')
            ).all()

            # get levenshtein
            username_lsd = [
                levenshtein_distance(keyword, u.username)
                for u in username_list
            ]
            displayname_lsd = [
                levenshtein_distance(keyword, u.display_name)
                for u in displayname_list
            ]

            # get sorted index
            username_sort_index = sorted(
                range(len(username_lsd)),
                key=lambda i: username_lsd[i]
            )
            displayname_sort_index = sorted(
                range(len(displayname_lsd)),
                key=lambda i: displayname_lsd[i]
            )

            u_sort_idx = 0  # current sorted_username index
            d_sort_idx = 0  # current sorted_displayname index
            u_idx = 0
            d_idx = 0
            all_sorted = []
            while True:
                try:
                    u_idx = username_sort_index[u_sort_idx]
                except IndexError:
                    # finish
                    for d_idx in displayname_sort_index[d_sort_idx:]:
                        d = displayname_list[d_idx]
                        if d not in all_sorted:
                            all_sorted.append(d)
                    break
                try:
                    d_idx = displayname_sort_index[d_sort_idx]
                except IndexError:
                    # finish
                    for u_idx in username_sort_index[u_sort_idx:]:
                        u = username_list[u_idx]
                        if u not in all_sorted:
                            all_sorted.append(u)
                    break

                u_lsd = username_lsd[u_idx]
                d_lsd = displayname_lsd[d_idx]
                if u_lsd < d_lsd:
                    u = username_list[u_idx]
                    if u not in all_sorted:
                        all_sorted.append(u)
                    u_sort_idx += 1
                    continue

                d = displayname_list[d_idx]
                if d not in all_sorted:
                    all_sorted.append(d)
                d_sort_idx += 1

            all_sorted = [
                User.from_id(u.id)
                for u in all_sorted
            ]
            username_sorted = [
                User.from_id(username_list[i].id)
                for i in username_sort_index
            ]
            displayname_sorted = [
                User.from_id(displayname_list[i].id)
                for i in displayname_sort_index
            ]

            if offset is None:
                return cls(
                    all_result=all_sorted[:limit],
                    username=username_sorted[:limit],
                    display_name=displayname_sorted[:limit],
                    all_result_total=len(all_sorted),
                    username_total=len(username_sorted),
                    display_name_total=len(displayname_sorted),
                )

            if limit is None:
                return cls(
                    all_result=all_sorted[offset:],
                    username=username_sorted[offset:],
                    display_name=displayname_sorted[offset:],
                    all_result_total=len(all_sorted),
                    username_total=len(username_sorted),
                    display_name_total=len(displayname_sorted),
                )

            return cls(
                all_result=all_sorted[:limit],
                username=username_sorted[:limit],
                display_name=displayname_sorted[:limit],
                all_result_total=len(all_sorted),
                username_total=len(username_sorted),
                display_name_total=len(displayname_sorted),
            )


class LoginUser(User):
    email: str

    @staticmethod
    def from_db(db_user: db.User):
        skilltags_db = db_user.skilltags
        skilltags = [
            SkillTag.from_db(x)
            for x in skilltags_db
        ]
        sns = Sns(
            twitter=db_user.twitter,
            instagram=db_user.instagram,
            github=db_user.github,
            youtube=db_user.youtube,
            vimeo=db_user.vimeo,
            facebook=db_user.facebook,
            tiktok=db_user.tiktok,
            linkedin=db_user.linkedin,
            wantedly=db_user.wantedly,
            url=db_user.url,
        )

        icon = db_user.icon
        if icon is None:
            icon = STANDARD_ICON
        return LoginUser(
            username=db_user.username,
            email=db_user.email,
            display_name=db_user.display_name,
            icon=icon,
            bio=db_user.bio,
            sns=sns,
            skilltags=skilltags
        )

    @classmethod
    def from_token(cls, token: str) -> Optional[Any]:
        with db.session_scope() as s:
            # check token
            t: Optional[db.Token] = db.Token.get_token(token)
            if t is None:
                return None

            user: Optional[db.User] = s.query(db.User).get(t.user_id)
            if user is None:
                return None

            return cls.from_db(user)


class UserCreate(BaseModel):
    username: str
    email: str
    raw_password: str
    display_name: str
    icon: Optional[str]
    bio: Optional[str]

    # SNS
    twitter: Optional[str]
    instagram: Optional[str]
    github: Optional[str]
    youtube: Optional[str]
    vimeo: Optional[str]
    facebook: Optional[str]
    tiktok: Optional[str]
    linkedin: Optional[str]
    wantedly: Optional[str]
    url: Optional[str]

    skilltags: List[int]

    def create(self) -> Optional[User]:
        db_skilltags = []
        with db.session_scope() as s:
            exists = s.query(db.User).filter(db.User.username == self.username)
            if exists.count() > 0:
                raise HTTPException(
                    status.HTTP_409_CONFLICT,
                    'username already exists',
                )
            exists = s.query(db.User).filter(db.User.email == self.email)
            if exists.count() > 0:
                raise HTTPException(
                    status.HTTP_409_CONFLICT,
                    'email already exists',
                )

            for tagid in self.skilltags:
                tag = s.query(db.SkillTag).get(tagid)
                if tag is None:
                    return None
                db_skilltags.append(tag)

        user = db.User.create(
            raw_password=self.raw_password,
            username=self.username,
            email=self.email,
            display_name=self.display_name,
            icon=self.icon,
            bio=self.bio,
            twitter=self.twitter,
            instagram=self.instagram,
            github=self.github,
            youtube=self.youtube,
            vimeo=self.vimeo,
            facebook=self.facebook,
            tiktok=self.tiktok,
            linkedin=self.linkedin,
            wantedly=self.wantedly,
            url=self.url,
            skilltags=db_skilltags,
        )
        with db.session_scope() as s:
            s.add(user)
            s.commit()
            return User.from_db(user)


class UserToken(BaseModel):
    raw_token: str

    def auth(self) -> bool:
        t = db.Token.get_token(self.raw_token)
        if t is None:
            return False
        return True

    def expire(self) -> bool:
        token: Optional[db.Token] = db.Token.get_token(self.raw_token)
        if token is None:
            return False
        token.expire()
        return True


class UserLogin(BaseModel):
    username: str
    raw_password: str
    remember_password: bool

    def login(self) -> Optional[str]:
        with db.session_scope() as s:
            users: List[db.User] = list(
                s.query(db.User).filter(
                    db.User.username == self.username
                )
            )
            if len(users) != 1:
                return None

            user: db.User = users[0]
            if user.login(self.raw_password) is False:
                return None

            token = db.Token.issue_token(user)
            return token


class UserDelete(BaseModel):
    username: str
    raw_password: str

    def delete(self, token: str) -> bool:
        userid = db.Token.get_userid(token)
        with db.session_scope() as s:
            user = s.query(db.User).get(userid)
            if user.username != self.username:
                return False
            if user.login(self.raw_password) is False:
                return False

            user.delete()
            s.commit()

        return True


class PasswordUpdateResult(enum.Enum):
    TOKEN_WRONG = enum.auto()
    OLD_PASSWORD_WRONG = enum.auto()
    USER_NOT_FOUND = enum.auto()
    SUCCESS = enum.auto()


class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str

    def update(self, token: str) -> PasswordUpdateResult:
        t = db.Token.get_token(token)
        if t is None:
            return PasswordUpdateResult.TOKEN_WRONG

        with db.session_scope() as s:
            userid = db.Token.get_userid(token)
            user = s.query(db.User).get(userid)

            if user.is_active is False:
                return PasswordUpdateResult.USER_NOT_FOUND

            if user.login(self.old_password) is False:
                return PasswordUpdateResult.OLD_PASSWORD_WRONG
            result = user.set_password(self.new_password)
            if result is False:
                return PasswordUpdateResult.USER_NOT_FOUND
            s.commit()

        return PasswordUpdateResult.SUCCESS
