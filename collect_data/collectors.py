from utils import IInterviewReader, IWriter
from utils.filters import IDialogFilter, IFilter


def collect_dialog_dataset(reader: IInterviewReader, writer: IWriter, filter_: IDialogFilter):
    for interview in reader.read():
        for context, answer in zip(interview.replicas[:-1], interview.replicas[1:]):
            if not filter_.filter(context, answer):
                continue
            dialog_turn = {'context': context.phrase, 'answer': answer.phrase}
            writer.write(dialog_turn)


def collect_phrase_dataset(reader: IInterviewReader, writer: IWriter, filter_: IFilter):
    for interview in reader.read():
        for replica in interview.replicas:
            if not filter_.filter(replica):
                continue
            writer.write({'phrase': replica.phrase})
