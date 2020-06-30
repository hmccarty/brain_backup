FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 list

CMD ["python3", "app.py"]