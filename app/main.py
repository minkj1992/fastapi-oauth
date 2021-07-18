from fastapi import FastAPI
from passlib.context import CryptContext
from starlette.middleware.cors import CORSMiddleware

from app.api.v1_api import router as v1_router
from app.db import database, engine, metadata

metadata.create_all(engine)
app = FastAPI(title='oauth-demo')
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)
app.include_router(v1_router)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # noqa


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
