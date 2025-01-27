from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from library.domain.shared.base_entity import BaseEntity


@dataclass
class BookEntity(BaseEntity):
    title: str
    author: str
    is_borrowed: bool = False
    borrowed_date: datetime | None = None
    borrowed_by: UUID | None = None

    class config:
        db_excluded_fields: list[str] = ['id', 'created_at']
        to_dict_excluded_fields: list[str] = []
        from_dict_excluded_fields: list[str] = []
