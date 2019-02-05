FROM python:3.7-stretch

ADD GHubScraper/solution/main.py /

WORKDIR /solution
COPY . /solution

RUN pip install --trusted-host pypi.python.org -r GHubScraper/solution/requirements.txt

EXPOSE 80

ENV NAME Solution

CMD [ "python", "solution/main.py" ]
