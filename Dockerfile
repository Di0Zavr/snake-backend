FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app ./app

CMD [ "fastapi", "run", "./app/main.py", "--port", "9000" ]