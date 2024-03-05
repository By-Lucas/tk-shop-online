# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install psycopg2-binary instead of psycopg2
RUN pip install psycopg2-binary

# Copy the rest of the application code into the container at /app
COPY . .

# Copy the start script into the container at /app
COPY start.sh .

# Give execution permissions to the start script
RUN chmod +x start.sh

# Expose the port that Gunicorn will run on
# Update the port to match the one you use with Gunicorn
EXPOSE 8000

# Command to run the application using the start script
CMD ["./start.sh"]
