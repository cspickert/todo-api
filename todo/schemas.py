from datetime import datetime

from django.utils import timezone
from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field, model_validator


class Base(_BaseModel):
    """Abstract base schema."""


class TodoList(Base):
    """Primary todo list API representation."""

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class TodoListUpdate(Base):
    """Valid attributes for partial updates to todo lists."""

    name: str


class TodoListCreate(Base):
    """Valid attributes for creating todo lists."""

    name: str


class TodoTask(Base):
    """Primary todo list task API representation."""

    id: int
    todo_list_id: int = Field(alias="list_id")
    task: str
    completed: bool

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TodoTaskUpdate(Base):
    """Valid attributes for partial updates to todo list tasks."""

    task: str = ""
    completed: bool = False


class TodoTaskCreate(Base):
    """Valid attributes for creating todo list tasks."""

    task: str
    list_id: int


class ListResponse[_T: Base](_BaseModel):
    """Response schema for list endpoints.

    Note: this would be more useful with additional metadata, like next/prev
    links for paginated responses."""

    results: list[_T]
