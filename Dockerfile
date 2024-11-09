# Use an official python image as the base image
FROM python:3.8-slim-buster

# Set the working directory in the ocntainer to /app
WORKDIR /app

# Copy the contents of the current directory into the container /app
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the default commands to run when starting the container
CMD ["python", "app.py"]