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

# Build arguments for environment variables
ARG GEMINI_API_KEY=""

# Set environment variables
ENV GEMINI_API_KEY=${GEMINI_API_KEY}
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

# Expose port
EXPOSE 3000

# Default command (can be overridden by docker-compose)
CMD ["yarn", "dev"]
