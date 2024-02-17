from fastapi import FastAPI

from .lists import router as lists_router
from .tasks import router as tasks_router


def register_routers(app: FastAPI):
    app.include_router(lists_router)
    app.include_router(tasks_router)


__all__ = ["register_routers"]
