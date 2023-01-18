import pytest

from app.main import app, task_manager


@pytest.fixture(scope='session')
def testing_app():
    app.config.update({'TESTING': True})
    yield app


@pytest.fixture(scope='session')
def client(testing_app):
    return testing_app.test_client()


@pytest.fixture(scope='session')
def task_manager_():
    yield task_manager


@pytest.fixture()
def fulfill_tasks(task_manager_):
    tasks = []
    for n in ('a', 'b', 'c'):
        task = task_manager_.create({'name': f'task_{n}'})
        tasks.append(task)

    yield tasks

    for task in tasks:
        task_manager.delete(task.id)
