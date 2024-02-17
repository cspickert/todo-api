from fastapi import Depends, status
from fastapi.routing import APIRouter

from todo import models
from todo.queries import fetch_list, fetch_task, fetch_user
from todo.schemas import ListResponse, TodoTask, TodoTaskCreate, TodoTaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


# Tasks


@router.post(
    "",
    response_model=TodoTask,
)
def create_task(
    task: TodoTaskCreate,
    user: models.User = Depends(fetch_user),
):
    task_attrs = task.model_dump()
    task_attrs["todo_list_id"] = task_attrs.pop("list_id")
    todo_list = fetch_list(list_id=task.list_id, user=user)
    task = todo_list.tasks.create(**task_attrs)
    return TodoTask.model_validate(task)


@router.get(
    "",
    response_model=ListResponse[TodoTask],
)
def get_tasks(user: models.User = Depends(fetch_user), list_id: int | None = None):
    tasks_queryset = models.TodoTask.objects.filter(todo_list__user=user)
    if list_id is not None:
        tasks_queryset = tasks_queryset.filter(todo_list_id=list_id)
    results = [TodoTask.model_validate(obj) for obj in tasks_queryset]
    return ListResponse(results=results)


@router.get(
    "/{task_id}",
    response_model=TodoTask,
)
def get_task(task: models.TodoTask = Depends(fetch_task)):
    return TodoTask.model_validate(task)


@router.patch(
    "/{task_id}",
    response_model=TodoTask,
)
def update_task(
    task_attrs: TodoTaskUpdate,
    task: models.TodoTask = Depends(fetch_task),
):
    for attr, value in task_attrs.model_dump(exclude_unset=True).items():
        setattr(task, attr, value)
    task.save()
    return TodoTask.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task: models.TodoTask = Depends(fetch_task),
):
    task.delete()
