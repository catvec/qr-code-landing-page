FROM python:3.13-alpine

ARG UID=1000
ARG GID=1000

WORKDIR /app

RUN apk add --no-cache \
    gcc g++ \
    musl-dev \
    postgresql-dev \
    shadow \
    curl

RUN groupadd -g ${GID} appuser && \
    useradd -m -u ${UID} -g appuser appuser

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R appuser:appuser /app

USER appuser

COPY --chown=appuser:appuser . .

RUN python manage.py collectstatic --noinput

ENV PORT=8000
EXPOSE ${PORT}

ENTRYPOINT ["/app/docker-entrypoint.sh"]
