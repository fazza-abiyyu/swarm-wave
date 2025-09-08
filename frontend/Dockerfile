# Frontend Dockerfile - Nuxt 4
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json yarn.lock* ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Default command (can be overridden by docker-compose)
CMD ["yarn", "dev"]
