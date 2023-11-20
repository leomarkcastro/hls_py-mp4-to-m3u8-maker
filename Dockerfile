FROM python:3.11.6-alpine3.17

RUN mkdir -p /app
ADD ./requirements.txt /app/requirements.txt

RUN set -ex \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | sort -u \
    | xargs -r apk info --installed \
    | sort -u)" \
    && apk add --virtual rundeps $runDeps

ADD . /app
WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# install ffmpeg
RUN apk add --no-cache ffmpeg

EXPOSE 8000

ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY ${DJANGO_SECRET_KEY}

RUN ["python", "manage.py", "collectstatic", "--noinput"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "server.wsgi:application"]