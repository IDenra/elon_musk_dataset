from typing import List

from pydantic import BaseModel


class Replica(BaseModel):
    author: str
    serial_number: int
    phrase: str


class Interview(BaseModel):
    title: str
    url: str
    replicas: List[Replica]
