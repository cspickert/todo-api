import pytest
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient

from todo.models import User


@pytest.fixture(autouse=True)
def allow_db_access(transactional_db):
    # Global replacement for `pytest.mark.django_db`
    pass


@pytest.fixture
def make_user():
    def fn(**kwargs):
        return User.objects.create(**kwargs)

    return fn


@pytest.fixture
def user(make_user):
    return make_user(username="test user")


@pytest.fixture
def other_user(make_user):
    return make_user(username="other test user")


@pytest.fixture
def make_key():
    def fn(user, **kwargs):
        return user.keys.create(**kwargs)

    return fn


@pytest.fixture
def key(make_key, user):
    return make_key(user=user)


@pytest.fixture
def other_key(make_key, other_user):
    return make_key(user=other_user)


@pytest.fixture
def auth(key):
    return HTTPAuthorizationCredentials(scheme="test", credentials=key.key)


@pytest.fixture
def todo_list(user):
    return user.lists.create(name="test list")


@pytest.fixture
def task(todo_list):
    return todo_list.tasks.create(task="test task")


@pytest.fixture
def make_client():
    from asgi import app

    def fn(key=None):
        kwargs = {}
        if key is not None:
            kwargs["headers"] = {"Authorization": f"Bearer {key.key}"}
        return TestClient(app, **kwargs)

    return fn


@pytest.fixture
def anon_client(make_client):
    return make_client()


@pytest.fixture
def client(make_client, key):
    return make_client(key=key)


@pytest.fixture
def other_client(make_client, other_key):
    return make_client(key=other_key)
