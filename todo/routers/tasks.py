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
    status_code=status.HTTP_201_CREATED,
    description="Create a task.",
)
async def create_task(
    task: TodoTaskCreate,
    user: models.User = Depends(fetch_user),
):
    task_attrs = task.model_dump()
    task_attrs["todo_list_id"] = task_attrs.pop("list_id")
    todo_list = await fetch_list(list_id=task.list_id, user=user)
    task = await todo_list.tasks.acreate(**task_attrs)
    return TodoTask.model_validate(task)


@router.get(
    "",
    response_model=ListResponse[TodoTask],
    description="Retrieve tasks.",
)
async def get_tasks(
    user: models.User = Depends(fetch_user), list_id: int | None = None
):
    tasks_queryset = models.TodoTask.objects.filter(todo_list__user=user)
    if list_id is not None:
        tasks_queryset = tasks_queryset.filter(todo_list_id=list_id)
    results = [TodoTask.model_validate(obj) async for obj in tasks_queryset]
    return ListResponse(results=results)


@router.get(
    "/{task_id}",
    response_model=TodoTask,
    description="Retrieve a task.",
)
async def get_task(task: models.TodoTask = Depends(fetch_task)):
    return TodoTask.model_validate(task)


@router.patch(
    "/{task_id}",
    response_model=TodoTask,
    description="Update a task.",
)
async def update_task(
    task_update_attrs: TodoTaskUpdate,
    task: models.TodoTask = Depends(fetch_task),
):
    stored_attrs = TodoTaskUpdate.model_validate(task, from_attributes=True)
    updated_attrs = stored_attrs.model_copy(
        update=task_update_attrs.model_dump(exclude_unset=True)
    )
    for attr, value in updated_attrs.model_dump(
        exclude_unset=True,
        exclude={"completed"},
    ).items():
        if getattr(task, attr) != value:
            setattr(task, attr, value)
    await task.asave()
    return TodoTask.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a task.",
)
async def delete_task(
    task: models.TodoTask = Depends(fetch_task),
):
    await task.adelete()
