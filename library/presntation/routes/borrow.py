import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from library.application.book_service import BookService
from library.application.services import get_book_service
from library.infrastructure.database.db import get_async_session
from library.presntation.models import BookBase, BookResponse

router = APIRouter()
# Book Borrowing Endpoints:
# POST /borrow/{book_id}/{member_id}: Borrow a book.
@router.post("/borrow/{book_id}/{member_id}")
async def borrow(book_id: uuid.UUID, member_id: uuid.UUID, service: BookService = Depends(get_book_service)) -> BookResponse:
    book = await service.borrow_book(book_id, member_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"No book found with this Id: {book_id}")
    return book

# POST /return/{book_id}: Return a borrowed book.
@router.post("/return/{book_id}")
async def return_book(book_id: uuid.UUID, service: BookService = Depends(get_book_service)) -> BookResponse:
    book = await service.return_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"No book found with this Id: {book_id}")
    return BookResponse(**book)