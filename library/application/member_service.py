from typing import Any
from uuid import UUID

from library.application.services import get_work_service
from library.application.shared.exceptions import DataNotFoundException
from library.domain.member.entity import MemberEntity


class MemberService:

    # add a member service
    async def add(self, member: dict[str, Any]) -> MemberEntity:
        """
        This method allows you to add member.
        """
        member_data = MemberEntity.from_dict(member)
        async with get_work_service() as work_service:
            return await work_service.member_repo.add(member_data)

    # List all members
    async def list(self) -> list[MemberEntity]:
        """
        This method lists all members in the repository.
        """
        async with get_work_service() as work_service:
            return await work_service.member_repo.get_all()

    # get member by id
    async def get_by_id(self, id: UUID) -> MemberEntity:
        """
        Get a book by its Id.
        """
        async with get_work_service() as work_service:
            if not (member := await work_service.member_repo.get_by_id(id)):
                raise DataNotFoundException(f'There is No member with {id} found')
            return member

    async def update(self, id: UUID, data: dict[str, Any]) -> MemberEntity:
        async with get_work_service() as work_service:
            if not await work_service.member_repo.get_by_id(id):
                raise DataNotFoundException(f'Member with ID {id} not found.')
            return await work_service.member_repo.update(id, data)

    async def delete(self, id: UUID) -> MemberEntity | None:
        async with get_work_service() as work_service:
            if not await work_service.member_repo.get_by_id(id):
                raise DataNotFoundException(f'Member with ID {id} not found.')
            return await work_service.member_repo.delete(id)
