FROM python:3.14-slim-bookworm

WORKDIR /demo

COPY . .

RUN apt-get update && apt-get -y install gcc build-essential python3-dev
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uwsgi", "uwsgi.ini"]