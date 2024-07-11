import os
from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.pool import NullPool
from typing import Iterator

import dotenv

dotenv.load_dotenv()


class ConnectionString(Enum):
    """
    連線資訊
    """
    # official = 'mysql+pymysql://gary:gary1984@10.20.144.3:3306/company?charset=utf8mb4'
    official = os.getenv("DB_CONN")


db_engine = create_engine(ConnectionString.official.value,
                          query_cache_size=50,
                          echo=False,
                          poolclass=NullPool,
                          future=True)


def create_session() -> Iterator[Session]:
    """
    建立sqlalchemy session
    Returns:
    """

    session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine, future=True)
    session = ScopedSession(session)()
    try:
        yield session
    except Exception as ex:
        session.rollback()
        raise ex
    finally:
        session.close()
        db_engine.dispose()


@contextmanager
def use_with_create_session() -> Iterator[Session]:
    return create_session()
