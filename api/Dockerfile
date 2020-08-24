FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /api/
WORKDIR /api/
COPY pyproject.toml /api/
RUN pip install poetry
RUN poetry install




