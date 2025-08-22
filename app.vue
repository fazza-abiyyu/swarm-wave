<template>
  <div id="app">
    <NuxtPage />
  </div>
</template>

<script setup>
// App.vue - Root component for Swarm Lab
// This is the main entry point for the Nuxt 3 application
</script>

<style>
/* Global styles for Swarm Lab */
html {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  padding: 0;
  background-color: #f8fafc;
}

/* Custom scrollbar for webkit browsers */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Focus styles for accessibility */
:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Smooth transitions */
* {
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, 
              border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

/* Responsive typography */
@media (max-width: 768px) {
  html {
    font-size: 14px;
  }
}

/* Print styles */
@media print {
  body {
    background: white;
  }
  
  .no-print {
    display: none;
  }
}
</style>