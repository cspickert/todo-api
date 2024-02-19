import pytest
from django.utils import timezone

from todo.models import TodoTask


@pytest.fixture
def todo_list_1(user):
    return user.lists.create(name="list 1")


@pytest.fixture
def task_1(todo_list_1):
    return todo_list_1.tasks.create(task="task 1")


@pytest.fixture
def todo_list_2(user):
    return user.lists.create(name="list 2")


@pytest.fixture
def task_2(todo_list_2):
    return todo_list_2.tasks.create(task="task 2")


def test_create_task(client, todo_list):
    resp = client.post(
        "/tasks",
        json={"list_id": todo_list.id, "task": "new test task"},
    )
    assert resp.status_code == 201
    task = TodoTask.objects.last()
    assert resp.json() == {
        "id": task.id,
        "list_id": task.todo_list_id,
        "task": "new test task",
        "completed": False,
    }


def test_create_task_missing_fields(client):
    resp = client.post("/tasks", json={})
    assert resp.status_code == 422
    errors = resp.json()["detail"]
    assert len(errors) == 2
    assert set(error["type"] for error in errors) == {"missing"}
    assert set(error["loc"][1] for error in errors) == {"task", "list_id"}


def test_get_tasks(client, task):
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert resp.json() == {
        "results": [
            {
                "id": task.id,
                "list_id": task.todo_list_id,
                "task": task.task,
                "completed": False,
            }
        ]
    }


def test_get_tasks_filter_by_list(client, todo_list_1, todo_list_2, task_1, task_2):
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert [task["id"] for task in resp.json()["results"]] == [task_1.id, task_2.id]

    resp = client.get(f"/tasks?list_id={todo_list_1.id}")
    assert resp.status_code == 200
    assert [task["id"] for task in resp.json()["results"]] == [task_1.id]

    resp = client.get(f"/tasks?list_id={todo_list_2.id}")
    assert resp.status_code == 200
    assert [task["id"] for task in resp.json()["results"]] == [task_2.id]

    resp = client.get("/tasks?list_id=8675309")
    assert resp.status_code == 200
    assert [task["id"] for task in resp.json()["results"]] == []


def test_get_tasks_anon(anon_client):
    resp = anon_client.get("/tasks")
    # TODO: change to 401, see https://github.com/tiangolo/fastapi/issues/2026
    assert resp.status_code == 403


def test_get_task(client, task):
    resp = client.get(f"/tasks/{task.id}")
    assert resp.status_code == 200
    assert resp.json() == {
        "id": task.id,
        "list_id": task.todo_list_id,
        "task": task.task,
        "completed": False,
    }


def test_get_task_nonexistent(client):
    resp = client.get("/tasks/8675309")
    assert resp.status_code == 404


def test_get_task_user_mismatch(other_client, task):
    resp = other_client.get(f"/tasks/{task.id}")
    assert resp.status_code == 404


def test_update_task(client, task):
    updated_task = f"{task.task} (updated)"
    resp = client.patch(f"/tasks/{task.id}", json={"task": updated_task})
    assert resp.status_code == 200
    assert resp.json() == {
        "id": task.id,
        "list_id": task.todo_list_id,
        "task": updated_task,
        "completed": False,
    }
    task.refresh_from_db()
    assert task.task == updated_task


@pytest.mark.freeze_time
def test_update_task_completed(client, task):
    resp = client.patch(f"/tasks/{task.id}", json={"completed": True})
    assert resp.status_code == 200
    assert resp.json() == {
        "id": task.id,
        "list_id": task.todo_list_id,
        "task": task.task,
        "completed": True,
    }
    task.refresh_from_db()
    assert task.completed
    assert task.completed_at == timezone.now()


@pytest.mark.freeze_time
def test_update_task_not_completed(client, task):
    task.completed_at = timezone.now()
    task.save()
    resp = client.patch(f"/tasks/{task.id}", json={"completed": False})
    assert resp.status_code == 200
    assert resp.json() == {
        "id": task.id,
        "list_id": task.todo_list_id,
        "task": task.task,
        "completed": False,
    }
    task.refresh_from_db()
    assert not task.completed
    assert task.completed_at is None


def test_update_task_nonexistent(client):
    resp = client.patch("/tasks/8675309", json={"task": "updated task"})
    assert resp.status_code == 404


def test_update_task_user_mismatch(other_client, task):
    resp = other_client.patch(f"/tasks/{task.id}", json={"name": "updated name"})
    assert resp.status_code == 404


def test_delete_task(client, task):
    resp = client.delete(f"/tasks/{task.id}")
    assert resp.status_code == 204
    with pytest.raises(TodoTask.DoesNotExist):
        task.refresh_from_db()


def test_delete_task_nonexistent(client):
    resp = client.delete("/tasks/8675309")
    assert resp.status_code == 404


def test_delete_task_user_mismatch(other_client, task):
    resp = other_client.delete(f"/tasks/{task.id}")
    assert resp.status_code == 404
