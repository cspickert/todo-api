# Todo API

This is a simple to-do list API built with `fastapi` and `django`.

## Quick start

To run the API locally (http://localhost:8000), run the following:

```sh
$ pipenv shell
$ pipenv install
$ python manage.py setup_db
$ uvicorn asgi:app
```

These requests should work out of the box after running the commands above:

```sh
$ TODO_API_AUTH="Authorization: Bearer 5Pm3njv9csfhBLvLyJXdTeBFmjlw8bs2"
$ curl -H "$TODO_API_AUTH" "localhost:8000/lists"
$ curl -H "$TODO_API_AUTH" "localhost:8000/lists/1"
$ curl -H "$TODO_API_AUTH" "localhost:8000/tasks?list_id=1"
$ curl -H "$TODO_API_AUTH" "localhost:8000/tasks/1"
```

Try creating, updating, or deleting lists and tasks using `POST`, `PATCH`, and
`DELETE` requests!

## Testing

To run the unit tests, run the following:

```sh
$ pipenv install --dev
$ pipenv run pytest
```
