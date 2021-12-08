from pydantic import BaseModel


class User(BaseModel):
    username: str


class Update(BaseModel):
    hash: str  # hashed username of updated user
    column: int
    row: int
