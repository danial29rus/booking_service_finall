
FROM python:3.10

RUN mkdir /booking_service

WORKDIR /booking_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /booking_service/docker/docker-bootstrap.sh
