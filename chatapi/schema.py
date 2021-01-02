from typing import Optional
from pydantic import BaseModel
import db
from datetime import datetime


class ForeignKeyError(Exception):
    pass


class Thread(BaseModel):
    id: int
    type: db.ThreadType
    status: db.ThreadStatus
    project_id: int
    title: str

    @classmethod
    def from_db(cls, db_thread: db.Thread):
        return cls(
            id=db_thread.id,
            type=db_thread.type,
            status=db_thread.status,
            project_id=db_thread.project_id,
            title=db_thread.title,
        )


class ThreadCreate(BaseModel):
    type: db.ThreadType
    status: db.ThreadStatus
    project_id: int
    title: str

    def create(self):
        with db.session_scope() as s:
            t = db.Thread(
                type=self.type,
                status=self.status,
                project_id=self.project_id,
                title=self.title,
            )
            s.add(t)
            s.commit()
            return Thread.from_db(t)


class Message(BaseModel):
    id: int
    thread_id: int
    username: str
    content: str
    created_at: datetime

    @classmethod
    def from_db(cls, db_msg: db.Message):
        return cls(
            id=db_msg.id,
            thread_id=db_msg.thread_id,
            username=db_msg.username,
            content=db_msg.content,
            created_at=db_msg.created_at,
        )


class MessageCreate(BaseModel):
    thread_id: int
    content: str

    def create(self, username: str):
        with db.session_scope() as s:
            thread = s.query(db.Thread).get(self.thread_id)
            if thread is None:
                raise ForeignKeyError

            m = db.Message(
                thread_id=thread.id,
                username=username,
                content=self.content,
                created_at=datetime.now(),
            )
            s.add(m)
            s.commit()
            return Message.from_db(m)
