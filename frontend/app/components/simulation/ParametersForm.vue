<template>
  <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
    <h2 class="text-2xl font-bold mb-4 text-gray-800">⚙️ Algorithm Parameters</h2>
    
    <!-- Common Parameters -->
    <div class="mb-6">
      <h3 class="text-lg font-semibold mb-3 text-gray-700">Common Parameters</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Default Agents</label>
          <input
            v-model.number="localParams.num_default_agents"
            type="number"
            min="1"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Iterations</label>
          <input
            v-model.number="localParams.n_iterations"
            type="number"
            min="1"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Random Seed</label>
          <input
            v-model.number="localParams.random_seed"
            type="number"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Task ID Column</label>
          <select
            v-model="localParams.task_id_col"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select column</option>
            <option v-for="header in headers" :key="header" :value="header">
              {{ header }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Agent ID Column (Optional)</label>
          <select
            v-model="localParams.agent_id_col"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select column</option>
            <option v-for="header in headers" :key="header" :value="header">
              {{ header }}
            </option>
          </select>
        </div>
      </div>
    </div>
    
    <!-- Dependencies -->
    <div class="mb-6">
      <div class="flex items-center mb-3">
        <input
          v-model="localParams.enable_dependencies"
          type="checkbox"
          class="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
        />
        <label class="ml-2 text-sm font-medium text-gray-700">
          Enable Task Dependencies
        </label>
      </div>
      
      <div v-if="localParams.enable_dependencies">
        <label class="block text-sm font-medium text-gray-700 mb-1">Dependency Column</label>
        <select
          v-model="localParams.dependency_col"
          class="w-full md:w-1/3 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select column</option>
          <option v-for="header in headers" :key="header" :value="header">
            {{ header }}
          </option>
        </select>
      </div>
    </div>
    
    <!-- ACO Parameters -->
    <div v-if="selectedAlgorithms.includes('ACO')" class="mb-6">
      <h3 class="text-lg font-semibold mb-3 text-blue-700">ACO Parameters</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Number of Ants</label>
          <input
            v-model.number="localParams.n_ants"
            type="number"
            min="1"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Alpha (α)</label>
          <input
            v-model.number="localParams.alpha"
            type="number"
            step="0.1"
            min="0"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Beta (β)</label>
          <input
            v-model.number="localParams.beta"
            type="number"
            step="0.1"
            min="0"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Evaporation Rate</label>
          <input
            v-model.number="localParams.evaporation_rate"
            type="number"
            step="0.1"
            min="0"
            max="1"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Pheromone Deposit</label>
          <input
            v-model.number="localParams.pheromone_deposit"
            type="number"
            step="10"
            min="0"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
    </div>
    
    <!-- PSO Parameters -->
    <div v-if="selectedAlgorithms.includes('PSO')" class="mb-6">
      <h3 class="text-lg font-semibold mb-3 text-red-700">PSO Parameters</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Number of Particles</label>
          <input
            v-model.number="localParams.n_particles"
            type="number"
            min="1"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Inertia Weight (w)</label>
          <input
            v-model.number="localParams.w"
            type="number"
            step="0.1"
            min="0"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Cognitive Coefficient (c1)</label>
          <input
            v-model.number="localParams.c1"
            type="number"
            step="0.1"
            min="0"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Social Coefficient (c2)</label>
          <input
            v-model.number="localParams.c2"
            type="number"
            step="0.1"
            min="0"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue';

const props = defineProps({
  parameters: { type: Object, required: true },
  headers: { type: Array, required: true },
  selectedAlgorithms: { type: Array, required: true }
});

const emit = defineEmits(['update:parameters']);

const localParams = reactive({ ...props.parameters });

watch(localParams, (newParams) => {
  emit('update:parameters', { ...newParams });
}, { deep: true });

watch(() => props.parameters, (newParams) => {
  Object.assign(localParams, newParams);
}, { deep: true });
</script>
