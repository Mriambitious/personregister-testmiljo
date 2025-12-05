FROM python:3.9-slim
WORKDIR /app
COPY . /app

# Create a directory for the database
RUN mkdir -p /data

# Set database path 
ENV DATABASE_PATH=/data/test_users.db

CMD ["python", "app.py"]