# Use the official Node.js 20 LTS image as the base image
FROM node:20

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker caching
COPY package*.json ./

# Install dependencies using npm ci for a clean, reproducible build
RUN npm ci --only=production

# Copy the rest of the application files
COPY . .

# Create a directory for downloads and set correct permissions
RUN mkdir -p /app/downloads && chmod -R 777 /app/downloads

# Install yt-dlp properly
RUN apt-get update && \
    apt-get install -y python3 python3-pip yt-dlp && \
    chmod +x /usr/bin/yt-dlp && \
    rm -rf /var/lib/apt/lists/*

# Expose the port the app will run on
EXPOSE 3000

# Define the command to run the application
CMD ["node", "server.js"]
