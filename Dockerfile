FROM python:3

WORKDIR /app

COPY . /app

RUN curl -sSL https://install.python-poetry.org | python -

RUN poetry install --no-interaction --no-ansi

EXPOSE 80

ENV POSTGRES_DB: test_database
ENV POSTGRES_USER: test_username
ENV POSTGRES_PASSWORD: test_password
ENV POSTGRES_HOST=postgres