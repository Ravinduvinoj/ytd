FROM node:20

# Install Python and yt-dlp for Linux
RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install yt-dlp

# Set the working directory
WORKDIR /app

# Copy package.json first to optimize caching
COPY package*.json ./

# Install Node.js dependencies
RUN npm ci --legacy-peer-deps --only=production

# Copy the rest of the application
COPY . .

# Expose the application port
EXPOSE 3000

# Start the application
CMD ["node", "server.js"]
