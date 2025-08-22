// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  
  // 应用配置
  app: {
    head: {
      title: 'Swarm Lab - Swarm Intelligence Simulation',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Swarm Lab is a Vue 3 + Tailwind CSS web app for simulating and visualizing Ant Colony Optimization (ACO) and Particle Swarm Optimization (PSO) algorithms in task scheduling and resource management.'  }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    }
  }
})
