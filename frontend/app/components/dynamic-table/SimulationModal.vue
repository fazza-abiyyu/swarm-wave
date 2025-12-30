<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900">Swarm Intelligence Simulation</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <div class="space-y-4">
        <p class="text-sm text-gray-600">Select algorithms to run on your current table data:</p>

        <div class="space-y-3">
          <label class="flex items-center space-x-3">
            <input type="checkbox" :checked="modelValue.includes('ACO')" @change="toggleAlgorithm('ACO')"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
            <div>
              <span class="text-sm font-medium text-gray-700">Ant Colony Optimization (ACO)</span>
              <p class="text-xs text-gray-500">Mimics ant foraging behavior</p>
            </div>
          </label>

          <label class="flex items-center space-x-3">
            <input type="checkbox" :checked="modelValue.includes('PSO')" @change="toggleAlgorithm('PSO')"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
            <div>
              <span class="text-sm font-medium text-gray-700">Particle Swarm Optimization (PSO)</span>
              <p class="text-xs text-gray-500">Models bird flocking behavior</p>
            </div>
          </label>
        </div>

        <div class="flex space-x-3 pt-4">
          <button @click="$emit('run')"
            class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium">
            Run Simulation
          </button>
          <button @click="$emit('close')"
            class="flex-1 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors font-medium">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: { type: Boolean, default: false },
  modelValue: { type: Array, default: () => [] }
});

const emit = defineEmits(['close', 'run', 'update:modelValue']);

const toggleAlgorithm = (algo) => {
  const current = [...props.modelValue];
  const index = current.indexOf(algo);
  if (index > -1) current.splice(index, 1);
  else current.push(algo);
  emit('update:modelValue', current);
};
</script>
