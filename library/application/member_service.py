from uuid import UUID
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from library.domain.member_type.entity import MemberType
from library.infrastructure.repositories.member_repository import MemberRepository

class MemberService:
    def __init__(self, member_repo: MemberRepository, session: AsyncSession):
        self.member_repo = member_repo
        self.session = session

    async def add_member(self, member: MemberType) -> dict[str, Any] | None:
        """
        This method allows you to add member.
        """
        return await self.member_repo.add(member)

    async def update_member(self, data: dict[str, Any]) -> dict[str, Any] | None:
        """
        This method allows you to update member data if he already exists
        """
        if 'member_id' not in data:
            raise KeyError("The 'member_id' field is required to update a member.")
        member_id = data["member_id"]
        if not data:
            raise Exception("No data provided for update.")

        member = await self.member_repo.get(member_id)

        if not member:
            raise Exception(f"Member with ID {member_id} not found.")

        return await self.member_repo.update(data)

    async def delete_member(self, member_id: UUID) -> UUID | None:
        """
        This method allows you to delete a member by id.
        """
        member = await self.member_repo.get(member_id)
        if not member:
            return None
        return await self.member_repo.delete(member_id)
