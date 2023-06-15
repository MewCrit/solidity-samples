# Dockerfile code goes here
# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Set the environment variable for the application
ENV PYTHONPATH=/app

# Expose port 9999 for the application
EXPOSE 9999

# Run the command to start the application
CMD ["python", "main.py"]
    
