FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /user_service_code/
WORKDIR /user_service_code/

COPY requirements.txt /user_service_code/
RUN pip install -r requirements.txt

