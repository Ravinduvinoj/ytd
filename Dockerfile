# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements file first (to leverage Docker caching)
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Create a directory for downloads
RUN mkdir -p downloads

# Expose the port Flask is running on
EXPOSE 3000

# Set the command to run the Flask app
CMD ["python", "app.py"]
