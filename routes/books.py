import uuid
from typing import Type

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Book, BookBase, BookResponse

router = APIRouter()

# Book Endpoints:
# POST /books/: Add a new book.
@router.post("/")
async def add_book(book_data: BookBase, session: Session = Depends(get_session)) -> BookResponse :
    book = Book(title=book_data.title, author=book_data.author)
    session.add(book)
    session.commit()
    session.refresh(book)
    return BookResponse(**book.model_dump())

# GET /books/: View all books.
@router.get("/")
async def get_books(session: Session = Depends(get_session)) -> list[Book]:
    books = session.exec(select(Book)).all()
    return list(books)

# GET /books/{book_id}: View a specific book by ID.
@router.get("/{book_id}")
async def book_by_id(book_id: uuid.UUID, session: Session = Depends(get_session)) -> Book:
    print("who are you?")
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with this Id {book_id} not Found")
    return book

# PUT /books/{book_id}: Update book details.
@router.put('/{book_id}')
async def book_update(book_id: uuid.UUID, book_data: BookBase, session: Session = Depends(get_session)) -> Book:
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"No book found with this Id: {book_id}")
    book.title = book_data.title
    book.author = book_data.author
    session.commit()
    session.refresh(book)
    return book

# DELETE /books/{book_id}: Delete a book.
@router.delete("/{book_id}")
async def book_delete(book_id: uuid.UUID, session: Session = Depends(get_session)) -> uuid.UUID:
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"No book found with this Id: {book_id}")
    session.delete(book)
    session.commit()

    deleted_book = session.get(Book, book_id)
    if deleted_book is not None:
        raise HTTPException(status_code=500, detail="Failed to delete the book")
    return book_id
