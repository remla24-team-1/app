# Dockerfile
FROM python:3.12.3-slim

RUN apt-get update && apt-get install -y \
    libjpeg-dev

WORKDIR /app

COPY ./app-frontend /app/app-frontend
COPY ./app-service /app/app-service

# python dependencies
RUN pip install Flask==3.0.3 \
    Flask-Cors==3.0.10

EXPOSE 8080

CMD ["python", "app-service/server.py"]
