# Swarm Wave Backend

A Flask-based REST API implementing Swarm Intelligence algorithms (ACO and PSO) for multi-agent task scheduling optimization with real-time streaming results.

## Overview

The backend provides a robust API for algorithm execution, real-time progress streaming via Server-Sent Events (SSE), flexible task data handling, and comprehensive performance metrics.

## Documentation

For full documentation in Indonesian, please refer to [backend/docs/README.md](docs/README.md).

## Project Structure

```
backend/
├── models/         # Algorithm Implementations (ACO, PSO)
├── app.py          # Main Flask Application
├── requirements.txt # Dependencies
├── Dockerfile      # Docker Configuration
└── docs/           # Detailed Documentation
```

## Quick Start

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The API will be available at `http://localhost:5001`.
