FROM python:3.7

ENV PORT 8001

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]