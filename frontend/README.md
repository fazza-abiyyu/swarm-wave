# 🐜 Swarm Lab Frontend - Cloud Task Scheduling Interface

A modern web application built with **Nuxt 4**, **Vue 3**, and **Tailwind CSS** for visualizing and interacting with swarm intelligence algorithms (ACO & PSO) in cloud task scheduling scenarios.

## 🚀 Overview

The frontend provides an intuitive interface for:
- **Interactive Algorithm Simulation**: Run ACO and PSO algorithms with real-time visualization
- **Dynamic Data Management**: Import, edit, and manage task scheduling datasets
- **Performance Visualization**: Real-time charts and metrics display using Chart.js
- **Streaming Results**: Live updates from backend algorithms via server-sent events
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

## 🎯 Key Features

### 🧪 **Algorithm Simulation**
- **Ant Colony Optimization (ACO)**: Parameter tuning with real-time feedback
- **Particle Swarm Optimization (PSO)**: Swarm behavior visualization
- **Live Streaming**: Real-time algorithm progress with WebSocket-like streaming
- **Interactive Charts**: Performance metrics visualization with Chart.js
- **Parameter Controls**: Adjust algorithm parameters dynamically

### 📊 **Data Management**
- **CSV Import/Export**: Handle large datasets for task scheduling
- **Dynamic Table Editor**: Excel-like editing experience
- **JSON Data Processing**: Flexible data format support
- **Sample Datasets**: Pre-loaded cloud task scheduling examples
- **Data Validation**: Input validation with user-friendly error messages

### 🎨 **User Experience**
- **Toast Notifications**: Elegant, non-intrusive feedback system
- **Loading States**: Visual feedback during algorithm execution
- **Responsive Layout**: Mobile-first design with Tailwind CSS
- **Modern UI**: Clean, academic-focused interface design

## 🛠️ Technology Stack

### **Core Framework**
- **Nuxt 4**: Vue.js meta-framework with server-side rendering
- **Vue 3**: Composition API with TypeScript support
- **TypeScript**: Type safety and enhanced developer experience

### **Styling & UI**
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Interactive data visualization
- **Custom Components**: Modular, reusable UI components

### **Data & APIs**
- **Server-Sent Events**: Real-time streaming from Flask backend
- **Fetch API**: Modern HTTP client for API communication
- **JSON Processing**: Flexible data handling and validation

### **AI Integration**
- **Google Generative AI**: Enhanced user interactions
- **Marked**: Markdown processing for rich text content

## 📁 Project Structure

```
frontend/
├── app/                        # Application Source
│   ├── app.vue                # Root Application Component
│   ├── components/            # Reusable Components
│   │   ├── DynamicTable.vue   # Interactive Data Table
│   │   └── SimulationPage.vue # Main Algorithm Interface
│   ├── composables/           # Vue Composables
│   │   └── useAiChatStream.ts # Streaming API Client
│   └── pages/                 # Route Pages
│       ├── index.vue          # Landing Page
│       ├── about.vue          # About Page
│       └── dashboard/         # Dashboard Section
│           └── index.vue      # Main Dashboard
├── assets/                    # Static Assets
│   └── css/
│       └── main.css           # Global Styles
├── public/                    # Public Static Files
│   ├── favicon.ico
│   └── robots.txt
├── server/                    # Server API Routes
│   └── api/
│       ├── chat-stream.post.ts # AI Chat Streaming
│       └── test.get.ts        # API Test Endpoint
├── nuxt.config.ts            # Nuxt Configuration
├── package.json              # Dependencies & Scripts
├── tailwind.config.js        # Tailwind Configuration
├── tsconfig.json            # TypeScript Configuration
└── example.env              # Environment Variables Template
```
## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm/yarn
- **Backend**: Ensure Flask backend is running on `http://localhost:5001`

### Development Setup

```bash
# Navigate to frontend directory
cd frontend

# Set up environment variables
cp example.env .env
# Edit .env and add your API keys:
# GEMINI_API_KEY=your_gemini_api_key
# API_URL=http://localhost:5001

# Install dependencies
npm install

# Start development server
npm run dev

# Open browser
Navigate to http://localhost:3000
```

### Build & Deploy

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Generate static site (optional)
npm run generate
```

## 🎨 Core Components

### 🔥 **SimulationPage.vue** - Main Algorithm Interface
The heart of the application, providing:

**Algorithm Controls:**
- Algorithm selection (ACO/PSO)
- Parameter adjustment sliders
- Iteration count settings
- Real-time parameter validation

**Data Management:**
- CSV file upload and parsing
- Dynamic data table editor
- Sample dataset loader
- Data validation and error handling

**Visualization:**
- Real-time progress charts
- Performance metrics display
- Algorithm convergence visualization
- Interactive result tables

**Streaming Integration:**
- Live algorithm updates via Server-Sent Events
- Progress indicators and loading states
- Toast notifications for user feedback
- Error handling and recovery

### 📊 **DynamicTable.vue** - Interactive Data Editor
Excel-like data editing experience:

**Table Operations:**
- Add/remove rows and columns
- Inline cell editing
- Column header customization
- Row selection and bulk operations

**Data Import/Export:**
- CSV file import with validation
- JSON data format support
- Data export to multiple formats
- Sample data templates

**User Experience:**
- Responsive design for all screen sizes
- Keyboard navigation support
- Context menus and shortcuts
- Undo/redo functionality

### 🔗 **useAiChatStream.ts** - Streaming Composable
Custom Vue composable for handling real-time data:

**Features:**
- Server-Sent Events management
- Connection state handling
- Automatic reconnection logic
- Type-safe data streaming

**Usage:**
```typescript
const { streamData, isConnected, error } = useAiChatStream()
```

## 📊 Data Flow Architecture

```
Frontend User Interface
         ↓
    Data Validation
         ↓
  API Request (POST /stream_scheduling)
         ↓
    Flask Backend Processing
         ↓
 Server-Sent Events Stream
         ↓
   Real-time UI Updates
         ↓
    Results Visualization
```

## 🎯 Pages & Routing

### **/** - Landing Page (`index.vue`)
- Project introduction
- Feature highlights  
- Navigation to dashboard

### **/about** - About Page (`about.vue`)
- Project information
- Technology stack details
- Research background

### **/dashboard** - Main Application (`dashboard/index.vue`)
- Algorithm simulation interface
- Data management tools
- Performance monitoring

## ⚙️ Configuration

### **Environment Variables Setup**

The frontend includes an `example.env` template file:

```bash
# Copy the example environment file
cp example.env .env
```

**Frontend .env file structure:**
```bash
# Google Generative AI Key (for enhanced features)
GEMINI_API_KEY=your_gemini_api_key_here

# Backend API URL
API_URL=http://localhost:5001
```

### **Additional Environment Variables (.env)**
```bash
# Backend API Configuration
NUXT_PUBLIC_API_BASE=http://localhost:5001

# Development Settings
NUXT_HOST=0.0.0.0
NUXT_PORT=3000

# Optional: AI Integration
GOOGLE_API_KEY=your_google_api_key
```

### **Nuxt Configuration (nuxt.config.ts)**
Key configurations:
- Tailwind CSS integration
- TypeScript support
- Server-side API routes
- Build optimization settings

### **Tailwind Configuration (tailwind.config.js)**
- Custom color palette
- Responsive breakpoints
- Component utilities
- Animation classes

## � Design System

### **Color Palette**
- **Primary Blue**: `#3b82f6` - Actions, links, primary buttons
- **Secondary Yellow**: `#eab308` - Highlights, secondary actions
- **Success Green**: `#10b981` - Success states, confirmations
- **Error Red**: `#ef4444` - Error states, warnings
- **Neutral Grays**: `#374151` to `#f9fafb` - Text and backgrounds

### **Typography**
- **Font Family**: Inter (system fonts fallback)
- **Headings**: Bold weights with proper scaling
- **Body Text**: Regular weight, optimized line-height
- **Code**: Monospace font for technical content

### **Spacing & Layout**
- **Container**: Responsive max-width with padding
- **Grid System**: Tailwind's flexible grid
- **Component Spacing**: Consistent margin/padding scale
- **Mobile-First**: Progressive enhancement approach

## 🧪 Development

### **Development Scripts**
```bash
# Development server with hot reload
npm run dev

# Type checking
npm run type-check

# Build production bundle
npm run build

# Preview production build
npm run preview

# Generate static site
npm run generate
```

### **Code Quality**
- **TypeScript**: Type safety across components
- **ESLint**: Code quality and consistency
- **Prettier**: Code formatting
- **Git Hooks**: Pre-commit validation

### **Performance Optimization**
- **Code Splitting**: Automatic route-based splitting
- **Tree Shaking**: Unused code elimination
- **Asset Optimization**: Image and font optimization
- **Caching**: Intelligent browser caching strategies

## 📱 Responsive Design

### **Breakpoints**
- **Mobile**: `< 640px` - Stacked layout, touch-optimized
- **Tablet**: `640px - 1024px` - Adapted interface, gesture support
- **Desktop**: `> 1024px` - Full featured interface

### **Mobile Optimizations**
- Touch-friendly button sizes
- Swipe gestures for table navigation
- Optimized modal and dropdown sizing
- Compressed data views for small screens

## 🔗 API Integration

### **Backend Communication**
The frontend communicates with the Flask backend via:

**REST Endpoints:**
- `POST /stream_scheduling` - Algorithm execution
- `GET /health` - Backend health check

**Streaming Events:**
- Real-time algorithm progress
- Performance metrics updates
- Error and status notifications

**Data Format:**
```typescript
interface AlgorithmRequest {
  algorithm: 'ACO' | 'PSO'
  tasks: TaskData[]
  parameters: AlgorithmParameters
}

interface StreamResponse {
  iteration: number
  best_score: number
  metrics: PerformanceMetrics
  status: 'running' | 'completed' | 'error'
}
```

## 🚀 Deployment Options

### **Static Hosting (Recommended)**
```bash
# Generate static site
npm run generate

# Deploy .output/public/ to:
# - Vercel, Netlify, GitHub Pages
# - AWS S3, Google Cloud Storage
# - Any static hosting provider
```

### **Server-Side Rendering**
```bash
# Build for SSR
npm run build

# Deploy to Node.js hosting:
# - Vercel, Railway, Render
# - DigitalOcean, Heroku
# - Custom VPS with PM2
```

### **Docker Deployment**
```bash
# Use provided Dockerfile
docker build -t swarm-lab-frontend .
docker run -p 3000:3000 swarm-lab-frontend

# Or use docker-compose
docker compose up frontend
```

## � Educational Use Cases

Perfect for:
- **Computer Science Courses**: Algorithm visualization and comparison
- **Research Projects**: Cloud computing and task scheduling studies  
- **Student Labs**: Hands-on swarm intelligence experiments
- **Academic Demonstrations**: Interactive algorithm behavior showcase
- **Data Science Education**: Real-time data processing visualization

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Navigate to frontend: `cd frontend`
4. Set up environment: `cp example.env .env` (edit with your API keys)
5. Install dependencies: `npm install`
6. Start development: `npm run dev`
5. Make your changes
6. Test thoroughly
7. Submit a pull request

### **Code Guidelines**
- Follow existing TypeScript patterns
- Use Composition API for Vue components
- Maintain responsive design principles
- Add appropriate error handling
- Write meaningful commit messages

## 🆘 Troubleshooting

### **Common Issues**

**Frontend won't start:**
```bash
# Clear cache and reinstall
rm -rf node_modules .nuxt .output
npm install
npm run dev
```

**API connection issues:**
```bash
# Check backend is running
curl http://localhost:5001/health

# Verify environment variables
echo $NUXT_PUBLIC_API_BASE
```

**Build errors:**
```bash
# Check TypeScript errors
npm run type-check

# Clear build cache
rm -rf .nuxt .output
npm run build
```

---

## 📄 License

This project is licensed under the **MIT License** - see the root [LICENSE](../LICENSE) file for details.

---

**Built with ❤️ for swarm intelligence research and education**

[![Nuxt](https://img.shields.io/badge/Nuxt-4.0-00DC82?logo=nuxt.js)](https://nuxt.com/)
[![Vue](https://img.shields.io/badge/Vue-3.5-4FC08D?logo=vue.js)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4-06B6D4?logo=tailwind-css)](https://tailwindcss.com/)
