# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables (optional, you can also set these in your deployment environment)
ENV FLASK_APP=app.py

# Expose the port that the Flask app runs on
EXPOSE 5001

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
