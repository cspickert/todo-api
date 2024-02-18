from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field


class Base(_BaseModel):
    pass


class TodoList(Base):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class TodoListUpdate(Base):
    name: str


class TodoListCreate(TodoListUpdate):
    pass


class TodoTask(Base):
    id: int
    todo_list_id: int = Field(alias="list_id")
    task: str
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TodoTaskUpdate(Base):
    task: str


class TodoTaskCreate(TodoTaskUpdate):
    list_id: int


class ListResponse[_T: Base](_BaseModel):
    results: list[_T]
