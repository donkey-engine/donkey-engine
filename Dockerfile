FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
COPY requirements.dev.txt /code/
RUN pip install -r requirements.dev.txt
COPY . /code/
