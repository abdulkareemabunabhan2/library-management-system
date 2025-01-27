from sqlalchemy.ext.asyncio import AsyncConnection

from library.domain.member.entity import MemberEntity
from library.infrastructure.database.schema import Member
from library.infrastructure.repositories.base_repository import BaseRepository


class MemberRepository(BaseRepository[MemberEntity]):
    def __init__(self, connection: AsyncConnection):
        super().__init__(connection, MemberEntity, Member)
