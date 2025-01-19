import uuid
from datetime import date

from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class MemberBase(SQLModel):
    name: str
    email: EmailStr

class Member(MemberBase, table=True):
    member_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class BookBase(SQLModel):
    title: str
    author: str

class Book(BookBase, table=True):
    book_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    is_borrowed: bool = False
    borrowed_date: date | None = None
    borrowed_by: uuid.UUID | None = Field(default=None, foreign_key="member.member_id")

class BookResponse(BookBase):
    book_id: uuid.UUID
    is_borrowed: bool
    borrowed_date: date | None = None
    borrowed_by: uuid.UUID | None = None
