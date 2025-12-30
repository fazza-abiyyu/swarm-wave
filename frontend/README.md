# Swarm Wave Frontend

A modern web application built with Nuxt 4, Vue 3, and Tailwind CSS for visualizing and interacting with swarm intelligence algorithms (ACO & PSO) in multi-agent task scheduling scenarios.

## Overview

The frontend provides an intuitive interface for interactive algorithm simulation, dynamic data management, performance visualization with Chart.js, and real-time result streaming from the backend.

## Key Features

- **Algorithm Simulation**: Interactive controls for ACO and PSO with real-time feedback.
- **Visualization**: Live charts and metrics for algorithm convergence and performance.
- **Data Management**: Excel-like table editor for managing task datasets (CSV/JSON).
- **Real-time Streaming**: Live updates via Server-Sent Events (SSE).
- **Responsive Design**: Optimized for desktop and mobile devices.

## Technology Stack

- **Framework**: Nuxt 4, Vue 3, TypeScript
- **Styling**: Tailwind CSS
- **Visualization**: Chart.js
- **API**: Server-Sent Events (SSE), standard Fetch API

## Project Structure

```
frontend/
├── app/
│   ├── components/    # Reusable UI components
│   ├── pages/         # Route pages (index, dashboard, about)
│   └── composables/   # Vue composables (state, streaming)
├── server/            # Server API routes
├── nuxt.config.ts    # Nuxt configuration
└── tailwind.config.js # Tailwind configuration
```

## Quick Start

### Prerequisites
- Node.js 18+
- Backend running on `http://localhost:5001`

### Development Setup

```bash
cd frontend

# Set up environment variables
cp example.env .env
# Edit .env: API_URL=http://localhost:5001

# Install dependencies
npm install

# Start development server
npm run dev
```

Navigate to `http://localhost:3000`.

### Build & Deploy

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Generate static site
npm run generate
```

## Core Components

### SimulationPage.vue
The main interface for running algorithms. Handles parameter configuration, data selection, and real-time visualization of results.

### DynamicTable.vue
An interactive data editor allowing users to create, import (CSV/JSON), and modify task scheduling datasets.

### useAiChatStream.ts
A Composable that manages the Server-Sent Events connection for streaming real-time algorithm progress.

## Configuration

Environment variables can be configured in `.env`:

```bash
GEMINI_API_KEY=your_key  # Optional: For AI features
API_URL=http://localhost:5001
```

## Troubleshooting

- **Connection Issues**: Ensure the Flask backend is running and accessible at `API_URL`.
- **Build Errors**: Run `npm run type-check` to identify TypeScript issues.
- **Clean Install**: If issues persist, remove `node_modules` and `.nuxt`, then reinstall dependencies.
