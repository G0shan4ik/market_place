FROM python:3.12-slim-bookworm

WORKDIR /app
COPY . .

RUN pip install poetry && apt update -y
RUN poetry config virtualenvs.create false && apt-get update

RUN poetry install


ENTRYPOINT ["poetry", "run", "dev"]