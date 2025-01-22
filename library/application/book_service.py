from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from library.domain.book_type.entity import BookType
from library.infrastructure.repositories.books_repository import BookRepository
from library.infrastructure.repositories.member_repository import MemberRepository
from datetime import datetime, timezone
class BookService:
    def __init__(self, book_repo: BookRepository, member_repo: MemberRepository, session: AsyncSession):
        self.book_repo = book_repo
        self.member_repo = member_repo
        self.session = session

    async def borrow_book(self, book_id: UUID, member_id: UUID) -> dict[str, Any]:
        """
        This method allow the member to borrow a book if is it not already borrowed
        """
        book = await self.book_repo.get(book_id)
        if not book:
            raise Exception(f"Book with ID {book_id} not found.")
        if book["borrowed_by"]:
            raise Exception(f"Book with ID {book_id} is already borrowed.")

        member = await self.member_repo.get(member_id)
        if not member:
            raise Exception(f"Member with ID {member_id} not found.")

        book["is_borrowed"] = True
        book["borrowed_by"] = member_id
        book["borrowed_date"] = datetime.now(timezone.utc)
        await self.book_repo.update(book)
        return book

    async def return_book(self, book_id: UUID) -> dict[str, Any] | None:
        """
        This method allows the user to return a book.
        """
        book = await self.book_repo.get(book_id)
        if not book:
            return None
        if not book["is_borrowed"]:
            raise Exception(f"Book with ID {book_id} is not borrowed.")

        book["is_borrowed"] = False
        book["borrowed_by"] = None
        book["borrowed_date"] = None
        await self.book_repo.update(book)
        return book
