# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's caching mechanism
COPY requirements.txt .

# Install dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port that the app will run on
EXPOSE 3000

# Use Gunicorn to serve the Flask app (with binding to 0.0.0.0:3000)
CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app"]
