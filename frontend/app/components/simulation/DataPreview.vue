<template>
  <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
    <h2 class="text-2xl font-bold mb-4 text-gray-800">📊 Data Preview</h2>
    
    <div class="mb-4 flex flex-wrap gap-4 items-end">
      <div class="flex-1 min-w-[200px]">
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Preview Limit
        </label>
        <input
          :value="limit"
          @input="$emit('update:limit', parseInt($event.target.value) || 1)"
          @blur="validateLimit"
          type="number"
          min="1"
          :max="maxLimit"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      
      <button
        @click="$emit('update:showAll', !showAll)"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        {{ showAll ? 'Show Limited' : 'Show All' }} ({{ totalTasks }} tasks)
      </button>
    </div>

    <div class="overflow-x-auto">
      <DynamicTable :data="displayData" :maxHeight="400" />
    </div>
    
    <p class="text-sm text-gray-600 mt-2">
      Showing {{ displayCount }} of {{ totalTasks }} tasks
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  tasks: { type: Array, required: true },
  limit: { type: Number, required: true },
  showAll: { type: Boolean, required: true }
});

const emit = defineEmits(['update:limit', 'update:showAll']);

const maxLimit = computed(() => props.tasks.length);

const displayData = computed(() => {
  if (props.showAll) {
    return props.tasks;
  }
  const actualLimit = Math.min(Math.max(1, props.limit), props.tasks.length);
  return props.tasks.slice(0, actualLimit);
});

const displayCount = computed(() => displayData.value.length);
const totalTasks = computed(() => props.tasks.length);

const validateLimit = () => {
  if (props.limit <= 0) {
    emit('update:limit', 1);
  } else if (props.limit > props.tasks.length) {
    emit('update:limit', props.tasks.length);
  }
};
</script>
