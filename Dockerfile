FROM python:3.10-slim

WORKDIR /srv
COPY . .

RUN pip install -U poetry
RUN poetry install

ENTRYPOINT [ "poetry", "run" ]
CMD gunicorn -w 1 -b 0.0.0.0 "app.main:app"
