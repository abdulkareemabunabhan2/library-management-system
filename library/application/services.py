from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from library.infrastructure.database.db import get_async_session
from library.infrastructure.repositories.books_repository import BookRepository
from library.infrastructure.repositories.member_repository import MemberRepository
from library.application.book_service import BookService
from library.application.member_service import MemberService
router = APIRouter()

# book repo
def get_book_repo(session: AsyncSession = Depends(get_async_session)) -> BookRepository:
    return BookRepository(session)

# member repo
def get_member_repo(session: AsyncSession = Depends(get_async_session)) -> MemberRepository:
    return MemberRepository(session)

# Book service
def get_book_service(
    book_repo: BookRepository = Depends(get_book_repo),
    member_repo: MemberRepository = Depends(get_member_repo),
    session: AsyncSession = Depends(get_async_session),
) -> BookService:
    return BookService(book_repo, member_repo, session)

# Member service
def get_member_service(
    member_repo: MemberRepository = Depends(get_member_repo),
    session: AsyncSession = Depends(get_async_session),
) -> MemberService:
    return MemberService(member_repo, session)
