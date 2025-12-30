<template>
  <div v-if="show" class="json-section mb-6 bg-white rounded-lg border border-gray-200 shadow-none p-4 transition-all duration-300">
    <div class="flex justify-between items-center mb-2">
      <label class="block text-sm font-medium text-gray-700">JSON Input</label>
      <button @click="$emit('load-sample')" class="text-sm text-blue-600 hover:text-blue-800 font-medium">
        Load Default Dataset
      </button>
    </div>
    <textarea 
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
      :class="{ 'border-red-300': error }"
      placeholder='// Any dataset structure supported:
// Manufacturing: [{"Job_ID":1,"Processing_Time":45,"Setup_Time":5}]
// Logistics: [{"Order_ID":1,"Distance_km":250,"Weight_kg":1500}]'
    ></textarea>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: String, default: '' },
  show: { type: Boolean, default: false },
  error: { type: Boolean, default: false }
});

defineEmits(['update:modelValue', 'load-sample']);
</script>
