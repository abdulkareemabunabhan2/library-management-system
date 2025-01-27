from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from library.application.services import get_work_service
from library.application.shared.exceptions import DataNotFoundException
from library.domain.book.entity import BookEntity


class BookService:
    async def add(self, data: dict[str, Any]) -> BookEntity:
        book_entity = BookEntity.from_dict(data)
        async with get_work_service() as work_service:
            return await work_service.book_repo.add(book_entity)

    async def update(self, id: UUID, data: dict[str, Any]) -> BookEntity:
        async with get_work_service() as work_service:
            if not await work_service.book_repo.get_by_id(id):
                raise DataNotFoundException(f'Book with ID {id} not found.')
            return await work_service.book_repo.update(id, data)

    async def list(self) -> list[BookEntity]:
        async with get_work_service() as work_service:
            return await work_service.book_repo.get_all()

    async def get_by_id(self, id: UUID) -> BookEntity:
        async with get_work_service() as work_service:
            if not (book := await work_service.book_repo.get_by_id(id)):
                raise DataNotFoundException(f'Book with ID {id} not found.')
            return book

    async def delete(self, id: UUID) -> BookEntity:
        async with get_work_service() as work_service:
            if not await work_service.book_repo.get_by_id(id):
                raise DataNotFoundException(f'Book with ID {id} not found.')
            return await work_service.book_repo.delete(id)

    async def borrow_book(self, book_id: UUID, member_id: UUID) -> BookEntity:
        async with get_work_service() as work_service:
            book = await work_service.book_repo.get_by_id(book_id)
            if not book:
                raise DataNotFoundException(f'Book with ID {book_id} not found.')
            book_data = book.to_dict()
            if book_data['is_borrowed']:
                raise ValueError(f'Book with ID {book_id} is already borrowed.')

            member = await work_service.member_repo.get_by_id(member_id)
            if not member:
                raise DataNotFoundException(f'Member with ID {member_id} not found.')

            book_data['is_borrowed'] = True
            book_data['borrowed_by'] = member_id
            book_data['borrowed_date'] = datetime.now(timezone.utc)
            result = await work_service.book_repo.update(book_id, book_data)
            return result

    async def return_book(self, book_id: UUID) -> BookEntity:
        async with get_work_service() as work_service:
            book = await work_service.book_repo.get_by_id(book_id)
            if not book:
                raise DataNotFoundException(f'Book with ID {book_id} not found.')
            book_data = book.to_dict()
            if not book_data['is_borrowed']:
                raise ValueError(f'Book with ID {book_id} is not borrowed.')

            book_data['is_borrowed'] = False
            book_data['borrowed_by'] = None
            book_data['borrowed_date'] = None
            result = await work_service.book_repo.update(book_id, book_data)
            return result
