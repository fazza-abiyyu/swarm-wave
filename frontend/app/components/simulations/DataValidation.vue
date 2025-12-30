<template>
  <div v-if="errors.length > 0 || warnings.length > 0" class="bg-white rounded-xl border border-gray-200 shadow-none p-6 mb-6">
    <h3 class="text-lg font-medium text-gray-900 mb-4">Data Validation</h3>

    <div v-if="errors.length > 0" class="mb-4">
      <div v-for="error in errors" :key="error"
        class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-2 text-sm">
        <svg class="w-4 h-4 inline mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
        {{ error }}
      </div>
    </div>

    <div v-if="warnings.length > 0" class="mb-4">
      <div v-for="warning in warnings" :key="warning"
        class="bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded-md mb-2 text-sm">
        <svg class="w-4 h-4 inline mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        {{ warning }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  errors: { type: Array, default: () => [] },
  warnings: { type: Array, default: () => [] }
});
</script>
