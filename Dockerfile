FROM python:3.7

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5050

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]