from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from library.application.member_service import MemberService
from library.application.shared.exceptions import DataNotFoundException
from library.presntation.models import MemberCreate, MemberResponse

router = APIRouter()


# Member Endpoints:
# POST /members/: Add a new member.
@router.post('/')
async def create_member(data: MemberCreate, service: MemberService = Depends(MemberService)) -> MemberResponse:
    member = await service.add(data.model_dump())
    member_data = member.to_dict()
    return MemberResponse(**member_data)


# GET /members/: View all members.
@router.get('/')
async def get_all(service: MemberService = Depends(MemberService)) -> list[MemberResponse]:
    db_members = await service.list()
    if not db_members:
        raise HTTPException(status_code=500, detail=f'Database error')
    return [MemberResponse(**member.to_dict()) for member in db_members]


# GET /members/{member_id}: View a specific member by ID.
@router.get('/{id}')
async def get_by_id(id: UUID, service: MemberService = Depends(MemberService)) -> MemberResponse:
    try:
        db_member = await service.get_by_id(id)
        member_data = db_member.to_dict()
        return MemberResponse(**member_data)
    except DataNotFoundException:
        raise HTTPException(status_code=404, detail=f'there is no member with id {id}')


# PUT /members/{member_id}: Update member details.
@router.put('/{id}')
async def update(id: UUID, data: MemberCreate, service: MemberService = Depends(MemberService)) -> MemberResponse:
    update_data = data.model_dump()
    try:
        db_member = await service.update(id, update_data)
        member_data = db_member.to_dict()
        return MemberResponse(**member_data)
    except DataNotFoundException:
        raise HTTPException(status_code=404, detail=f'No member found with this Id: {id}')


# DELETE /members/{member_id}: Delete a member.
@router.delete('/{id}')
async def delete(id: UUID, service: MemberService = Depends(MemberService)) -> UUID:
    try:
        await service.delete(id)
        return id
    except DataNotFoundException:
        raise HTTPException(status_code=404, detail=f'No member found with this Id: {id}')
