from dataclasses import dataclass, fields
from datetime import datetime
from typing import Any, Type, TypeVar
from uuid import UUID

T = TypeVar('T', bound='BaseEntity')


def get_field_value(field_type: type[Any] | str | Any, filed_data: Any) -> Any:
    if filed_data is None:
        return None
    if isinstance(field_type, type) and issubclass(field_type, BaseEntity):
        return field_type.from_dict(filed_data)

    origin = getattr(field_type, "__origin__", None)
    if origin is list and isinstance(filed_data, list):
        args = getattr(field_type, "__args__", [])
        if args and isinstance(args[0], type) and issubclass(args[0], BaseEntity):
            return [args[0].from_dict(item) for item in filed_data]

    return filed_data


@dataclass
class BaseEntity:
    id: UUID
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls: Type[T], data: dict[str, Any], exclude: list[str] | None = None) -> T:
        """
        Convert the current object to a dictionary and handle nested dataclasses.
        Recursively converts all nested dataclasses to dictionaries.
        """
        excluded_fields = cls.config.from_dict_excluded_fields
        if exclude:
            excluded_fields = excluded_fields + exclude

        instance_data = {}
        entity_fields = {f.name: f.type for f in fields(cls)}
        for field_name, field_type in entity_fields.items():
            field_data = None
            if field_name not in excluded_fields:
                field_data = data.get(field_name, None)
            instance_data[field_name] = get_field_value(field_type, field_data)
        return cls(**instance_data)

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
                if field.name == 'id' and value:
                    value = str(value)
                elif field.type == 'datetime.datetime' and value:
                    value = value.isoformat()
                data[field.name] = value
        return data

    class config:
        db_excluded_fields: list[str] = []
        to_dict_excluded_fields: list[str] = []
        from_dict_excluded_fields: list[str] = []
