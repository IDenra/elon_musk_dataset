import abc
from typing import Iterable, Callable

from models import Replica


class IFilter(abc.ABC):
    @abc.abstractmethod
    def filter(self, replica: Replica) -> bool:
        ...


class AuthorFilter(IFilter):
    def __init__(self, author_lowered: str):
        self._author_lowered = author_lowered

    def filter(self, replica: Replica) -> bool:
        return replica.author.lower() == self._author_lowered


class MaxLengthFilter(IFilter):
    def __init__(self, max_length: int):
        self._max_length = max_length

    def filter(self, replica: Replica) -> bool:
        return len(replica.phrase) <= self._max_length


class ChainFilter(IFilter):
    def __init__(self, filters: Iterable[IFilter], agg_func: Callable[[Iterable[bool]], bool] = any):
        self._filters = filters
        self._agg_func = agg_func

    def filter(self, replica: Replica) -> bool:
        return self._agg_func(filter_.filter(replica) for filter_ in self._filters)
