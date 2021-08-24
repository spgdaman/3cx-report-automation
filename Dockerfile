FROM python:3.7

EXPOSE 8001

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD flask run --host=0.0.0.0 --port=8001