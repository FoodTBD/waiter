FROM tiangolo/uwsgi-nginx-flask:python3.11-2023-07-24

COPY ./requirements.lock /app/requirements.lock

RUN pip install --no-cache-dir --upgrade -r /app/requirements.lock

COPY ./app /app
