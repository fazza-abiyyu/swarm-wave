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
      title: "Swarm Wave - Swarm Intelligence Simulation",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          name: "description",
          content:
            "Swarm Wave is a Vue 3 + Tailwind CSS web app for simulating and visualizing Ant Colony Optimization (ACO) and Particle Swarm Optimization (PSO) algorithms in multi-agent task scheduling and resource management.",
        },
        // Security meta tags
        { 'http-equiv': 'X-Content-Type-Options', content: 'nosniff' },
        { 'http-equiv': 'X-Frame-Options', content: 'SAMEORIGIN' },
        { 'http-equiv': 'X-XSS-Protection', content: '1; mode=block' },
        { 'http-equiv': 'Referrer-Policy', content: 'strict-origin-when-cross-origin' },
        // Hide Nuxt generator info
        { name: 'generator', content: '' }
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    },
  },
  // Server-side configuration for security headers
  nitro: {
    routeRules: {
      '/**': {
        headers: {
          'X-Frame-Options': 'SAMEORIGIN',
          'X-Content-Type-Options': 'nosniff',
          'X-XSS-Protection': '1; mode=block',
          'Referrer-Policy': 'strict-origin-when-cross-origin',
          'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=(), usb=()',
          'Content-Security-Policy': "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob: https:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com https://*.vercel.app https://*.vanila.app; style-src 'self' 'unsafe-inline' https: https://*.vercel.app https://*.vanila.app; img-src 'self' data: blob: https: http:; connect-src 'self' http://localhost:* http://127.0.0.1:* https: wss: ws:; font-src 'self' data: https:; object-src 'self' data:; base-uri 'self'; form-action 'self' https:; frame-ancestors 'self'"
        }
      }
    },
    // Remove X-Powered-By header
    experimental: {
      payloadExtraction: false
    }
  }
});
