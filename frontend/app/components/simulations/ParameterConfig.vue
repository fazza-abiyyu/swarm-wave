<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-none p-6 mb-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-6">Algorithm Parameters</h2>

    <!-- Common Parameters -->
    <div class="mb-8">
      <h3 class="text-lg font-medium text-gray-800 mb-4">Common Parameters</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Number of Agents -->
        <div>
          <div class="flex items-center gap-1 mb-2">
            <label class="block text-sm font-medium text-gray-700">Number of Agents</label>
            <span class="relative group cursor-pointer text-gray-400 text-xs font-bold">?
              <div class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10">
                Number of worker agents (ants or particles) that will process tasks simultaneously. Range: 1-10.
              </div>
            </span>
          </div>
          <input v-model.number="localParams.num_default_agents" type="number" min="1" max="10"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
        </div>

        <!-- Iterations -->
        <div>
          <div class="flex items-center gap-1 mb-2">
            <label class="block text-sm font-medium text-gray-700">Iterations</label>
            <span class="relative group cursor-pointer text-gray-400 text-xs font-bold">?
              <div class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10">
                Total number of optimization cycles. Range: 1-100.
              </div>
            </span>
          </div>
          <input v-model.number="localParams.n_iterations" type="number" min="1" max="100"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
        </div>

        <!-- Task ID Column -->
        <div>
          <div class="flex items-center gap-1 mb-2">
            <label class="block text-sm font-medium text-gray-700">Task ID Column</label>
            <span v-if="localParams.task_id_col === datasetHeaders[0] && datasetHeaders.length > 0" 
              class="px-2 py-1 text-xs bg-blue-100 text-blue-600 rounded-md">Auto-selected</span>
          </div>
          <select v-model="localParams.task_id_col"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option v-if="datasetHeaders.length === 0" value="" disabled>No columns available</option>
            <option v-for="header in datasetHeaders" :key="header" :value="header">{{ header }}</option>
          </select>
        </div>

        <!-- Dependencies Column -->
        <div>
          <div class="flex items-center gap-1 mb-2">
            <label class="block text-sm font-medium text-gray-700">Dependencies Column</label>
            <span v-if="localParams.enable_dependencies" class="px-2 py-1 text-xs bg-green-100 text-green-600 rounded-md">Enabled</span>
          </div>
          <select v-model="localParams.dependency_col"
            @change="localParams.enable_dependencies = localParams.dependency_col !== ''"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option value="">None (No Dependencies)</option>
            <option v-for="header in datasetHeaders" :key="header" :value="header">{{ header }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Algorithm-Specific Parameters -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- ACO Parameters -->
      <template v-if="selectedAlgorithms.includes('ACO')">
        <div>
          <h3 class="text-lg font-medium text-gray-800 mb-4">ACO Parameters</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <div class="flex items-center gap-1 mb-2">
                <label class="block text-sm font-medium text-gray-700">Alpha (Pheromone)</label>
              </div>
              <input v-model.number="localParams.alpha" type="number" step="0.1" min="0" max="5"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Beta (Heuristic)</label>
              <input v-model.number="localParams.beta" type="number" step="0.1" min="0" max="5"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Evaporation Rate</label>
              <input v-model.number="localParams.evaporation_rate" type="number" step="0.1" min="0" max="1"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Pheromone Deposit</label>
              <input v-model.number="localParams.pheromone_deposit" type="number" step="1" min="1" max="500"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Number of Ants</label>
              <input v-model.number="localParams.n_ants" type="number" min="1" max="100"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
          </div>
        </div>
      </template>

      <!-- PSO Parameters -->
      <template v-if="selectedAlgorithms.includes('PSO')">
        <div>
          <h3 class="text-lg font-medium text-gray-800 mb-4">PSO Parameters</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Particles</label>
              <input v-model.number="localParams.n_particles" type="number" min="1" max="100"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Inertia (w)</label>
              <input v-model.number="localParams.w" type="number" step="0.1" min="0" max="1"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Cognitive (c1)</label>
              <input v-model.number="localParams.c1" type="number" step="0.1" min="0" max="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Social (c2)</label>
              <input v-model.number="localParams.c2" type="number" step="0.1" min="0" max="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- Action Buttons -->
    <div class="mt-6 flex gap-3">
      <button @click="$emit('run-simulation')"
        :disabled="isRunning || selectedAlgorithms.length === 0 || !dataValidation.isValid || filteredTasksLength === 0"
        class="flex-1 md:flex-none px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors">
        <span v-if="isRunning">Running...</span>
        <span v-else-if="filteredTasksLength === 0">No Data Available</span>
        <span v-else-if="!dataValidation.isValid">Invalid Data</span>
        <span v-else>{{ `Run ${selectedAlgorithms.join(" & ")} Simulation` }}</span>
      </button>
      <button v-if="isRunning" @click="$emit('stop-simulation')"
        class="px-6 py-3 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><rect x="6" y="6" width="8" height="8" rx="1" /></svg>
        Stop
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue';

const props = defineProps({
  parameters: { type: Object, required: true },
  selectedAlgorithms: { type: Array, default: () => [] },
  datasetHeaders: { type: Array, default: () => [] },
  isRunning: { type: Boolean, default: false },
  dataValidation: { type: Object, default: () => ({ isValid: true }) },
  filteredTasksLength: { type: Number, default: 0 }
});

const emit = defineEmits(['update:parameters', 'run-simulation', 'stop-simulation']);

const localParams = reactive({ ...props.parameters });

watch(localParams, (newVal) => {
  emit('update:parameters', { ...newVal });
}, { deep: true });

watch(() => props.parameters, (newVal) => {
  Object.assign(localParams, newVal);
}, { deep: true });
</script>
