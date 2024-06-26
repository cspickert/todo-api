from fastapi import Depends, status
from fastapi.routing import APIRouter

from todo import models
from todo.queries import fetch_list, fetch_user
from todo.schemas import ListResponse, TodoList, TodoListCreate, TodoListUpdate

router = APIRouter(prefix="/lists", tags=["lists"])


# Lists


@router.post(
    "",
    response_model=TodoList,
    status_code=status.HTTP_201_CREATED,
    description="Create a list.",
)
async def create_list(
    todo_list: TodoListCreate,
    user: models.User = Depends(fetch_user),
):
    list_attrs = todo_list.model_dump()
    todo_list = await user.lists.acreate(**list_attrs)
    return TodoList.model_validate(todo_list)


@router.get(
    "",
    response_model=ListResponse[TodoList],
    description="Retrieve lists.",
)
async def get_lists(
    user: models.User = Depends(fetch_user),
):
    results = [TodoList.model_validate(obj) async for obj in user.lists.all()]
    return ListResponse(results=results)


@router.get(
    "/{list_id}",
    response_model=TodoList,
    description="Retrieve a list.",
)
async def get_list(
    todo_list: models.TodoList = Depends(fetch_list),
):
    return TodoList.model_validate(todo_list)


@router.patch(
    "/{list_id}",
    response_model=TodoList,
    description="Update a list.",
)
async def update_list(
    list_attrs: TodoListUpdate,
    todo_list: models.TodoList = Depends(fetch_list),
):
    for attr, value in list_attrs.model_dump(exclude_unset=True).items():
        setattr(todo_list, attr, value)
    await todo_list.asave()
    return TodoList.model_validate(todo_list)


@router.delete(
    "/{list_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a list.",
)
async def delete_list(
    todo_list: models.TodoList = Depends(fetch_list),
):
    await todo_list.adelete()
