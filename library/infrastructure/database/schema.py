import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table

from library.infrastructure.database.db import metadata


Book = Table(
    'book',
    metadata,
    Column('book_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('title', String, nullable=False),
    Column('author', String, nullable=False),
    Column('is_borrowed',Boolean, default=False),
    Column('borrowed_date',DateTime(timezone=True), nullable=True),
    Column('borrowed_by',UUID(as_uuid=True), ForeignKey('member.member_id'), nullable=True),
)

Member = Table(
    'member',
    metadata,
    Column('member_id',UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('name', String, nullable=False),
    Column('email', String, nullable=False),
)
