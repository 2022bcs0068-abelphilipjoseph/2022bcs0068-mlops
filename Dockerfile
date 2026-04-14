FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for MLflow/boto3 if needed
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/main.py .

EXPOSE 8000

# uvicorn main:app handles main.py at root after COPY
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
