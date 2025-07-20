FROM python:3.11-alpine

RUN addgroup -g 1000 homecv && \
    adduser -u 1000 -G homecv -s /bin/sh -D homecv

RUN apk add --no-cache \
    glib \
    libstdc++ \
    libgomp \
    libgcc

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=homecv:homecv . .

USER homecv

EXPOSE 9000

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "2", "run:app"]
