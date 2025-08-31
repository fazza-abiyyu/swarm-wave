// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss"],
  // Development server configuration for Docker
  devServer: {
    host: '0.0.0.0',
    port: 3000
  },
  // Enable file watching for Docker volumes
  vite: {
    server: {
      watch: {
        usePolling: true,
        interval: 1000
      }
    }
  },
  runtimeConfig: {
    // Private keys (only available on server-side)
    GEMINI_API_KEY: process.env.GEMINI_API_KEY,
    
    // Public keys (exposed to client-side)
    public: {
      API_URL: process.env.NODE_ENV === 'development' ? 'http://localhost:5001' : (process.env.API_URL || 'http://localhost:5001'),
    }
  },
  app: {
    head: {
      title: "Swarm Lab - Swarm Intelligence Simulation",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          name: "description",
          content:
            "Swarm Lab is a Vue 3 + Tailwind CSS web app for simulating and visualizing Ant Colony Optimization (ACO) and Particle Swarm Optimization (PSO) algorithms in task scheduling and resource management.",
        },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    },
  },
});
