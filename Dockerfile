# Dockerfile
FROM python:3.12.3-slim

RUN apt-get update && 

WORKDIR /app

COPY ./app-frontend /app/app-frontend

COPY ./app-service /app/app-service

RUN pip install Flask==3.0.3

EXPOSE 5000

CMD ["python", "app-service/server.py"]
