import pytest
from pydantic import ValidationError

from app.managers import TaskManager
from app.models import Task


class TestTaskManager:
    manager = None

    def setup_method(self):
        self.manager = TaskManager()
        for i in range(1, 3):
            self.manager.create({'name': f'task_{i}'})
    
    def test_get_all(self):
        tasks = self.manager.get_all()
        for i, task in enumerate(tasks, 1):
            assert task.id == i
            assert task.name == f'task_{i}'
            assert task.status == 0
        
        self.manager = TaskManager()
        assert self.manager.get_all() == []

    @pytest.mark.parametrize(
        'key,expected_result',
        [
            ('task-1', {'id': 1, 'name': 'task_1', 'status': 0}),
            ('task-2', {'id': 2, 'name': 'task_2', 'status': 0}),
            ('task-3', None),
        ]
    )
    def test_get(self, key, expected_result):
        task = self.manager.get(key)
        if task:
            assert task.dict() == expected_result
        else:
            assert task is None
    
    @pytest.mark.parametrize(
        'task_name,expected_result',
        [
            ('task_3', {'id': 3, 'name': 'task_3', 'status': 0}),
            ('task_4', {'id': 3, 'name': 'task_4', 'status': 0}),
        ]
    )    
    def test_create(self, task_name, expected_result):
        task = self.manager.create({'name': task_name})
        assert task.dict() == expected_result
    
    @pytest.mark.parametrize(
        'pk,data,expected_result',
        [
            (
                1,
                {'id': 1, 'name': 'task_1', 'status': 1},
                {'id': 1, 'name': 'task_1', 'status': 1}
            ),
            (
                2,
                {'id': 2, 'name': 'task_2_1'},
                {'id': 2, 'name': 'task_2_1', 'status': 0}
            ),
            (
                3,
                {'id': 3, 'name': 'task_3', 'status': 1},
                'Task <3> does not exist'
            ),
            (
                1,
                {'id': 2, 'name': 'task_1', 'status': 1},
                'invalid updating on Task <1>'
            ),
            (
                1,
                {'id': 1, 'name': 'task_1', 'status': 5},
                '1 validation error'
            )
        ]
    )
    def test_update(self, pk, data, expected_result):
        result = self.manager.update(pk, data)
        print(result)
        if isinstance(result, Task):
            assert result.dict() == expected_result
        else:
            assert result.startswith(expected_result)

    @pytest.mark.parametrize(
        'pk,expected_result',
        [
            (1, 'success'),
            (3, 'failure')
        ]
    )
    def test_delete(self, pk, expected_result):
        assert self.manager.delete(pk) == expected_result
