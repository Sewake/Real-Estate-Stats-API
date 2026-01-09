FROM python:3.12.7-slim-bookworm

# Set working directory
WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project
COPY app .

# Gunicorn entrypoint
CMD ["gunicorn", "-b", "0.0.0.0:8000", "config.wsgi:application"]