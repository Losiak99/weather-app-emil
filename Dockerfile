FROM python:3.12-alpine

LABEL org.opencontainers.image.authors="Emil Los"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir flask requests

RUN rm -rf /root/.cache

EXPOSE 5000

CMD ["python", "app.py"]
