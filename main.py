from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer

from todo.models import TodoList, TodoTask

# Init app
app = FastAPI()

security = HTTPBearer()


# Lists


@app.get("/lists")
def get_lists(credentials: Annotated[str, Depends(security)]):
    return []


# @app.post("/lists")
# def create_list(list):
#     raise NotImplementedError


# @app.get("/lists/{list_id}")
# def get_list(list_id: int):
#     raise NotImplementedError


# @app.put("/lists/{list_id}")
# def update_list(list_id: int, list: List):
#     raise NotImplementedError


# @app.delete("/lists/{list_id}")
# def delete_list(list_id: int):
#     raise NotImplementedError


# # Tasks


# @app.get("/tasks")
# def get_tasks(list_id: int):
#     return []


# @app.post("/tasks")
# def create_task(list_id: int, task: Task):
#     raise NotImplementedError


# @app.get("/tasks/{task_id}")
# def get_task(task_id: int):
#     raise NotImplementedError


# @app.put("/tasks/{task_id}")
# def update_task(task_id: int, task: Task):
#     raise NotImplementedError


# @app.delete("/tasks/{task_id}")
# def delete_task(task_id: int):
#     raise NotImplementedError
