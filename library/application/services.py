from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, Self

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from library.infrastructure.database.db import async_engine
from library.infrastructure.repositories.book_repository import BookRepository
from library.infrastructure.repositories.member_repository import MemberRepository


class WorkService:
    def __init__(self, engine: AsyncEngine):
        self.engine: AsyncEngine = engine
        self.connection: AsyncConnection

    async def __aenter__(self) -> Self:
        self.connection = await self.engine.connect()
        await self.connection.begin()
        return self

    async def __aexit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[object]) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.connection.close()

    async def commit(self) -> None:
        if self.connection:
            await self.connection.commit()

    async def rollback(self) -> None:
        if self.connection:
            await self.connection.rollback()

    @property
    def book_repo(self) -> BookRepository:
        if not hasattr(self, "_book_repo"):
            self._book_repo = BookRepository(self.connection)
        return self._book_repo

    @property
    def member_repo(self) -> MemberRepository:
        if not hasattr(self, "_member_repo"):
            self._member_repo = MemberRepository(self.connection)
        return self._member_repo


@asynccontextmanager
async def get_work_service() -> AsyncGenerator[WorkService, None]:
    async with WorkService(async_engine) as work_service:
        yield work_service
