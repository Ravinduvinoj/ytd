# Use a Windows Server-based Node.js image
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Set the working directory
WORKDIR C:\app

# Copy necessary files
COPY . C:\app

# Expose the application port
EXPOSE 3000

# Start the application
CMD ["node", "server.js"]
