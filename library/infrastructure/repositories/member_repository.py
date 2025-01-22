from typing import TypeVar, Generic, Any
from uuid import UUID
from sqlalchemy import insert, select, update, delete
from sqlmodel.ext.asyncio.session import AsyncSession
from library.domain.member_type.entity import MemberType
from library.infrastructure.database.schema import Member
T = TypeVar('T', bound=MemberType)
class MemberRepository(Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    # add(member),
    async def add(self, member_data: T) -> dict[str, Any] | None:
        """
        Add new member to the database.
        """
        member = member_data.to_dict(member_data.config.db_excluded_fields)
        command = insert(Member).values(member)
        result = await self.session.execute(command)
        await self.session.commit()
        member_id = result.inserted_primary_key[0]
        inserted_member = await self.session.execute(
            select(Member).where(Member.c.member_id == member_id)
        )
        member_dict = inserted_member.fetchone()._asdict() if inserted_member else {}
        return member_dict

    # get(member_id),
    async def get(self, member_id: UUID) -> dict[str, Any] | None:
        """
        Get member by id from the database
        """
        command = select(Member).where(Member.c.member_id == member_id)
        result = await self.session.execute(command)
        row = result.fetchone()
        if not row:
            return None
        return row._asdict()

    # list(),
    async def list(self) -> list[dict[str, Any]] | None:
        command = select(Member)
        result = await self.session.execute(command)
        rows = result.fetchall()
        print(f"this is rows : {rows}")
        return [dict(row._mapping) for row in rows]

    # delete(member_id),
    async def delete(self, member_id: UUID) -> UUID | None:
        """
        Delete Member from the database
        """
        command = delete(Member).where(Member.c.member_id == member_id)
        result = await self.session.execute(command)
        await self.session.commit()
        if result.rowcount == 0:
            return None
        return member_id

    # update(member_data)
    async def update(self, data: dict[str, Any]) -> dict[str, Any] | None:
        update_data = {k: v for k, v in data.items() if k not in MemberType.config.db_excluded_fields}
        command = update(Member).where(Member.c.member_id == data["member_id"]).values(**update_data).returning(*Member.c)
        result = await self.session.execute(command)
        row = result.fetchone()
        if not row:
            raise None
        await self.session.commit()
        return row._asdict()
