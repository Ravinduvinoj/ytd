# Use the official Node.js 20 image as the base image
FROM node:20

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker caching
COPY package*.json ./

# Install dependencies using npm ci for a clean, reproducible build
RUN npm ci --legacy-peer-deps --only=production

# Copy the rest of the application files
COPY . .

# Ensure yt-dlp.exe is executable
RUN chmod +x yt-dlp.exe

# Create a directory for downloads
RUN mkdir -p downloads

# Expose the port the app will run on
EXPOSE 3000

# Define the command to run the application
CMD ["node", "server.js"]