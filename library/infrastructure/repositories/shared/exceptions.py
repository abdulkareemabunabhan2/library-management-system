from typing import Any


class DatabaseError(Exception):
    """Base exceptions for infrastructure-related errors."""

    def __init__(self, message: str, data: dict[str, Any] | None = None) -> None:
        self.message = message
        self.data = data
