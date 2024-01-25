FROM python:3.11-alpine3.19

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./src /app
COPY ./scripts /scripts
WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
      build-base postgresql-dev musl-dev zlib zlib-dev linux-headers  && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        www-data && \
#    mkdir -p /vol/web/media && \
#    mkdir -p /vol/web/media/uploads && \
#    mkdir -p /vol/web/static && \
#    chown -R www-data:www-data /vol && \
#    chmod -R 755 /vol && \
#    chmod -R 755 /vol/web/media/uploads \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER www-data

CMD ["run.sh"]
