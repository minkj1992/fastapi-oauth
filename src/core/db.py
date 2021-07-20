from typing import Generator

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

_DATABASE_URL = "sqlite:///./test.db"
metadata = sqlalchemy.MetaData()
users = sqlalchemy.Table(
        "users",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("username", sqlalchemy.String),
        sqlalchemy.Column("hashed_password", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database_session() -> Generator[Session, None, None]:
    """ sqlalchemy Session generator """
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
