from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from library.configs import env


# Helper functions to construct database URLs
def get_db_url() -> str:
    return 'postgresql+asyncpg://%s:%s@%s:%s/%s' % (
    env.POSTGRES_USER, env.POSTGRES_PASSWORD, env.DB_HOST, env.POSTGRES_PORT, env.POSTGRES_DB)


def get_db_sync_url() -> str:
    return 'postgresql://%s:%s@%s:%s/%s' % (
    env.POSTGRES_USER, env.POSTGRES_PASSWORD, env.DB_HOST, env.POSTGRES_PORT, env.POSTGRES_DB)


async_engine = create_async_engine(get_db_url(), echo=True)
sync_engine = create_engine(get_db_sync_url(), echo=True)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)


metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Dependency to provide async session
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session









# import os
# from dotenv import load_dotenv
# from sqlmodel import create_engine, SQLModel, Session
# load_dotenv()
#
# DATABASE_URL = os.getenv("DATABASE_URL")
# print(DATABASE_URL)
# engine = create_engine(DATABASE_URL, echo=True)
# print(engine)
# def init_db():
#     SQLModel.metadata.create_all(engine)
#
# def get_session():
#     with Session(engine) as session:
#         yield session
#
# print(get_session())