<template>
  <div class="controls-section mb-6 bg-white rounded-lg border border-gray-200 shadow-none p-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
      <!-- Modify Group -->
      <div class="space-y-2">
        <span class="text-xs font-medium text-gray-500 uppercase tracking-wider block text-center">Modify</span>
        <div class="grid grid-cols-2 gap-2">
          <button @click="$emit('add-row')"
            class="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
            Add Row
          </button>
          <button @click="$emit('add-column')"
            class="px-3 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
            Add Col
          </button>
        </div>
      </div>
      
      <!-- Import Group -->
      <div class="space-y-2">
        <span class="text-xs font-medium text-gray-500 uppercase tracking-wider block text-center">Import</span>
        <div class="grid grid-cols-2 gap-2">
          <button @click="$emit('import-json')"
            class="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
            JSON
          </button>
          <button @click="$emit('import-csv')"
            class="px-3 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
            CSV
          </button>
        </div>
      </div>
      
      <!-- Export Group -->
      <div class="space-y-2">
        <span class="text-xs font-medium text-gray-500 uppercase tracking-wider block text-center">Export</span>
        <div class="grid grid-cols-2 gap-2">
          <button @click="$emit('export-json')"
            class="px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
            JSON
          </button>
          <button @click="$emit('export-csv')"
            class="px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
            CSV
          </button>
        </div>
      </div>
      
      <!-- Tools Group -->
      <div class="space-y-2">
        <span class="text-xs font-medium text-gray-500 uppercase tracking-wider block text-center">Tools</span>
        <div class="grid grid-cols-1 gap-2">
          <button @click="$emit('toggle-json')"
            class="px-3 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
            {{ showJsonEditor ? 'Hide' : 'Show' }} JSON
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  showJsonEditor: { type: Boolean, default: false }
});

defineEmits(['add-row', 'add-column', 'import-json', 'import-csv', 'export-json', 'export-csv', 'toggle-json']);
</script>
