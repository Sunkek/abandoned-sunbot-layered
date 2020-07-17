FROM python:3

WORKDIR /code

ENV PYTHONUNBUFFERED 1

COPY entrypoint.sh entrypoint.sh

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["sudo", "apt", "install", "netcat"]

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]