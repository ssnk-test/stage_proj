FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /mon_code/
WORKDIR /mon_code/

COPY requirements.txt /mon_code/
RUN pip install -r requirements.txt

