<template>
  <div id="app">
    <NuxtPage />
  </div>
</template>

<script setup>
// Global style configuration
useHead({
  title: 'Swarm Wave',
  meta: [
    { name: 'description', content: 'An educational-themed data table management app built with Nuxt 4 and Flask' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
  ]
})
</script>

<style>
/* Global style reset */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #333;
}

#app {
  min-height: 100vh;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Focus styles */
button:focus,
input:focus,
textarea:focus,
select:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Button click effect */
button:active {
  transform: scale(0.98);
}

/* Transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
