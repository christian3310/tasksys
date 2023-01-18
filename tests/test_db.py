import pytest

from app.db import DummyDB


class TestDummyDB:
    db = DummyDB()
    
    def setup_method(self):
        self.db.data = {f'test_{i}': f'value_{i}' for i in range(1, 4)}

    @pytest.mark.parametrize(
        'key,value',
        [
            ('key_1', 'value_1'),
            ('key_2', 'value_2'),
        ]
    )    
    def test_create(self, key, value):
        self.db.create(key, value)
        assert self.db.data[key] == value

        self.db.create(key, f'{value}-2')
        assert self.db.data[key] == value

    @pytest.mark.parametrize(
        'key,expected_value',
        [(f'test_{i}', f'value_{i}') for i in range(1, 4)]
    )
    def test_read(self, key, expected_value):
        assert self.db.read(key) == expected_value
    
    def test_read_all(self):
        assert set(self.db.read_all()) == set(self.db.data.values())

    @pytest.mark.parametrize(
        'key,update_data,expected_result',
        [
            ('test_1', 'value_5', True),
            ('test_2', 'value_4', True),
            ('test_7', None, False)
        ]
    )
    def test_update(self, key, update_data, expected_result):
        assert self.db.update(key, update_data) is expected_result
        assert self.db.data.get(key) == update_data
    
    @pytest.mark.parametrize(
        'key,expected_result',
        [
            ('test_1', True),
            ('test_2', True),
            ('test_7', False)
        ]
    )
    def test_delete(self, key, expected_result):
        assert self.db.delete(key) is expected_result
