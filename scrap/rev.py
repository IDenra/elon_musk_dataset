from pathlib import Path
from typing import List
import time

import click
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup, Tag

from models import Interview, Replica

_MOZILLA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
HEADERS = ({'User-Agent': _MOZILLA,
            'Accept-Language': 'en-US, en;q=0.5'})


@click.command()
@click.option('--base_url', required=True, help='Url to interview cards.')
@click.option('--save_path', required=True, type=Path, help='Path to jsonlines file to save scrapped interviews.')
@click.option(
    '--request_delay_in_sec', default=0.5, type=float, help='Delay in seconds between each request to website.'
)
def scrap(base_url: str, save_path: Path, request_delay_in_sec: float):
    print('scrapping interview urls...')
    interview_urls = scrap_interview_urls(base_url, request_delay_in_sec)

    for interview_url in tqdm(interview_urls, desc='scrapping interviews'):
        interview = scrap_interview(interview_url)
        if contains_elon_musk(interview):
            save_interview(save_path, interview)
        time.sleep(request_delay_in_sec)


def scrap_interview_urls(base_url: str, request_delay_in_sec: float) -> List[str]:
    page_num = 1
    interview_urls = []
    url_parts = base_url.split('?', maxsplit=1)

    base_url = url_parts[0]
    params = url_parts[1] if len(url_parts) == 2 else ''

    while True:
        response = requests.get(f'{base_url}/page/{page_num}?{params}', headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        post_cards = soup.find_all('div', class_="fl-post-column")
        page_urls = [post_card.find('a')['href'] for post_card in post_cards]
        interview_urls.extend(page_urls)

        if not _is_next_button_present(soup):
            break

        time.sleep(request_delay_in_sec)
        page_num += 1

    return interview_urls


def _is_next_button_present(soup: BeautifulSoup) -> bool:
    return soup.find('a', class_="next") is not None


def scrap_interview(interview_url: str) -> Interview:
    response = requests.get(interview_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    replicas = []
    for i, bs_replica in enumerate(soup.find('div', class_='fl-callout-text').children):
        if not isinstance(bs_replica, Tag) and bs_replica.name != 'p' or not _has_phrase(bs_replica):
            continue

        author_and_time, phrase = bs_replica.text.split('\n')
        if _is_time_present(author_and_time):
            author, _ = author_and_time.split(': ')
        else:
            author = author_and_time

        replica = Replica(author=author, serial_number=i, phrase=phrase)
        replicas.append(replica)

    return Interview(title=soup.find('h1', class_='fl-heading').text.strip(), url=interview_url, replicas=replicas)


def _has_phrase(bs_replica: Tag):
    return '\n' in bs_replica.text


def _is_time_present(author_and_time: str) -> bool:
    return '(' in author_and_time and ')' in author_and_time


def contains_elon_musk(interview: Interview) -> bool:
    return any(replica.author.lower() == 'elon musk' for replica in interview.replicas)


def save_interview(save_path: Path, interview: Interview):
    with open(save_path, 'a') as f:
        f.write(interview.json(ensure_ascii=False))
        f.write('\n')


if __name__ == '__main__':
    scrap()
