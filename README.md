# To-do API

## Overview

This is a simple REST API for managing to-do lists and tasks, built with
`fastapi` and the `django` ORM (with data stored in SQLite).

### Example

Here's an example of how this API can be used to create and manage to-dos:

* `POST /lists {"name": "Work"}` - create a "Work" to-do list
* `POST /tasks {"list_id": 1, "task": "Design API"}` - add a task to the list
* `POST /tasks {"list_id": 1, "task": "Write documentation"}` - add another task to the list
* `GET /tasks?list_id=1` - get tasks on the list
* `PATCH /tasks/1 {"task": "Design & build API"}` - update a task
* `DELETE /tasks/2` - remove a task
* `DELETE /lists/1` - remove a list (and all associated tasks)

## API overview

The API consists of two resources, lists and tasks.

Requests must be authenticated using API keys passed via the HTTP
`Authorization` header with the value formatted as `Bearer <api_key>`. Requests
made with a given API key can only be used to interact data created by the API
key's associated user (keys for different users cannot be used to access one
anothers' data).

### Lists

Endpoint: `/lists[/{id}]`

This resource represents a to-do list, i.e. a collection of tasks (see below).
Each list has the following attributes:
* `id` - The auto-generated unique ID for the list
* `name` - A user-provided name for the list (e.g. "Reminders")

Supported operations:
* `POST /lists` - create a list
* `GET /lists` - get all lists created by the requesting user
* `GET /lists/{id}` - get the list with the provided `id`
* `PATCH /lists/{id}` - update one or more attributes of the list with the provided `id`
* `DELETE /lists/{id}` - delete the list with the provided `id` *and all associated tasks*

### Tasks

Endpoint `/tasks[/{id}]`

This resource represents a task on a to-do list. It has the following
attributes:
* `id` - The auto-generated unique ID for the task
* `list_id` - The ID of the list the task belongs to
* `task` - Arbitrary user-provided task string (e.g. "take out the trash")

Supported operations:
* `POST /tasks` - create a task
* `GET /tasks` - get all tasks created by the requesting user
* `GET /tasks?list_id={list_id}` - get all tasks on the to-do list with the provided list `id`
* `GET /tasks/{id}` - get the task with the provided `id`
* `PATCH /tasks/{id}` - update one or more attributes of the task with the provided `id`
* `DELETE /tasks/{id}` - delete the task with the provided `id`

## Running the API

To run the API locally (http://localhost:8000), run the following:

```sh
$ pipenv shell
$ pipenv install
$ python manage.py setup_db
$ uvicorn asgi:app
```

This API key is now ready to use: `5Pm3njv9csfhBLvLyJXdTeBFmjlw8bs2`

## Swagger UI

Navigate to http://localhost:8000/docs to view and interact with the API in your
web browser.

## Command line

You can also try out the API via `curl` on the command line:

```sh
$ TODO_API_AUTH="Authorization: Bearer 5Pm3njv9csfhBLvLyJXdTeBFmjlw8bs2"
$ curl -H "$TODO_API_AUTH" "localhost:8000/lists"
$ curl -H "$TODO_API_AUTH" "localhost:8000/lists/1"
$ curl -H "$TODO_API_AUTH" "localhost:8000/tasks?list_id=1"
$ curl -H "$TODO_API_AUTH" "localhost:8000/tasks/1"
```

Try creating, updating, or deleting lists and tasks using `POST`, `PATCH`, and
`DELETE` requests.

## Testing

To run the unit tests, run the following:

```sh
$ pipenv install --dev
$ pipenv run pytest
```
