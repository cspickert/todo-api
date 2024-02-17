from fastapi import Depends, Security, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer

from todo import models

security = HTTPBearer()


def fetch_user(auth: str = Security(security)) -> models.User:
    try:
        return models.User.objects.get(keys__key=auth.credentials)
    except models.Key.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )


def fetch_list(
    list_id: int,
    user: models.User = Depends(fetch_user),
) -> models.TodoList:
    try:
        return user.lists.get(id=list_id)
    except models.TodoList.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found.",
        )


def fetch_task(
    task_id: int,
    user: models.User = Depends(fetch_user),
) -> models.TodoTask:
    try:
        return models.TodoTask.objects.filter(todo_list__user=user).get(id=task_id)
    except models.TodoTask.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
