FROM python:3.10-alpine

WORKDIR /app
# Install PostgreSQL client libraries and headers

COPY requirements.txt .

RUN \
    apk add --no-cache postgresql-libs  &&  \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3 install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps 


COPY . .

CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000
