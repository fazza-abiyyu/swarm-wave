<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-none p-6 mb-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-4">Algorithm Selection</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="flex items-center">
        <input
          :checked="modelValue.includes('ACO')"
          @change="toggleAlgorithm('ACO')"
          type="checkbox" id="aco-checkbox"
          class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
        />
        <label for="aco-checkbox" class="ml-2 text-sm font-medium text-gray-900">
          Ant Colony Optimization (ACO)
        </label>
      </div>
      <div class="flex items-center">
        <input
          :checked="modelValue.includes('PSO')"
          @change="toggleAlgorithm('PSO')"
          type="checkbox" id="pso-checkbox"
          class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
        />
        <label for="pso-checkbox" class="ml-2 text-sm font-medium text-gray-900">
          Particle Swarm Optimization (PSO)
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: { type: Array, default: () => [] }
});

const emit = defineEmits(['update:modelValue']);

const toggleAlgorithm = (algo) => {
  const current = [...props.modelValue];
  const index = current.indexOf(algo);
  if (index > -1) {
    current.splice(index, 1);
  } else {
    current.push(algo);
  }
  emit('update:modelValue', current);
};
</script>
