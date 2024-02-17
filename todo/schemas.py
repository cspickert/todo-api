from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


class Base(_BaseModel):
    pass


class TodoList(Base):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class TodoListWritable(Base):
    name: str


class TodoTask(Base):
    id: int
    task: str
    model_config = ConfigDict(from_attributes=True)


class ListResponse[_T: Base](_BaseModel):
    results: list[_T]
