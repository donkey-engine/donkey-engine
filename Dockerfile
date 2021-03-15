FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.dev.txt /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/