import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr

class MemberBase(BaseModel):
    name: str
    email: EmailStr

class MemberCreate(MemberBase):
    pass

class MemberResponse(MemberBase):
    member_id: uuid.UUID

class BookBase(BaseModel):
    title: str
    author: str

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    book_id: uuid.UUID
    is_borrowed: bool = False
    borrowed_date: datetime | None = None
    borrowed_by: uuid.UUID | None = None
