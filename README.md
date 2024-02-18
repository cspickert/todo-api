# Todo API

This is a simple to-do list API built with `fastapi` and `django`.

## How to run the API

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
