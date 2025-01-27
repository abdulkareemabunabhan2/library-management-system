from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID

from library.infrastructure.database.db import metadata

Book = Table(
    'book',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column('title', String, nullable=False),
    Column('author', String, nullable=False),
    Column('is_borrowed', Boolean, default=False),
    Column('borrowed_date', DateTime(timezone=True), nullable=True),
    Column('borrowed_by', UUID(as_uuid=True), ForeignKey('member.id'), nullable=True),
    Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
    Column('updated_at', DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc)),
)

Member = Table(
    'member',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column('name', String, nullable=False),
    Column('email', String, nullable=False),
    Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
    Column('updated_at', DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc))
)
