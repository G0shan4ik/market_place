FROM python:3.12-slim-bookworm

WORKDIR /app

COPY . .

RUN pip install poetry && apt update -y && apt install libpq-dev -y && \
    poetry config virtualenvs.create false && \
    apt-get update && apt-get install git -y
RUN poetry install

ENTRYPOINT ["poetry", "run", "dev"]