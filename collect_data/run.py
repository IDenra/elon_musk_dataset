from pathlib import Path

import typer
import pandas as pd

from constants import ELON_MUSK_LOWERED
from collect_data.collectors import collect_dialog_dataset, collect_phrase_dataset
from utils import CsvWriter
from utils.filters import MaxAnswerLengthFilter, AuthorDialogFilter, ChainDialogFilter, AuthorFilter, ChainFilter
from utils.reader import ManyInterviewsReader

app = typer.Typer()


@app.command()
def collect_short_answer_dialogs(
    interview_paths: str = typer.Option(..., help="Paths to jsonlines file with interviews."),
    save_path: Path = typer.Option(..., help="Path to resulting dataset."),
):
    interview_paths = [Path(interview_path) for interview_path in interview_paths.split(',')]
    reader = ManyInterviewsReader(interview_paths)
    writer = CsvWriter(save_path)
    filter_ = ChainDialogFilter([AuthorDialogFilter(ELON_MUSK_LOWERED), MaxAnswerLengthFilter(max_answer_length=50)])
    collect_dialog_dataset(reader, writer, filter_)
    _postprocess_dataset(save_path)


@app.command()
def collect_all_dialogs(
    interview_paths: str = typer.Option(..., help="Paths to jsonlines file with interviews."),
    save_path: Path = typer.Option(..., help="Path to resulting dataset."),
):
    interview_paths = [Path(interview_path) for interview_path in interview_paths.split(',')]
    reader = ManyInterviewsReader(interview_paths)
    writer = CsvWriter(save_path)
    filter_ = ChainDialogFilter([AuthorDialogFilter(ELON_MUSK_LOWERED)])
    collect_dialog_dataset(reader, writer, filter_)
    _postprocess_dataset(save_path)


@app.command()
def collect_all_phrases(
    interview_paths: str = typer.Option(..., help="Paths to jsonlines file with interviews."),
    save_path: Path = typer.Option(..., help="Path to resulting dataset."),
):
    interview_paths = [Path(interview_path) for interview_path in interview_paths.split(',')]
    reader = ManyInterviewsReader(interview_paths)
    writer = CsvWriter(save_path)
    filter_ = ChainFilter([AuthorFilter(ELON_MUSK_LOWERED)])
    collect_phrase_dataset(reader, writer, filter_)
    _postprocess_dataset(save_path)


def _postprocess_dataset(path: Path):
    df = pd.read_csv(path).dropna().drop_duplicates()
    df.to_csv(path, index=False)


if __name__ == '__main__':
    app()
