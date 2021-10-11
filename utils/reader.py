import abc
from pathlib import Path
from typing import Generator, Iterable, Iterator

from models import Interview


class IInterviewReader(abc.ABC):
    @abc.abstractmethod
    def read(self) -> Iterator[Interview]:
        ...


class InterviewReader(IInterviewReader):
    def __init__(self, interviews_path: Path):
        self._interviews_path = interviews_path

    def read(self) -> Iterator[Interview]:
        with open(self._interviews_path) as interviews_file:
            for interview_line in interviews_file:
                yield Interview.from_json(interview_line)


class ManyInterviewsReader(IInterviewReader):
    def __init__(self, interviews_paths: Iterable[Path]):
        self._interviews_paths = interviews_paths

    def read(self) -> Iterator[Interview]:
        for path in self._interviews_paths:
            reader = InterviewReader(path)
            yield from reader.read()


class SquashedInterviewReader(IInterviewReader):
    def __init__(self, interview_reader: IInterviewReader):
        self._interview_reader = interview_reader

    def read(self) -> Iterator[Interview]:
        for interview in self._interview_reader.read():
            yield interview.squash_subsequent_replicas()
