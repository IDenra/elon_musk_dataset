# elon_musk_dataset
## Preparing
1. [Install poetry](https://python-poetry.org/docs/#installation)
2. Install dependencies: `poetry install`
3. Activate virtual environment: `poetry shell`

## Scrapping
To scrap data from rev.com use command like that:  
`PYTHONPATH=. python scrap/rev.py --base_url https://www.rev.com/blog/transcripts?s=Elon+Musk --save_path rev-interviews.jsonlines`