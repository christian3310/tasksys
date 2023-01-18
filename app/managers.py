from typing import Union

from pydantic import BaseModel, ValidationError

from app.db import DummyDB
from app.models import Task


def decorate_primary_key(f):
    def wrapper(ins, pk, *args):
        pk = f'{ins.model_name}-{pk}'
        return f(ins, pk, *args)
    return wrapper


class Manager:
    def __init__(self):
        self.model: BaseModel = self.Meta.model
        self.model_name = self.model.__name__
        self.db = DummyDB()

    @decorate_primary_key
    def get(self, pk: int) -> Union[BaseModel, bool]:
        raw_data = self.db.read(pk)
        return self.model.parse_raw(raw_data) if raw_data else None
    
    def get_all(self) -> list[BaseModel]:
        data = [self.model.parse_raw(v) for v in self.db.read_all()]
        return sorted(data, key=lambda d: d.id)

    def create(self, data: dict) -> Union[BaseModel, str]:
        data['id'] = self.db.index_forward()
        try:
            item = self.model.parse_obj(data)
        except ValidationError as e:
            return str(e)

        self.db.create(f'{self.model_name}-{item.id}', item.json())
        return item

    def update(self, pk: int, data: dict) -> Union[BaseModel, str]:
        item = self.get(pk)
        if not item:
            return f'{self.model_name} <{pk}> does not exist'
        elif item.id != data['id']:
            return f'invalid updating on {self.model_name} <{pk}>'

        item_dict = item.dict()
        item_dict.update(data)
        try:
            item = self.model.parse_obj(item_dict)
        except ValidationError as e:
            return str(e)

        self.db.update(f'{self.model_name}-{item.id}', item.json())
        return item

    @decorate_primary_key
    def delete(self, pk: int) -> str:
        return 'success' if self.db.delete(pk) else 'failure'


class TaskManager(Manager):
    class Meta:
        model = Task
