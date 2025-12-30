<template>
  <div class="table-section bg-white rounded-lg border border-gray-200 shadow-none overflow-hidden">
    <div class="overflow-x-auto">
      <table class="min-w-max w-full divide-y divide-gray-200 whitespace-nowrap">
        <!-- Header -->
        <thead class="bg-gradient-to-r from-blue-50 to-yellow-50 sticky top-0 z-10">
          <tr>
            <th v-for="(header, index) in headers" :key="index"
              class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              <div class="flex items-center space-x-2">
                <div class="relative flex-1 flex items-center">
                  <input :value="header" @blur="$emit('update-header', index, $event.target.value)"
                    @keyup.enter="$emit('update-header', index, $event.target.value)"
                    :class="{ 'border-red-300': !header || header.trim() === '' }"
                    class="bg-transparent border-none outline-none w-full font-medium px-2 py-1 rounded focus:bg-blue-50 focus:ring-1 focus:ring-blue-300"
                    :placeholder="`Column ${index + 1}`" />
                  <div v-if="!header || header.trim() === ''" class="ml-2">
                    <div class="relative group">
                      <div class="w-4 h-4 bg-pink-400 rounded-full flex items-center justify-center cursor-help">
                        <span class="text-white text-xs font-bold">!</span>
                      </div>
                      <div class="absolute right-full top-1/2 -translate-y-1/2 mr-1 w-32 p-2 bg-pink-500 text-white text-xs rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-20 normal-case">
                        Required
                      </div>
                    </div>
                  </div>
                </div>
                <button @click="$emit('remove-column', index)"
                  class="text-red-500 hover:text-red-700 text-xs font-bold" title="Delete column">×</button>
              </div>
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <!-- Body -->
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(_, rowIndex) in (columnData[0] || [])" :key="rowIndex" class="hover:bg-gray-50 transition-colors">
            <td v-for="(header, colIndex) in headers" :key="colIndex" class="px-4 py-3 text-sm text-gray-900 relative">
              <div class="flex items-center">
                <input 
                  :value="getValidatedValue(columnData[colIndex]?.[rowIndex])"
                  @input="$emit('cell-input', rowIndex, colIndex, $event.target.value)"
                  @blur="$emit('cell-blur', rowIndex, colIndex, $event.target.value)"
                  class="w-full bg-transparent border-none outline-none px-2 py-1 rounded focus:bg-blue-50 focus:ring-1 focus:ring-blue-300"
                  :class="{ 'border-red-300': hasCellError(rowIndex, colIndex) }"
                  :placeholder="`Cell ${rowIndex + 1}-${colIndex + 1}`" />
                <div v-if="hasCellError(rowIndex, colIndex)" class="ml-2">
                  <div class="relative group">
                    <div class="w-4 h-4 bg-pink-400 rounded-full flex items-center justify-center cursor-help">
                      <span class="text-white text-xs font-bold">!</span>
                    </div>
                    <div class="absolute right-full top-1/2 -translate-y-1/2 mr-1 w-48 p-2 bg-pink-500 text-white text-xs rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-20 normal-case">
                      {{ getCellErrorMessage(rowIndex, colIndex) }}
                    </div>
                  </div>
                </div>
              </div>
            </td>
            <td class="px-4 py-3 text-sm text-gray-900">
              <button @click="$emit('remove-row', rowIndex)"
                class="text-red-600 hover:text-red-900 font-medium text-sm" title="Delete row">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div v-if="(columnData[0] || []).length === 0" class="text-center py-12 bg-gray-50">
      <div class="text-gray-500">
        <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No data available</h3>
        <p class="text-gray-500">Click "Add Row" to start creating your data table</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  headers: { type: Array, required: true },
  columnData: { type: Array, required: true },
  cellErrors: { type: Object, default: () => ({}) }
});

defineEmits(['update-header', 'remove-column', 'remove-row', 'cell-input', 'cell-blur']);

const getValidatedValue = (value) => value !== null && value !== undefined ? String(value) : '';

const hasCellError = (rowIndex, colIndex) => {
  const header = props.headers[colIndex];
  const key = `${rowIndex}-${header}`;
  return props.cellErrors[key] || false;
};

const getCellErrorMessage = (rowIndex, colIndex) => {
  const value = props.columnData[colIndex]?.[rowIndex] || '';
  const header = props.headers[colIndex] || '';
  
  if (value === null || value === undefined || value.trim() === '') return 'Required';
  if (colIndex === 0) return '';
  
  const headerLower = header.toLowerCase();
  if (headerLower.includes('depend') || headerLower.includes('prerequisite')) {
    const trimmed = value.trim();
    if (!/^(\d+([;,]\d+)*|none|null|0)$/i.test(trimmed)) return 'Use format: 0, 1;2, 1,2 or "none"';
    return '';
  }
  
  if (!/^-?(?:\d+(?:\.\d*)?|\.\d+)$/.test(value.trim())) return 'Must be a number';
  return '';
};
</script>
