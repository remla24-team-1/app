# Dockerfile
FROM python:3.12.3-slim

RUN apt-get update && apt-get install -y \
    libjpeg-dev

WORKDIR /app

# download python dependencis from txt file
COPY app-service/requirements.txt /app/app-service/
RUN pip install -r /app/app-service/requirements.txt


COPY ./app-frontend /app/app-frontend
COPY ./app-service /app/app-service

# python dependencies
# RUN pip install Flask==3.0.3 \
#     Flask-Cors==3.0.10 remlaversionutilpy==0.1.1.dev1 python-dotenv==1.0.1 Requests==2.31.0
    
EXPOSE 8080

CMD ["python", "app-service/server.py"]
