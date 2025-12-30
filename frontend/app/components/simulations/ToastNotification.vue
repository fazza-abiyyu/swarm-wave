<template>
  <div
    v-if="show"
    class="fixed top-4 right-4 z-50 px-4 py-3 rounded-lg border border-gray-200 shadow-none flex items-center animate-fade-in"
    :class="{
      'bg-red-500 text-white': type === 'error',
      'bg-green-500 text-white': type === 'success',
      'bg-blue-500 text-white': type === 'info'
    }"
  >
    <svg v-if="type === 'error'" class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
    </svg>
    <svg v-else-if="type === 'success'" class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
    </svg>
    <span>{{ message }}</span>
  </div>
</template>

<script setup>
defineProps({
  show: { type: Boolean, default: false },
  message: { type: String, default: '' },
  type: { type: String, default: 'error' }
});
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in { animation: fadeIn 0.3s ease-out; }
</style>
