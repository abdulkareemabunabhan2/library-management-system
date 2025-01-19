import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Type
from db import get_session
from models import MemberBase, Member

router = APIRouter()

# Member Endpoints:
# POST /members/: Add a new member.
@router.post("/")
async def create_member(member_data: MemberBase, session: Session = Depends(get_session)) -> Member:
    member_db = Member(name= member_data.name, email=member_data.email)
    session.add(member_db)
    session.commit()
    session.refresh(member_db)
    return member_db

# GET /members/: View all members.
@router.get("/")
async def members(session: Session = Depends(get_session)) -> list[Member]:
    db_members = session.exec(select(Member)).all()
    return list(db_members)

# GET /members/{member_id}: View a specific member by ID.
@router.get("/{member_id}")
async def member(member_id: uuid.UUID, session: Session = Depends(get_session)) -> Member:
    db_member = session.get(Member, member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail=f"there is no member with this id: {member_id}")
    return db_member

# PUT /members/{member_id}: Update member details.
@router.put('/{member_id}')
async def book_update(member_id: uuid.UUID, member_data: MemberBase, session: Session = Depends(get_session)) -> Member:
    db_member = session.get(Member, member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail=f"No db_member found with this Id: {member_id}")
    db_member.name = member_data.name
    db_member.email = member_data.email
    session.commit()
    session.refresh(db_member)
    return db_member

# DELETE /members/{member_id}: Delete a member.
@router.delete("/{member_id}")
async def member_delete(member_id: uuid.UUID, session: Session = Depends(get_session)) -> uuid.UUID:
    db_member = session.get(Member, member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail=f"No member found with this Id: {member_id}")
    session.delete(db_member)
    session.commit()

    deleted_member = session.get(Member, member_id)
    if deleted_member is not None:
        raise HTTPException(status_code=500, detail="Failed to delete the member")
    return member_id
