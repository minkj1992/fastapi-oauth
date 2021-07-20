from fastapi import FastAPI


def create_app() -> FastAPI:
    """ app factory method """
    _app = FastAPI()
    return _app
