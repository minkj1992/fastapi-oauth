from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.core.db import metadata, engine
from src.core.fastapi import create_app

metadata.create_all(bind=engine)
app = create_app()


@app.exception_handler(AuthError)
async def handle_auth_error(request: Request, ex: AuthError):
    return JSONResponse(status_code=ex.status_code, content=ex.error)


@app.get("/private")
async def private(user=Security(get_current_user)):
    return user


@app.get("/private-with-scopes")
async def privateScopes(user=Security(get_current_user, scopes=["openid"])):
    return {"message": "You're authorized with scopes!"}


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
