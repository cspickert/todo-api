# Todo API

This is a simple to-do list REST API built with `fastapi` and `django`.

## API overview

The API consists of two resources: lists and tasks. See below for an overview of
each.

### Lists

Endpoint: `/lists[/{id}]`

This resource represents a to-do list, i.e. a collection of tasks (see below).
Each list has the following attributes:
* `id` - A unique ID for the list
* `name` - A user-provided name for the list (e.g. "Reminders")

### Tasks

Endpoint `/tasks[/{id}]`

This resource represents a task on a to-do list. It has the following
attributes:
* `id` - A unique ID for the task
* `list_id` - The ID of the list the task belongs to
* `task` - Arbitrary user-provided task string (e.g. "take out the trash")

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
