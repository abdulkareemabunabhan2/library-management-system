from abc import ABC
from typing import Any, Generic, Type, TypeVar
from uuid import UUID

from sqlalchemy import Table, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection

from library.domain.shared.base_entity import BaseEntity
from library.infrastructure.repositories.shared.exceptions import DatabaseError

T = TypeVar('T', bound=BaseEntity)


class BaseRepository(ABC, Generic[T]):
    def __init__(self, connection: AsyncConnection, model_cls: Type[T], table: Table):
        self.connection = connection
        self.table = table
        self.model_cls = model_cls

    async def add(self, entity: T) -> T:
        data = entity.to_dict(entity.config.db_excluded_fields + ['id', 'created_at'])

        command = insert(self.table).values(data).returning(*self.table.columns)
        result = await self.connection.execute(command)
        row = result.first()
        if not row:
            raise DatabaseError('Failed to create row',
                                {'model_cls': self.model_cls.__name__, 'table': self.table.name})
        return self.model_cls.from_dict(dict(row._mapping))

    async def get_by_id(self, id: UUID) -> T | None:
        command = select(self.table).where(self.table.c.id == id)
        result = await self.connection.execute(command)
        row = result.first()
        return self.model_cls.from_dict(dict(row._mapping)) if row else None

    async def get_all(self) -> list[T]:
        command = select(self.table)
        result = await self.connection.execute(command)
        return [self.model_cls.from_dict(dict(row._mapping)) for row in result.all()]

    async def update(self, id: UUID, data: dict[str, Any]) -> T:
        invalid_keys = [k for k in data if k not in self.table.c
                        and k not in self.model_cls.config.db_excluded_fields]

        if invalid_keys:
            raise DatabaseError(
                f"Invalid column(s) in data: {', '.join(invalid_keys)}",
                {'model_cls': self.model_cls.__name__, 'table': self.table.name, 'invalid_columns': invalid_keys}
            )
        update_data = {k: v for k, v in data.items() if k not in self.model_cls.config.db_excluded_fields}
        command = update(self.table).where(self.table.c.id == id).values(**update_data).returning(*self.table.columns)
        result = await self.connection.execute(command)
        row = result.first()
        if not row:
            raise DatabaseError('Failed to update row',
                                {'model_cls': self.model_cls.__name__, 'table': self.table.name, 'id': str(id)})
        return self.model_cls.from_dict(dict(row._mapping))

    async def delete(self, id: UUID) -> T:
        command = delete(self.table).where(self.table.c.id == id).returning(*self.table.c)
        result = await self.connection.execute(command)
        row = result.first()
        if not row:
            raise DatabaseError('Failed to delete row',
                                {'model_cls': self.model_cls.__name__, 'table': self.table.name})
        return self.model_cls.from_dict(dict(row._mapping))
