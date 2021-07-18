import sqlalchemy
from databases import Database

from fastapi.security import OAuth2PasswordBearer

DATABASE_URL = "sqlite:///./test.db"
metadata = sqlalchemy.MetaData()
users = sqlalchemy.Table(
        "users",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("username", sqlalchemy.String),
        sqlalchemy.Column("hashed_password", sqlalchemy.String),
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
)

database = Database(DATABASE_URL)

