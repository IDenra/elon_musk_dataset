# elon_musk_dataset
## Preparing
1. [Install poetry](https://python-poetry.org/docs/#installation)
2. Install dependencies: `poetry install`
3. Activate virtual environment: `poetry shell`

## Scrapping
To scrap data from rev.com use command like that:  
`PYTHONPATH=. python scrap/rev.py --base_url https://www.rev.com/blog/transcripts?s=Elon+Musk --save_path rev-interviews.jsonlines`  

From vox.com:  
`PYTHONPATH=. python scrap/vox.py --interview_url https://www.vox.com/2018/11/2/18053428/recode-decode-full-podcast-transcript-elon-musk-tesla-spacex-boring-company-kara-swisher --save_path vox-interview.jsonlines`  

## Collecting data
`PYTHONPATH=. python collect_data/run.py collect-all-dialogs --interview-paths=rev-interviews.jsonlines,vox-interview.jsonlines --save-path=all_dialog_dataset.csv`  

`PYTHONPATH=. python collect_data/run.py collect-short-answer-dialogs --interview-paths=rev-interviews.jsonlines,vox-interview.jsonlines --save-path=short_answer_dialog_dataset.csv`  

`PYTHONPATH=. python collect_data/run.py collect-all-phrases --interview-paths=rev-interviews.jsonlines,vox-interview.jsonlines --save-path=all_phrases_dataset.csv`