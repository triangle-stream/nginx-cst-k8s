# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y curl

# Make port 80 available to the world outside this container
EXPOSE 6000

# Define environment variable
ENV ENV Dev

# Run app.py when the container launches
CMD ["python", "mm4.py"]

