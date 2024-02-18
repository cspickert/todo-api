import pytest

from todo.models import TodoList, TodoTask


def test_create_list(client):
    resp = client.post("/lists", json={"name": "new test list"})
    assert resp.status_code == 201
    todo_list = TodoList.objects.last()
    assert resp.json() == {"id": todo_list.id, "name": "new test list"}


def test_create_list_missing_field(client):
    resp = client.post("/lists", json={})
    assert resp.status_code == 422
    errors = resp.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["type"] == "missing"
    assert errors[0]["loc"] == ["body", "name"]


def test_get_lists(client, todo_list):
    resp = client.get("/lists")
    assert resp.status_code == 200
    assert resp.json() == {"results": [{"id": todo_list.id, "name": todo_list.name}]}


def test_get_lists_anon(anon_client):
    resp = anon_client.get("/lists")
    # TODO: change to 401, see https://github.com/tiangolo/fastapi/issues/2026
    assert resp.status_code == 403


def test_get_list(client, todo_list):
    resp = client.get(f"/lists/{todo_list.id}")
    assert resp.status_code == 200
    assert resp.json() == {"id": todo_list.id, "name": todo_list.name}


def test_get_list_nonexistent(client):
    resp = client.get("/lists/8675309")
    assert resp.status_code == 404


def test_get_list_user_mismatch(other_client, todo_list):
    resp = other_client.get(f"/lists/{todo_list.id}")
    assert resp.status_code == 404


def test_update_list(client, todo_list):
    updated_name = f"{todo_list.name} (updated)"
    resp = client.patch(f"/lists/{todo_list.id}", json={"name": updated_name})
    assert resp.status_code == 200
    assert resp.json() == {"id": todo_list.id, "name": updated_name}
    todo_list.refresh_from_db()
    assert todo_list.name == updated_name


def test_update_list_nonexistent(client):
    resp = client.patch("/lists/8675309", json={"name": "updated name"})
    assert resp.status_code == 404


def test_update_list_user_mismatch(other_client, todo_list):
    resp = other_client.patch(f"/lists/{todo_list.id}", json={"name": "updated name"})
    assert resp.status_code == 404


def test_delete_list(client, todo_list, task):
    assert todo_list.tasks.get() == task
    resp = client.delete(f"/lists/{todo_list.id}")
    assert resp.status_code == 204
    with pytest.raises(TodoList.DoesNotExist):
        todo_list.refresh_from_db()
    with pytest.raises(TodoTask.DoesNotExist):
        task.refresh_from_db()


def test_delete_list_nonexistent(client):
    resp = client.delete("/lists/8675309")
    assert resp.status_code == 404


def test_delete_list_user_mismatch(other_client, todo_list):
    resp = other_client.delete(f"/lists/{todo_list.id}")
    assert resp.status_code == 404
