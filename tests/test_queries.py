import pytest
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from todo.models import User
from todo.queries import fetch_list, fetch_task, fetch_user


def test_fetch_user(auth, user):
    assert fetch_user(auth) == user


def test_fetch_user_invalid_auth():
    with pytest.raises(HTTPException, match=r"Invalid or missing API key.") as exc:
        auth = HTTPAuthorizationCredentials(scheme="test", credentials="bad key value")
        fetch_user(auth)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_fetch_list(todo_list, user):
    assert fetch_list(todo_list.id, user) == todo_list


def test_fetch_list_nonexistent(user):
    with pytest.raises(HTTPException, match=r"List not found.") as exc:
        fetch_list(8675309, user)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


def test_fetch_list_user_mismatch(todo_list):
    other_user = User.objects.create(username="other_user")
    with pytest.raises(HTTPException, match=r"List not found.") as exc:
        fetch_list(todo_list.id, other_user)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


def test_fetch_task(task, user):
    assert fetch_task(task.id, user) == task


def test_fetch_task_nonexistent(user):
    with pytest.raises(HTTPException, match=r"Task not found.") as exc:
        fetch_task(8675309, user)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


def test_fetch_task_user_mismatch(task):
    other_user = User.objects.create(username="other_user")
    with pytest.raises(HTTPException, match=r"Task not found.") as exc:
        fetch_task(task.id, other_user)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
