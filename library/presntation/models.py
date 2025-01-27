from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class MemberCreate(BaseModel):
    name: str
    email: EmailStr


class MemberResponse(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime
    updated_at: datetime | None


class BookCreate(BaseModel):
    title: str
    author: str


class BookResponse(BaseModel):
    id: UUID
    title: str
    author: str
    is_borrowed: bool | None = False
    created_at: datetime
    updated_at: Optional[datetime]
    borrowed_date: Optional[datetime]
    borrowed_by: UUID | None = None
