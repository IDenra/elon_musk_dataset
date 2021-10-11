import abc
import csv
from pathlib import Path
from typing import Dict, Any


class IWriter(abc.ABC):
    @abc.abstractmethod
    def write(self, data_piece: Dict[str, Any]):
        ...


class CsvWriter(IWriter):
    def __init__(self, file_path: Path):
        self._file_path = file_path
        self._is_first_run = True

    def write(self, data_piece: Dict[str, Any]):
        with open(self._file_path, 'a') as f:
            csv_writer = csv.DictWriter(f, list(data_piece.keys()))
            if self._is_first_run:
                csv_writer.writeheader()
                self._is_first_run = False
            csv_writer.writerow(data_piece)
