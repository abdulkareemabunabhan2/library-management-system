import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from library.application.book_service import BookService
from library.presntation.models import BookResponse

router = APIRouter()


# POST /books/: Add a new book.
@router.post('/')
async def add_book(
    book_data: dict[str, Any],
    service: BookService = Depends(BookService)
) -> Any:
    result = await service.add(book_data)
    book = result.to_dict()
    return BookResponse(**book)


# GET /books/: View all books.
@router.get('/')
async def get_books(service: BookService = Depends(BookService)) -> list[BookResponse]:
    books = await service.list()
    return [BookResponse(**book.to_dict()) for book in books]


# GET /books/{book_id}: View a specific book by ID.
@router.get('/{id}')
async def get_by_id(
    id: uuid.UUID,
    service: BookService = Depends(BookService)
) -> BookResponse:
    book = await service.get_by_id(id)
    if book is None:
        raise HTTPException(status_code=404, detail=f'Book with ID {id} not found.')
    book_data = book.to_dict()
    return BookResponse(**book_data)


# PUT /books/{book_id}: Update book details.
@router.put('/{id}')
async def update(
    id: uuid.UUID,
    data: dict[str, Any],
    service: BookService = Depends(BookService)
) -> BookResponse:
    book = await service.update(id, data)
    if book is None:
        raise HTTPException(status_code=404, detail=f'No book found with ID {id}.')
    book_data = book.to_dict()
    return BookResponse(**book_data)


# DELETE /books/{book_id}: Delete a book.
@router.delete('/{id}')
async def delete(
    id: uuid.UUID,
    service: BookService = Depends(BookService)
) -> uuid.UUID:
    result = await service.delete(id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'No book found with ID {id}.')
    return id
