# Swarm Wave - Docker Setup

## Quick Start

To run both frontend and backend services:

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop all services
docker-compose down

# View logs
docker-compose logs -f
```

## Individual Services

### Backend (Flask)
```bash
# Build backend image
docker build -t swarm-wave-backend ./backend

# Run backend container
docker run -p 5000:5000 swarm-wave-backend
```

### Frontend (Nuxt 4)
```bash
# Build frontend image
docker build -t swarm-wave-frontend ./frontend

# Run frontend container
docker run -p 3000:3000 swarm-wave-frontend
```

## Services

- **Frontend**: http://localhost:3000 (Nuxt 4)
- **Backend**: http://localhost:5000 (Flask API)

## Development

For development with hot reloading:

```bash
# Override command for development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## Environment Variables

Create `.env` files in respective directories:

### Backend `.env`
```
FLASK_ENV=development
FLASK_DEBUG=1
```

### Frontend `.env`
```
BACKEND_URL=http://localhost:5000
```
