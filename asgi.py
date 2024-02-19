import os

import django
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo.settings")
django.setup()


app = FastAPI(
    title="Todo API",
    description="A simple to-do list API.",
    version="0.1.0",
)


def init(app: FastAPI):
    from todo.routers import register_routers

    register_routers(app)


init(app)

__all__ = ["app"]
