from dataclasses import dataclass, fields
from datetime import datetime
from uuid import UUID
from typing import Any, Type, TypeVar


T = TypeVar("T", bound="BookType")
@dataclass
class BookType:
    book_id: UUID
    title: str
    author: str
    is_borrowed: bool = False
    borrowed_date: datetime | None = None
    borrowed_by: UUID | None = None

    @classmethod
    def from_dict(cls: Type[T],data: dict[str,Any]) -> T:
        """
        Convert a dictionary to an instance of the class.
        """
        return cls(
            book_id = UUID(data["book_id"]) if "book_id" in data and data["book_id"] is not None else None,
            title=data["title"],
            author=data["author"],
            borrowed_date=datetime.fromisoformat(data["borrowed_date"]) if "borrowed_date" in data else None,
            borrowed_by=UUID(data["borrowed_by"]) if "borrowed_by" in data and data["borrowed_by"] is not None else None
        )
    def to_dict(self, exclude: list[str] | None = None) -> dict[str, Any]:
        """
        Convert the current object to a dictionary.
        """
        excluded_fields = list(self.config.to_dict_excluded_fields)
        if exclude:
            excluded_fields += exclude
        data: dict[str, Any] = {}
        for field in fields(self):
            if field.name not in excluded_fields:
                value = getattr(self, field.name, None)
                if field.name == "book_id" and value:
                    value = str(value)
                elif field.name == "borrowed_date" and value:
                    value = value.isoformat()
                data[field.name] = value
        return data

    class config():
        db_excluded_fields: list[str] = ['book_id']
        to_dict_excluded_fields: list[str] = []
        from_dict_excluded_fields: list[str] = []