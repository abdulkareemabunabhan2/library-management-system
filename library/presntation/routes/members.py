import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from library.application.member_service import MemberService
from library.application.services import get_member_service
from library.domain.member_type.entity import MemberType
from library.infrastructure.database.db import get_async_session
from library.infrastructure.repositories.member_repository import MemberRepository
from library.presntation.models import MemberBase, MemberResponse
from library.application.services import get_member_repo
router = APIRouter()

# Member Endpoints:
# POST /members/: Add a new member.
@router.post("/")
async def create_member(member_data: MemberBase, service: MemberService = Depends(get_member_service)) -> MemberResponse:
    member_db = MemberBase(name= member_data.name, email=member_data.email)
    member = await service.add_member(MemberType.from_dict(member_db.model_dump()))
    return MemberResponse(**member)

# GET /members/: View all members.
@router.get("/")
async def members(member_repo: MemberRepository = Depends(get_member_repo)) -> list[MemberResponse]:
    db_members = await member_repo.list()
    return [MemberResponse(**member) for member in db_members]

# GET /members/{member_id}: View a specific member by ID.
@router.get("/{member_id}")
async def member(member_id: uuid.UUID, repo: MemberRepository = Depends(get_member_repo)) -> MemberResponse:
    db_member = await repo.get(member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail=f"there is no member with this id: {member_id}")
    return MemberResponse(**db_member)

# PUT /members/{member_id}: Update member details.
@router.put('/{member_id}')
async def member_update(member_id: uuid.UUID, member_data: MemberBase, service: MemberService = Depends(get_member_service)) -> MemberResponse:
    data = member_data.model_dump()
    data["member_id"] = member_id
    db_member = await service.update_member(data)
    if db_member is None:
        raise HTTPException(status_code=404, detail=f"No db_member found with this Id: {member_id}")
    return MemberResponse(**db_member)

# DELETE /members/{member_id}: Delete a member.
@router.delete("/{member_id}")
async def member_delete(member_id: uuid.UUID, service: MemberService = Depends(get_member_service)) -> uuid.UUID:
    db_member = await service.delete_member(member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail=f"No member found with this Id: {member_id}")
    return member_id
