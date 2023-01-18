FROM python:3.10-slim

ARG GUNICORN_WORKER=2
ENV WORKER=${GUNICORN_WORKER}

WORKDIR /srv
COPY . .

RUN pip install -U poetry
RUN poetry install

ENTRYPOINT [ "poetry", "run" ]
CMD gunicorn -w ${WORKER} -b 0.0.0.0 "app.main:app"
