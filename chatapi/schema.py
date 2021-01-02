from pydantic import BaseModel
import db


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
