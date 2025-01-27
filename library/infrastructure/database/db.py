from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from library.configs import env


def get_db_url() -> str:
    return 'postgresql+asyncpg://%s:%s@%s:%s/%s' % (env.POSTGRES_USER, env.POSTGRES_PASSWORD,
                                                    env.DB_HOST, env.POSTGRES_PORT, env.POSTGRES_DB)


async_engine = create_async_engine(get_db_url(), echo=True)
metadata = MetaData()
Base = declarative_base(metadata=metadata)
