from pathlib import Path

import click
import requests
from bs4 import BeautifulSoup, Tag

from models import Interview, Replica

_MOZILLA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
HEADERS = ({'User-Agent': _MOZILLA,
            'Accept-Language': 'en-US, en;q=0.5'})


@click.command()
@click.option('--interview_url', required=True, help='Url to interview.')
@click.option('--save_path', required=True, type=Path, help='Path to jsonlines file to save scrapped interviews.')
def scrap(interview_url: str, save_path: Path):
    print('scrapping interview...')
    interview = scrap_interview(interview_url)
    if contains_elon_musk(interview):
        save_interview(save_path, interview)


def scrap_interview(interview_url: str) -> Interview:
    response = requests.get(interview_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    replicas = []
    need_scrap = False
    i = 0
    for bs_replica in soup.find('div', class_='c-entry-content').children:
        if not isinstance(bs_replica, Tag) and bs_replica.name not in ['p', 'hr']:
            continue
        if not need_scrap:
            if bs_replica.name == 'hr':
                need_scrap = True
            continue

        subtag = bs_replica.next
        author = 'Kara Swisher' if subtag.name == 'strong' and subtag.text != 'Elon Musk' else 'Elon Musk'
        text = bs_replica.text.split(':', maxsplit=1)[1] if i < 2 else bs_replica.text

        replica = Replica(author=author, serial_number=i, phrase=text.strip())
        replicas.append(replica)
        i += 1

    return Interview(title=soup.find('h1', class_='c-page-title').text.strip(), url=interview_url, replicas=replicas)


def contains_elon_musk(interview: Interview) -> bool:
    return any(replica.author.lower() == 'elon musk' for replica in interview.replicas)


def save_interview(save_path: Path, interview: Interview):
    with open(save_path, 'a') as f:
        f.write(interview.json(ensure_ascii=False))
        f.write('\n')


if __name__ == '__main__':
    scrap()
