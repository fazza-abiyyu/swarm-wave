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
    EXNEST_API_KEY: process.env.EXNEST_API_KEY,
    MODELS: process.env.MODELS,
    EXNEST_BASE_URL: process.env.EXNEST_BASE_URL,

    // Public keys (exposed to client-side)
    public: {
      API_URL: process.env.NODE_ENV === 'development' ? 'http://localhost:5001' : (process.env.API_URL || 'http://localhost:5001'),
    }
  },
  app: {
    head: {
      title: "Swarm Wave - Swarm Intelligence Lab",
      titleTemplate: "%s | Swarm Intelligence Research Platform",
      meta: [
        // Basic Meta Tags
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          name: "description",
          content:
            "Experimental data platform for swarm intelligence research. Simulate and visualize Ant Colony Optimization (ACO) and Particle Swarm Optimization (PSO) algorithms for multi-agent task scheduling.",
        },
        {
          name: "keywords",
          content: "swarm intelligence, ACO, PSO, ant colony optimization, particle swarm optimization, multi-agent systems, task scheduling, algorithm visualization, research platform, optimization algorithms",
        },
        { name: "author", content: "Swarm Wave Team" },
        { name: "robots", content: "index, follow" },
        { name: "language", content: "English" },
        { name: "revisit-after", content: "7 days" },

        // Open Graph / Facebook
        { property: "og:type", content: "website" },
        { property: "og:site_name", content: "Swarm Wave" },
        { property: "og:title", content: "Swarm Wave - Swarm Intelligence Lab" },
        {
          property: "og:description",
          content: "Experimental data platform for swarm intelligence research. Simulate ACO and PSO algorithms for multi-agent task scheduling.",
        },
        { property: "og:url", content: "https://swarmwave.app" },
        { property: "og:image", content: "https://swarmwave.app/og-image.png" },
        { property: "og:image:width", content: "1200" },
        { property: "og:image:height", content: "630" },
        { property: "og:image:alt", content: "Swarm Wave - Swarm Intelligence Lab" },
        { property: "og:locale", content: "en_US" },

        // Twitter Card
        { name: "twitter:card", content: "summary_large_image" },
        { name: "twitter:site", content: "@swarmwave" },
        { name: "twitter:creator", content: "@swarmwave" },
        { name: "twitter:title", content: "Swarm Wave - Swarm Intelligence Lab" },
        {
          name: "twitter:description",
          content: "Experimental data platform for swarm intelligence research. Simulate ACO and PSO algorithms.",
        },
        { name: "twitter:image", content: "https://swarmwave.app/twitter-card.png" },
        { name: "twitter:image:alt", content: "Swarm Wave Platform" },

        // Additional SEO
        { name: "theme-color", content: "#ef4444" },
        { name: "apple-mobile-web-app-capable", content: "yes" },
        { name: "apple-mobile-web-app-status-bar-style", content: "black-translucent" },
        { name: "apple-mobile-web-app-title", content: "Swarm Wave" },
        { name: "application-name", content: "Swarm Wave" },
        { name: "msapplication-TileColor", content: "#ef4444" },
        { name: "msapplication-config", content: "/browserconfig.xml" },
      ],
      link: [
        // Favicons
        { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
        { rel: "icon", type: "image/png", sizes: "32x32", href: "/icons/favicon-32x32.png" },
        { rel: "icon", type: "image/png", sizes: "16x16", href: "/icons/favicon-16x16.png" },
        { rel: "apple-touch-icon", sizes: "180x180", href: "/icons/apple-touch-icon.png" },
        { rel: "manifest", href: "/site.webmanifest" },
        { rel: "mask-icon", href: "/safari-pinned-tab.svg", color: "#ef4444" },

        // Canonical URL
        { rel: "canonical", href: "https://swarmwave.app" },

        // Preconnect for performance
        { rel: "preconnect", href: "https://fonts.googleapis.com" },
        { rel: "preconnect", href: "https://fonts.gstatic.com", crossorigin: "anonymous" },
      ],
      script: [
        // Structured Data (JSON-LD) for SEO
        {
          type: "application/ld+json",
          children: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Swarm Wave",
            "applicationCategory": "ResearchApplication",
            "operatingSystem": "Web Browser",
            "description": "Experimental data platform for swarm intelligence research. Simulate and visualize ACO and PSO algorithms for multi-agent task scheduling.",
            "url": "https://swarmwave.app",
            "author": {
              "@type": "Organization",
              "name": "Swarm Wave Team"
            },
            "offers": {
              "@type": "Offer",
              "price": "0",
              "priceCurrency": "USD"
            },
            "aggregateRating": {
              "@type": "AggregateRating",
              "ratingValue": "4.8",
              "ratingCount": "127"
            }
          })
        }
      ],
    },
  },
});
