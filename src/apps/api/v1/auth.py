from datetime import timedelta, datetime
from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt  # noqa
from sqlalchemy.orm import Session

from src.core.oauth import oauth2_scheme, pwd_context
from src.core.secrets import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from src.apps.models.token import TokenData
from src.apps.models.user import User, UserRegister, UserDetail
from src.core.db import users, get_database_session

auth_router = APIRouter(prefix="/oauth")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_database_session), ):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_or_none(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_user_or_none(session: Session, username: str):
    query = users.select().where(users.c.username == username)
    data = await session.fetch_one(query)
    if data:
        return User(**data)
    return None


async def authenticate_user(session: Session, username: str, password: str):
    user = await get_user_or_none(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


@auth_router.get("/me", response_model=UserDetail)
async def get_users(current_user: User = Depends(get_current_active_user)):
    user = await current_user
    return {**user.dict()}


@auth_router.post("/register", response_model=User)
async def register(user: UserRegister, session: Session = Depends(get_database_session)):
    query = users.insert().values(username=user.username, hashed_password=get_password_hash(user.hashed_password))
    last_record_id = await session.execute(query)
    return {**user.dict(), "id": last_record_id}


@auth_router.post("/login")
async def login(session: Session = Depends(get_database_session), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "type": "bearer"}
