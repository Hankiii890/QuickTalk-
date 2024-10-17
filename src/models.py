from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    fullname: str | None = None
    password: str
    disable: bool

