FROM python:3

ADD GHubScraper/solution/main.py /

RUN pip install -r GHubScraper/requirements.txt

CMD [ "python", "GHubScraper/solution/main.py" ]
