import pytest
from pydantic import ValidationError

from app.models import Task


@pytest.mark.parametrize(
    'input_data,expected_status',
    [
        ({'id': 1, 'name': 'test_1', 'status': 0}, 0),
        ({'id': 2, 'name': 'test_2', 'status': 1}, 1),
        pytest.param(
            {'id': 3, 'name': 'test_3', 'status': 2},
            2,
            marks=pytest.mark.xfail(raises=ValidationError)
        )
    ]
)
def test_task_status_conint(input_data, expected_status):
    task = Task(**input_data)
    assert task.status == expected_status
