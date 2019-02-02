FROM python:3.7-stretch

ADD main.py /

WORKDIR /solution
COPY . /solution

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

ENV NAME Solution

CMD [ "python", "main.py" ]
