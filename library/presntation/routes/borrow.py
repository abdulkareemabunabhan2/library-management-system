import uuid

from fastapi import APIRouter, Depends, HTTPException

from library.application.book_service import BookService
from library.application.shared.exceptions import DataNotFoundException
from library.presntation.models import BookResponse

router = APIRouter()


# Book Borrowing Endpoints:
# POST /borrow/{book_id}/{member_id}: Borrow a book.
@router.post('/borrow/{book_id}/{member_id}')
async def borrow(book_id: uuid.UUID, member_id: uuid.UUID, service: BookService = Depends(BookService)) -> BookResponse:
    try:
        book = await service.borrow_book(book_id, member_id)
        return BookResponse(**book.to_dict())
    except DataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=400, detail=f'Book with id {book_id} is already borrowed')


# POST /return/{book_id}: Return a borrowed book.
@router.post('/return/{book_id}')
async def return_book(book_id: uuid.UUID, service: BookService = Depends(BookService)) -> BookResponse:
    try:
        book = await service.return_book(book_id)
        return BookResponse(**book.to_dict())
    except DataNotFoundException:
        raise HTTPException(status_code=404, detail=f'No book found with this Id: {book_id}')
    except ValueError:
        raise HTTPException(status_code=400, detail=f'Book with id {book_id} is not borrowed')
