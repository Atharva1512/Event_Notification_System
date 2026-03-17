# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app directory into the container
COPY ./app ./app

# Expose port 8080
EXPOSE 8080

# Command to run the application using uvicorn, pointing to the app directory
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]