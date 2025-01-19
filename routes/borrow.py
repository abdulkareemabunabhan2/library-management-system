import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Type
from db import get_session
from models import Book, Member
from datetime import datetime, timezone

router = APIRouter()
# Book Borrowing Endpoints:
# POST /borrow/{book_id}/{member_id}: Borrow a book.
@router.post("/borrow/{book_id}/{member_id}")
async def borrow(book_id: uuid.UUID, member_id: uuid.UUID, session: Session = Depends(get_session)) -> Book:
    book: Book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"No book found with this Id: {book_id}")
    if book.is_borrowed:
        raise HTTPException(status_code=400, detail=f"Book with id {book_id} is already borrowed")
    member = session.get(Member, member_id)
    if member is None:
        raise HTTPException(status_code=404, detail=f"No member found with this Id: {member_id}")
    book.is_borrowed = True
    book.borrowed_by = member_id
    book.borrowed_date = datetime.now(timezone.utc)
    session.commit()
    session.refresh(book)
    return book

# POST /return/{book_id}: Return a borrowed book.
@router.post("/return/{book_id}")
async def return_book(book_id: uuid.UUID, session: Session = Depends(get_session)) -> Book:
    book: Book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"No book found with this Id: {book_id}")
    if book.is_borrowed is False:
        raise HTTPException(status_code=400, detail=f"Book with id {book_id} is not borrowed")
    book.is_borrowed = False
    book.borrowed_by = None
    book.borrowed_date = None
    session.commit()
    session.refresh(book)
    return book