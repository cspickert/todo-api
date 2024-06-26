from fastapi import Depends, Security, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from todo import models

security = HTTPBearer()


async def fetch_user(
    auth: HTTPAuthorizationCredentials = Security(security),
) -> models.User:
    """Fetches the user associated with the provided API key.

    Raises an HTTP exception if the API key is invalid."""

    try:
        return await models.User.objects.aget(keys__key=auth.credentials)
    except models.User.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )


async def fetch_list(
    list_id: int,
    user: models.User = Depends(fetch_user),
) -> models.TodoList:
    """Fetches the todo list with the provided ID.

    Raises an HTTP 404 exception if the list does not exist for the current
    user."""

    try:
        return await user.lists.aget(id=list_id)
    except models.TodoList.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found.",
        )


async def fetch_task(
    task_id: int,
    user: models.User = Depends(fetch_user),
) -> models.TodoTask:
    """Fetches the todo task with the provided ID.

    Raises an HTTP 404 exception if the task does not exist for the current
    user."""

    try:
        return await models.TodoTask.objects.filter(todo_list__user=user).aget(
            id=task_id
        )
    except models.TodoTask.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
