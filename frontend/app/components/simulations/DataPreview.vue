<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-none p-6 mb-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-medium text-gray-900">Data Preview</h3>
      <button @click="$emit('edit-data')"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
        Edit
      </button>
    </div>
    
    <div v-if="!filteredTasks || filteredTasks.length === 0" class="text-center py-8 text-gray-500">
      <svg class="w-12 h-12 mx-auto mb-2 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM4.332 8.027a6.012 6.012 0 011.912-2.706C6.512 5.73 6.974 6 7.5 6A1.5 1.5 0 019 7.5V8a2 2 0 004 0 2 2 0 011.523-1.943A5.522 5.522 0 0016 10c0 .973-.325 1.875-.923 2.627A5.994 5.994 0 0110 16c-1.567 0-3.02-.529-4.191-1.425a6.012 6.012 0 01-1.912-2.706z" clip-rule="evenodd" />
      </svg>
      <p>No data available</p>
    </div>
    
    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th v-for="header in datasetHeaders" :key="header"
              class="px-4 py-2 text-left text-xs font-medium text-gray-500 tracking-wider">
              {{ header }}
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(task, index) in filteredTasks.slice(0, 5)" :key="index" class="hover:bg-gray-50">
            <td v-for="header in datasetHeaders" :key="header"
              class="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
              {{ task[header] }}
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="filteredTasks.length > 5" class="text-center py-2 text-sm text-gray-500">
        Showing first 5 of {{ filteredTasks.length }} rows
      </div>
    </div>

    <!-- Data Filtering Controls -->
    <div v-if="totalTasks > 10" class="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <h4 class="text-sm font-medium text-gray-700 mb-3">Filter Data for Simulation</h4>
      <div class="flex flex-wrap gap-4 items-start">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 mb-2">Limit Data Rows</label>
          <input
            :value="dataLimit"
            @input="$emit('update:dataLimit', Math.max(1, Math.min(totalTasks, parseInt($event.target.value) || 1)))"
            type="number" :min="1" :max="totalTasks"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter number of rows"
          />
          <p class="text-xs text-gray-500 mt-1">Showing {{ previewCount }} of {{ totalTasks }} rows</p>
        </div>
        <div class="flex items-center pt-7">
          <label class="flex items-center cursor-pointer whitespace-nowrap">
            <input :checked="showAllData" @change="$emit('update:showAllData', $event.target.checked)"
              type="checkbox" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500" />
            <span class="ml-2 text-sm text-gray-700">Select all data</span>
          </label>
        </div>
        <div class="text-sm text-gray-600 pt-7">
          <p>Preview: {{ previewCount }} rows</p>
          <p class="text-xs">This affects simulation input only</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  tasks: { type: Array, required: true },
  datasetHeaders: { type: Array, required: true },
  dataLimit: { type: Number, required: true },
  showAllData: { type: Boolean, default: false }
});

defineEmits(['edit-data', 'update:dataLimit', 'update:showAllData']);

const totalTasks = computed(() => props.tasks?.length || 0);

const filteredTasks = computed(() => {
  if (!props.tasks || !Array.isArray(props.tasks) || props.tasks.length === 0) return [];
  if (props.showAllData) return props.tasks;
  const actualLimit = Math.min(Math.max(1, props.dataLimit), props.tasks.length);
  return props.tasks.slice(0, actualLimit);
});

const previewCount = computed(() => {
  if (!props.tasks || props.tasks.length === 0) return 0;
  if (props.showAllData) return props.tasks.length;
  return Math.max(1, Math.min(props.dataLimit, props.tasks.length));
});
</script>
