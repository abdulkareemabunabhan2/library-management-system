from dataclasses import dataclass

from pydantic import EmailStr

from library.domain.shared.base_entity import BaseEntity


@dataclass
class MemberEntity(BaseEntity):
    """
    Represents a member entity with a unique ID, email, and name.
    """
    email: EmailStr
    name: str

    class config:
        db_excluded_fields: list[str] = ['id']
        to_dict_excluded_fields: list[str] = []
        from_dict_excluded_fields: list[str] = []
