import abc
from typing import Iterable, Callable

from models import Replica
from utils.filters.replica import AuthorFilter, MaxLengthFilter


class IDialogFilter(abc.ABC):
    @abc.abstractmethod
    def filter(self, context: Replica, answer: Replica) -> bool:
        ...


class AuthorDialogFilter(IDialogFilter):
    def __init__(self, author_lowered: str):
        self._author_filter = AuthorFilter(author_lowered)

    def filter(self, context: Replica, answer: Replica) -> bool:
        return self._author_filter.filter(answer)


class MaxAnswerLengthFilter(IDialogFilter):
    def __init__(self, max_answer_length: int):
        self._max_length_filter = MaxLengthFilter(max_answer_length)

    def filter(self, context: Replica, answer: Replica) -> bool:
        return self._max_length_filter.filter(answer)


class ChainDialogFilter(IDialogFilter):
    def __init__(self, filters: Iterable[IDialogFilter], agg_func: Callable[[Iterable[bool]], bool] = all):
        self._filters = filters
        self._agg_func = agg_func

    def filter(self, context: Replica, answer: Replica) -> bool:
        return self._agg_func(filter_.filter(context, answer) for filter_ in self._filters)
