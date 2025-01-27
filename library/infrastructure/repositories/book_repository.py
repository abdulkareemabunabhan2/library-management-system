from sqlalchemy.ext.asyncio import AsyncConnection

from library.domain.book.entity import BookEntity
from library.infrastructure.database.schema import Book
from library.infrastructure.repositories.base_repository import BaseRepository


class BookRepository(BaseRepository[BookEntity]):
    def __init__(self, connection: AsyncConnection):
        super().__init__(connection, BookEntity, Book)
