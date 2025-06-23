# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./
COPY package-lock.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the frontend source code
COPY . .

# Expose the port the Vite dev server runs on
EXPOSE 5173

# Command to run the Vite development server
CMD ["npm", "run", "dev"]