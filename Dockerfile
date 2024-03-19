# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*


# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Upgrade pip to the latest version
RUN python -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

# Copy the rest of the application code into the container at /app
COPY . .

# Expose the port that Gunicorn will run on
# Update the port to match the one you use with Gunicorn
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tk_send_product.wsgi:application"]

