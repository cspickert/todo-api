from pydantic import BaseModel


class TodoBaseModel(BaseModel):
    id: int


class Task(TodoBaseModel):
    list_id: int
    task: str


class List(TodoBaseModel):
    name: str
