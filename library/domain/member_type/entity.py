from dataclasses import dataclass, fields
from uuid import UUID
from typing import Any, Type, TypeVar

from pydantic import EmailStr

T = TypeVar("T", bound="MemberType")
@dataclass
class MemberType:
    """
    Represents a member entity with a unique ID, email, and name.
    """
    member_id: UUID
    email: EmailStr
    name: str

    @classmethod
    def from_dict(cls: Type[T],data: dict[str,Any]) -> T:
        """
        Convert a dictionary to an instance of the class.
        """
        return cls(
            member_id = UUID(data["member_id"]) if "member_id" in data and data["member_id"] is not None else None,
            name=data["name"],
            email=data["email"],
        )
    # def to_dict(self, exclude: list[str] | None = None) -> dict[str, Any]:
    #     """
    #     Convert the current object to a dictionary.
    #     """
    #     excluded_fields = list(self.config.to_dict_excluded_fields)
    #     if exclude:
    #         excluded_fields += exclude
    #     data: dict[str, Any] = {}
    #     for field in fields(self):
    #         if field.name not in excluded_fields:
    #             value = getattr(self, field.name, None)
    #             if field.name == "book_id" and value:
    #                 value = str(value)
    #             elif field.name == "borrowed_date" and value:
    #                 value = value.isoformat()
    #             data[field.name] = value
    #     return data
    def to_dict(self, exclude: list[str] | None = None) -> dict[str, Any]:
        """
        Convert the current object to a dictionary.
        """
        excluded_fields = self.config.to_dict_excluded_fields
        if exclude:
            excluded_fields += exclude
        data: dict[str, Any] = {}
        for field in fields(self):
            if field not in excluded_fields:
                value = getattr(self, field.name, None)
                if field.name == "member_id" and value:
                    value = str(value)
                elif field.name == "member_id":
                    continue
                data[field.name] =value
        return data
    class config():
        db_excluded_fields: list[str] = ['member_id']
        to_dict_excluded_fields: list[str] = []
        from_dict_excluded_fields: list[str] = []