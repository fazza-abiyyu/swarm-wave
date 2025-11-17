<template>
  <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
    <h2 class="text-2xl font-bold mb-4 text-gray-800">🎯 Select Algorithms</h2>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <label
        v-for="algo in availableAlgorithms"
        :key="algo"
        class="flex items-center p-4 border-2 rounded-lg cursor-pointer transition"
        :class="isSelected(algo) ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'"
      >
        <input
          type="checkbox"
          :value="algo"
          :checked="isSelected(algo)"
          @change="toggleAlgorithm(algo)"
          class="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
        />
        <div class="ml-3">
          <span class="font-semibold text-gray-900">{{ algo }}</span>
          <p class="text-sm text-gray-600">{{ getAlgorithmDescription(algo) }}</p>
        </div>
      </label>
    </div>
    
    <p v-if="selectedAlgorithms.length === 0" class="mt-4 text-sm text-red-600">
      ⚠️ Please select at least one algorithm
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  selectedAlgorithms: { type: Array, required: true }
});

const emit = defineEmits(['update:selectedAlgorithms']);

const availableAlgorithms = ['ACO', 'PSO'];

const isSelected = (algo) => props.selectedAlgorithms.includes(algo);

const toggleAlgorithm = (algo) => {
  const newSelection = isSelected(algo)
    ? props.selectedAlgorithms.filter(a => a !== algo)
    : [...props.selectedAlgorithms, algo];
  
  emit('update:selectedAlgorithms', newSelection);
};

const getAlgorithmDescription = (algo) => {
  const descriptions = {
    'ACO': 'Ant Colony Optimization - Bio-inspired swarm intelligence',
    'PSO': 'Particle Swarm Optimization - Population-based stochastic optimization'
  };
  return descriptions[algo] || '';
};
</script>
