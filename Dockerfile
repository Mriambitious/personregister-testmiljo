FROM python:3.9-slim
WORKDIR /app
COPY . /app

# Create a directory for the database
RUN mkdir -p /data

CMD ["python", "app.py"]