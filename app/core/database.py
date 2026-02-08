from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import config_manager
from app.utils.log import logger

mariadb_host = config_manager.get().MARIADB_HOST
mariadb_port = config_manager.get().MARIADB_PORT
mariadb_user = config_manager.get().MARIADB_USER
mariadb_password = config_manager.get().MARIADB_PASSWORD
mariadb_database = config_manager.get().MARIADB_DB


database_url = config_manager.get().DATABASE_URL or f"mysql+pymysql://{mariadb_user}:{mariadb_password}@{mariadb_host}:{mariadb_port}/{mariadb_database}?charset=utf8mb4"
engine = create_engine(database_url)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)
Base = declarative_base()


@contextmanager
def session_scope() -> Generator:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        logger.error(f"数据库操作失败：{str(e)}")
        raise
    finally:
        if session.is_active:
            session.expunge_all()
            session.close()


def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        logger.error(f"数据库操作失败：{str(e)}")
        raise
    finally:
        if session.is_active:
            session.expunge_all()
            session.close()
