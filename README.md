# Swarm Lab - Multi-Agent AI System

A comprehensive multi-agent AI system built with Nuxt 4 (frontend) and Flask (backend) for orchestrating and managing AI agent swarms.

## 🚀 Project Overview

Swarm Lab is a cutting-edge platform designed to create, manage, and deploy AI agent swarms. The system provides an intuitive web interface for configuring agents, monitoring their performance, and orchestrating complex multi-agent workflows.

## 🏗️ Architecture

This project follows a modern microservices architecture with clear separation between frontend and backend:

```
swarm-lab/
├── .gitignore
├── LICENSE
├── README.md
├── backend
    └── app.py
└── frontend
    ├── .gitignore
    ├── AI_CHAT_SETUP.md
    ├── README.md
    ├── app.vue
    ├── app
        ├── app.vue
        ├── components
        │   ├── DynamicTable.vue
        │   └── SimulationPage.vue
        ├── composables
        │   └── useAiChatStream.ts
        └── pages
        │   ├── about.vue
        │   ├── dashboard
        │       └── index.vue
        │   └── index.vue
    ├── assets
        └── css
        │   └── main.css
    ├── nuxt.config.ts
    ├── package.json
    ├── public
        ├── afavicon.ico
        ├── favicon.ico
        └── robots.txt
    ├── server
        └── api
        │   ├── chat-stream.post.ts
        │   └── test.get.ts
    ├── tailwind.config.js
    └── tsconfig.json
```

## 🛠️ Technology Stack

### Frontend (Nuxt 4)
- **Framework**: Nuxt 4 with Vue 3
- **Styling**: Tailwind CSS
- **HTTP Client**: Nuxt HTTP module
- **Icons**: Nuxt Icon module
- **Development**: TypeScript, ESLint, Prettier

### Backend (Flask)
- **Framework**: Flask with Flask-RESTX
- **Validation**: Flask-Marshmallow
- **CORS**: Flask-CORS
- **Environment**: Python 3.9+

## 🚦 Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   # Using yarn
   yarn install
   
   # Or using npm
   npm install
   ```

3. Development server:
   ```bash
   # Using yarn
   yarn dev
   
   # Or using npm
   npm run dev
   ```

4. Build for production:
   ```bash
   # Using yarn
   yarn build
   
   # Or using npm
   npm run build
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   ```

6. Run the development server:
   ```bash
   python run.py
   ```

## 🔧 Configuration

### Frontend Configuration

The frontend configuration is managed through `nuxt.config.ts` and environment variables:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/google-fonts',
    'nuxt-icon',
    '@pinia/nuxt',
    '@vueuse/nuxt',
  ],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:5000/api',
    },
  },
})
```

### Backend Configuration

Environment variables for the backend:

```bash
# .env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/swarm_lab
JWT_SECRET_KEY=your-jwt-secret-key
CORS_ORIGINS=http://localhost:3000
```

## 🧪 Development

### Frontend Development

```bash
# Development server with hot reload
yarn dev

# Type checking
yarn type-check

# Linting
yarn lint

# Formatting
yarn format
```

### Backend Development

```bash
# Run tests
python -m pytest

# Run with debug mode
python run.py --debug

# Database migration
python manage.py db migrate -m "migration message"
python manage.py db upgrade
```

## 🚀 Deployment

### Frontend Deployment

Build the frontend for production:

```bash
yarn build
yarn preview
```

The built files will be in `.output/public/` directory, ready to be served by any static hosting service.

### Backend Deployment

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn run:app
```

### Docker Deployment

Both frontend and backend include Docker configurations:

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `/docs` directory
- Join our community discussions

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes and updates.

---

**Built with ❤️ using Nuxt 4 and Flask**