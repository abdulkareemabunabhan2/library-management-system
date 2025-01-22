from typing import TypeVar, Generic, Any
from uuid import UUID
from sqlalchemy import select, delete, update, insert
from sqlalchemy.exc import NoResultFound
from sqlmodel.ext.asyncio.session import AsyncSession

from library.infrastructure.database.schema import Book
from library.domain.book_type.entity import BookType

T = TypeVar('T', bound=BookType)

class BookRepository(Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    # add(book)
    async def add(self, entity: BookType) -> dict[str, Any]:
        """
        Add a new book to the database and return the inserted book data.
        """
        data = entity.to_dict(entity.config.db_excluded_fields + ["borrowed_date"])
        command = insert(Book).values(data)
        result = await self.session.execute(command)
        await self.session.commit()

        book_id = result.inserted_primary_key[0]
        inserted_book = await self.session.execute(
            select(Book).where(Book.c.book_id == book_id)
        )
        book_dict = inserted_book.fetchone()._asdict() if inserted_book else {}
        return book_dict

    # get(book_id)
    async def get(self, book_id: UUID) -> dict[str, Any] | None:
        """
        Get book by id from the database
        """
        command = select(Book).where(Book.c.book_id == book_id)
        result = await self.session.execute(command)
        raw = result.fetchone()
        if not raw:
            return None
        return raw._asdict()

    # list()
    async def list(self) -> list[dict[str, Any]]:
        """
        List all books from database.
        """
        command = select(Book)
        result = await self.session.execute(command)
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]

    # delete(book_id)
    async def delete(self, book_id: UUID) -> UUID | None:
        """
        Delete from database.
        """
        command = delete(Book).where(Book.c.book_id == book_id)
        result = await self.session.execute(command)
        await self.session.commit()
        if result.rowcount == 0:
            return None
        return book_id

    # update(book)
    async def update(self, data: dict[str, Any]) -> dict[str, Any]:
        if 'book_id' not in data:
            raise KeyError("The 'book_id' field is required to update a book.")

        update_data = {k: v for k, v in data.items() if k not in BookType.config.db_excluded_fields}
        command = (
            update(Book)
            .where(Book.c.book_id == data['book_id'])
            .values(**update_data)
            .returning(*Book.c)
        )
        result = await self.session.execute(command)
        book = result.fetchone()
        if not book:
            return None
        await self.session.commit()
        return book._asdict()
