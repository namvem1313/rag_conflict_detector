# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and API code
COPY app/ app/
COPY api/ api/
COPY config/ config/
COPY main.py .

# Expose Flask port
EXPOSE 5055

# Run app
CMD ["python", "main.py"]
