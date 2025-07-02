# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Run the application
# Use a production-grade WSGI server like Gunicorn.
# This command uses the shell form to allow environment variable substitution for $PORT.
# --bind 0.0.0.0:$PORT: Binds to the port specified by Cloud Run.
# --workers 1 --threads 8: A good starting point for concurrency on Cloud Run.
# --timeout 0: Disables Gunicorn's timeout to let Cloud Run manage it.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app