FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP main
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . /app
