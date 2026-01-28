FROM python:3.13-alpine

ARG UID=1000
ARG GID=1000

WORKDIR /app

RUN apk add --no-cache \
    gcc g++ \
    musl-dev \
    postgresql-dev \
    shadow

RUN groupadd -g ${GID} appuser && \
    useradd -m -u ${UID} -g appuser appuser

COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements-dev.txt

RUN chown -R appuser:appuser /app

USER appuser

ENV PORT=8000
EXPOSE ${PORT}

CMD python manage.py runserver 0.0.0.0:${PORT}
