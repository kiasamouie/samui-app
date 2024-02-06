from typing import List

import strawberry

from Service.note import NoteService
from Service.user import UserService
from schema import NoteType, UserType


@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "Hello World!"

    @strawberry.field
    async def get_all(self) -> List[NoteType]:
        return await NoteService.get_all_note()

    @strawberry.field
    async def get_by_id(self, id: int) -> NoteType:
        return await NoteService.get_by_id(id)

    @strawberry.field
    async def get_all_users(self) -> List[UserType]:
        return await UserService.get_all_users()

    @strawberry.field
    async def get_user_by_id(self, id: int) -> UserType:
        return await UserService.get_by_id(id)