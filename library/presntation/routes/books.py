import uuid

from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from library.infrastructure.repositories.books_repository import BookRepository
from library.presntation.models import BookResponse
from library.domain.book_type.entity import BookType
from library.application.services import get_book_repo

router = APIRouter()
# Book Endpoints:
# POST /books/: Add a new book.
@router.post("/")
async def add_book(book_data: dict[str, Any], repo: BookRepository = Depends(get_book_repo) ) -> BookResponse :
    result = await repo.add(BookType.from_dict(book_data))
    return BookResponse(**result)

# GET /books/: View all books.
@router.get("/")
async def get_books(repo: BookRepository = Depends(get_book_repo)) -> list[BookResponse]:
    books = await repo.list()
    return [BookResponse(**book) for book in books]

# GET /books/{book_id}: View a specific book by ID.
@router.get("/{book_id}")
async def book_by_id(book_id: uuid.UUID, repo: BookRepository = Depends(get_book_repo)) -> BookResponse:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with this Id {book_id} not Found")
    return BookResponse(**book)

# PUT /books/{book_id}: Update book details.
@router.put('/{book_id}')
async def book_update(book_id: uuid.UUID, book_data: dict[str, Any], repo: BookRepository = Depends(get_book_repo)) -> BookResponse:
    book_data['book_id'] = book_id
    book = await repo.update(book_data)
    if book is None:
        raise HTTPException(status_code=404, detail=f"No book found with this Id: {book_id}")
    return BookResponse(**book)

# DELETE /books/{book_id}: Delete a book.
@router.delete("/{book_id}")
async def book_delete(book_id: uuid.UUID, repo: BookRepository = Depends(get_book_repo)) -> uuid.UUID:
    result = await repo.delete(book_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No book found with this Id: {book_id}")
    return result
