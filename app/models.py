from typing import Union

from pydantic import BaseModel, conint


class Task(BaseModel):
    id: int
    name: str
    status: conint(ge=0, le=1) = 0


class Response(BaseModel):
    result: Union[list[Task], Task, str]
