import pytest
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from todo.models import User
from todo.queries import fetch_list, fetch_task, fetch_user


@pytest.mark.asyncio
class TestQueries:
    async def test_fetch_user(self, auth, user):
        assert await fetch_user(auth) == user

    async def test_fetch_user_invalid_auth(self):
        with pytest.raises(HTTPException, match=r"Invalid or missing API key.") as exc:
            auth = HTTPAuthorizationCredentials(
                scheme="test", credentials="bad key value"
            )
            await fetch_user(auth)
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_fetch_list(self, todo_list, user):
        assert await fetch_list(todo_list.id, user) == todo_list

    async def test_fetch_list_nonexistent(self, user):
        with pytest.raises(HTTPException, match=r"List not found.") as exc:
            await fetch_list(8675309, user)
        assert exc.value.status_code == status.HTTP_404_NOT_FOUND

    async def test_fetch_list_user_mismatch(self, todo_list):
        other_user = await User.objects.acreate(username="other_user")
        with pytest.raises(HTTPException, match=r"List not found.") as exc:
            await fetch_list(todo_list.id, other_user)
        assert exc.value.status_code == status.HTTP_404_NOT_FOUND

    async def test_fetch_task(self, task, user):
        assert await fetch_task(task.id, user) == task

    async def test_fetch_task_nonexistent(self, user):
        with pytest.raises(HTTPException, match=r"Task not found.") as exc:
            await fetch_task(8675309, user)
        assert exc.value.status_code == status.HTTP_404_NOT_FOUND

    async def test_fetch_task_user_mismatch(self, task):
        other_user = await User.objects.acreate(username="other_user")
        with pytest.raises(HTTPException, match=r"Task not found.") as exc:
            await fetch_task(task.id, other_user)
        assert exc.value.status_code == status.HTTP_404_NOT_FOUND
