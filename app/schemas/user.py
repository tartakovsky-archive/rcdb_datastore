from pydantic import BaseModel, constr


class User(BaseModel):
    username: constr(min_length=4, max_length=64)
    is_active: bool


class UserDB(User):
    id: int
    password: constr(min_length=8, max_length=200)
