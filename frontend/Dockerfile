# Stage 1: Build the Nuxt application
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json only to allow caching of dependency download
COPY package.json ./

# Install build tools
RUN apk add --no-cache python3 make g++

# Install dependencies ignoring scripts (skips nuxt prepare, avoids missing file errors)
RUN npm install --legacy-peer-deps --ignore-scripts

# Copy the rest of the application source code
COPY . .

# Remove host package-lock.json to avoid platform conflicts (Windows vs Alpine)
RUN rm -f package-lock.json

# Re-run install to build native dependencies and run postinstall scripts (nuxt prepare)
# This uses the packages downloaded in the previous step but ensures everything is correctly built/configured
RUN npm install --legacy-peer-deps

# Build the application for production
RUN npm run build

# Stage 2: Create the final production image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy the built application from the builder stage
# This includes the server, public assets, etc.
COPY --from=builder /app/.output .

# Expose the port the app runs on (default for Nuxt is 3000)
EXPOSE 3000

# The command to start the Nuxt production server
# The entrypoint is located at .output/server/index.mjs
CMD ["node", "server/index.mjs"]
