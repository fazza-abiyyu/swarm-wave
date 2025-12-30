# Swarm Wave

A comprehensive web application for Multi-Agent Task Scheduling using Swarm Intelligence algorithms (ACO & PSO).

## Overview

Swarm Wave implements bio-inspired optimization techniques to solve complex resource allocation problems in distributed computing environments. It features a Flask backend for algorithm processing and a Nuxt frontend for real-time visualization and interaction.

## Architecture

- **Backend**: Python/Flask REST API implementing ACO and PSO algorithms.
- **Frontend**: Nuxt 4/Vue 3 web interface for simulation and visualization.

> [!IMPORTANT]
> **DISCLAIMER**: Sistem saat ini baru mendukung dataset spesifik sesuai penelitian dan belum bersifat universal.
> (The system currently only supports specific datasets according to the research and is not universal yet.)

## Key Features

- **Algorithms**: Ant Colony Optimization (ACO) and Particle Swarm Optimization (PSO).
- **Real-time**: WebSocket-like streaming of algorithm progress.
- **Visual Analytics**: Interactive dashboards and performance metrics.
- **Production Ready**: Docker containerization and comprehensive testing.

## Quick Start

The fastest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/fazza-abiyyu/swarm-wave.git
cd swarm-wave

# Set up environment
cp example.env .env
# Edit .env to add your API keys (optional)

# Start application
docker compose up --build
```

- **Frontend**: `http://localhost:3000`
- **Backend**: `http://localhost:5001`

## Documentation

- [Backend Documentation](./backend/README.md)
- [Frontend Documentation](./frontend/README.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
