FROM python:3

WORKDIR /code

ENV PYTHONUNBUFFERED 1

COPY ./entrypoint.sh .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]