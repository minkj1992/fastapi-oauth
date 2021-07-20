from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.apps.api.v1_api import router as v1_router
from src.core.db import metadata, engine
from src.core.fastapi import create_app

metadata.create_all(bind=engine)
app = create_app()
app.include_router(v1_router)
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="temporary_secret")

app.openapi_schema = get_openapi(
    title=f"oauth API",
    version='0.0.0',
    description=(
        "tidify</br>"
        "<hr>"
        "<h3>개발자</h3>"
        "<p>[제민욱](https://github.com/minkj1992)</p>"
    ),
    routes=app.routes,
)

print([r.__dict__ for r in app.routes])
