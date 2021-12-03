from pydantic import BaseModel


class User(BaseModel):
    username: str


class Update(BaseModel):
    user: str  # username of updated user
    column: int
    row: int
