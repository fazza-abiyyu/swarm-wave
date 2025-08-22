<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-yellow-50 flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-blue-600 mb-4">
        Swarm Lab
      </h1>
      <p class="text-lg text-gray-600 mb-8">
        群体智能实验室 - 基于Vue 3 + Tailwind CSS的教育主题应用
      </p>
      <NuxtLink 
        to="/dashboard"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        进入数据表格
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
// 首页重定向到dashboard
onMounted(() => {
  navigateTo('/dashboard')
})
</script>