# Use the official Node.js LTS image
FROM node:20

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json first for better caching
COPY package*.json ./

# Install dependencies with optimized options
RUN npm ci --legacy-peer-deps --only=production

# Copy the rest of the application
COPY . .

# Ensure yt-dlp.exe has execute permissions (if present)
RUN chmod +x /app/yt-dlp.exe || true

# Expose the application port
EXPOSE 3000

# Set the command to start the server
CMD ["node", "server.js"]
