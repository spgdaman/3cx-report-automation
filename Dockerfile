FROM python:3.7

WORKDIR /3cx-report-automation

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD  python app.py