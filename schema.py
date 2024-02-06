import strawberry
from pydantic import BaseModel

@strawberry.type
class NoteType:
    id: int
    name: str
    description: str

@strawberry.input
class NoteInput:
    name: str
    description: str

@strawberry.type
class UserType:
    id: int
    email: str
    username: str
    full_name: str

@strawberry.input
class UserInput:
    full_name: str
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    token_expires_at: str

class TokenData(BaseModel):
    username: str | None = None