<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-yellow-50 flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-blue-600 mb-4">
        Swarm Lab
      </h1>
      <p class="text-lg text-gray-600 mb-8">
        Swarm Intelligence Lab - An educational app built with Nuxt 4 + Tailwind CSS
      </p>
      <NuxtLink 
        to="/dashboard"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        Enter Data Table
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
// Redirect homepage to dashboard
onMounted(() => {
  navigateTo('/dashboard')
})
</script>