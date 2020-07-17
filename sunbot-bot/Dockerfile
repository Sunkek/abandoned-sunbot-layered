FROM gorialis/discord.py:minimal

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]