# Base Image
FROM python:3.10-slim

# Set Working Directory
WORKDIR /app

# Copy Application Code
COPY . /app

# Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Port
EXPOSE 8000

# Run the Application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
