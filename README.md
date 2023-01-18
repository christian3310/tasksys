# Task System

A Simple task system.

# Before Start

> The python version is 3.10

This project use poetry to manage packages and environment, please install it if you don't have poetry on your computer. Or, just run docker-compose to start the service.

```bash
pip install -U poetry
```

then run this command to do initialization.

```bash
poetry install
```

To activate virtualenv, exec the following command:

```bash
poetry shell
```

# Runserver

Execute the following command to run the server, if you're out of virtualenv, add `poetry run` before this command.

```bash
flask --app app.main run
```

Or, run docker directly.

```bash
docker compose up
```

# Usage

### Task model

field | type | note
---|---|---
id | int |
name | string |
status | bool | 0 or 1

### Get all tasks

> GET /tasks

```
Response {
"result": [
        {"id": 1, "name": "name", "status": 0}
    ]
}
```

### Create a task

> POST /task

```
Request {
    "name": "買晚餐"
}

Response (201) {
    "result": {"name": "買晚餐", "status": 0, "id": 1}
}
```

### Update a task

> PUT /task/<id>

```
Request {
    "name": "買早餐", "status": 1 "id": 1
}

Response (200) {
    "result": {"name": "買早餐", "status": 1, "id": 1}
}
```

### Delete a task

> DELETE /task/<id>

```
Response (200)
```

# Test

Run `pytest` directly, adding `peotry run` if you're out of the poerty shell.

```bash
# run with docker
docker exec -i tasksys poetry run pytest
```