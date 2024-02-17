from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from todo import models
from todo.schemas import ListResponse, TodoList, TodoListWritable
from todo.security import get_user

router = APIRouter(prefix="/lists", tags=["lists"])


# Lists


@router.post(
    "",
    response_model=TodoList,
)
def create_list(
    list: TodoListWritable,
    user: models.User = Depends(get_user),
):
    todo_list = user.lists.create(name=list.name)
    return TodoList.model_validate(todo_list)


@router.get(
    "",
    response_model=ListResponse[TodoList],
)
def get_lists(user: models.User = Depends(get_user)):
    todo_lists = [TodoList.model_validate(obj) for obj in user.lists.all()]
    return ListResponse(results=todo_lists)


@router.get(
    "/{list_id}",
    response_model=TodoList,
)
def get_list(
    list_id: int,
    user: models.User = Depends(get_user),
):
    try:
        todo_list = user.lists.get(id=list_id)
        return TodoList.model_validate(todo_list)
    except models.TodoList.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found.",
        )


@router.patch(
    "/{list_id}",
    response_model=TodoList,
)
def update_list(
    list_id: int,
    list_attrs: TodoListWritable,
    user: models.User = Depends(get_user),
):
    try:
        todo_list = user.lists.get(id=list_id)
        for attr, value in list_attrs.model_dump(exclude_unset=True).items():
            setattr(todo_list, attr, value)
        todo_list.save()
        return TodoList.model_validate(todo_list)
    except models.TodoList.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found.",
        )


@router.delete(
    "/{list_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_list(
    list_id: int,
    user: models.User = Depends(get_user),
):
    try:
        todo_list = user.lists.get(id=list_id)
        todo_list.delete()
    except models.TodoList.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found.",
        )
