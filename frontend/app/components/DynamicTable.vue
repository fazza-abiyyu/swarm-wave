<template>
    <div class="dynamic-table-container p-4">
        <!-- Error Message -->
        <div v-if="jsonError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <p class="text-red-600 text-sm">Invalid JSON format</p>
        </div>

        <!-- Controls Section -->
        <div class="controls-section mb-6 bg-white rounded-lg shadow-md p-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                <!-- Data Modification Group -->
                <div class="space-y-2">
                    <span class="text-xs font-medium text-gray-500 uppercase tracking-wider block text-center">Modify</span>
                    <div class="grid grid-cols-2 gap-2">
                        <button @click="addRow"
                            class="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
                            Add Row
                        </button>
                        <button @click="addColumn"
                            class="px-3 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
                            Add Col
                        </button>
                    </div>
                </div>
                
                <!-- Import Group -->
                <div class="space-y-2">
                    <span class="text-xs font-medium text-gray-500 uppercase tracking-wider block text-center">Import</span>
                    <div class="grid grid-cols-2 gap-2">
                        <button @click="importJson"
                            class="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
                            JSON
                        </button>
                        <button @click="importCsv"
                            class="px-3 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
                            CSV
                        </button>
                    </div>
                </div>
                
                <!-- Export Group -->
                <div class="space-y-2">
                    <span class="text-xs font-medium text-gray-500 uppercase tracking-wider block text-center">Export</span>
                    <div class="grid grid-cols-2 gap-2">
                        <button @click="exportJson"
                            class="px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
                            JSON
                        </button>
                        <button @click="exportCsv"
                            class="px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
                            CSV
                        </button>
                    </div>
                </div>
                
                <!-- Utility Group -->
                <div class="space-y-2">
                    <span class="text-xs font-medium text-gray-500 uppercase tracking-wider block text-center">Tools</span>
                    <div class="grid grid-cols-1 gap-2">
                        <button @click="toggleJsonEditor"
                            class="px-3 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm font-medium w-full h-10 flex items-center justify-center">
                            {{ showJsonEditor ? 'Hide' : 'Show' }} JSON
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- JSON Input Section (Collapsible) -->
        <div v-if="showJsonEditor"
            class="json-section mb-6 bg-white rounded-lg shadow-md p-4 transition-all duration-300">
            <div class="flex justify-between items-center mb-2">
                <label class="block text-sm font-medium text-gray-700">
                    JSON Input
                </label>
                <button @click="loadSampleData" class="text-sm text-blue-600 hover:text-blue-800 font-medium">
                Load Sample Data (Any Domain)
            </button>
            </div>
            <textarea v-model="jsonInput" @input="updateFromJson"
                class="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                placeholder='// Any dataset structure supported:
// Manufacturing: [{"Job_ID":1,"Processing_Time":45,"Setup_Time":5,"Material_Cost":250,"Priority":3}]
// Logistics: [{"Order_ID":1,"Distance_km":250,"Weight_kg":1500,"Urgency":4,"Fuel_Cost":180}]
// Finance: [{"Investment_ID":1,"Amount":50000,"Risk_Score":7.5,"Expected_Return":12.5}]
// Healthcare: [{"Patient_ID":1,"Age":45,"Treatment_Duration":14,"Medication_Cost":2500}]'></textarea>
        </div>

        <!-- Dynamic Table -->
        <div class="table-section bg-white rounded-lg shadow-md overflow-hidden">
            <!-- Responsive Table Container -->
            <div class="overflow-x-auto">
                <table class="min-w-max w-full divide-y divide-gray-200 whitespace-nowrap">
                    <!-- Sticky Table Header -->
                    <thead class="bg-gradient-to-r from-blue-50 to-yellow-50 sticky top-0 z-10">
                        <tr>
                            <th v-for="(header, index) in headers" :key="index"
                                class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                                <div class="flex items-center space-x-2">
                                    <div class="relative flex-1 flex items-center">
                                        <input v-model="headers[index]" @blur="updateHeader(index, headers[index])"
                                            @keyup.enter="updateHeader(index, headers[index])"
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
                                    <button @click="removeColumn(index)"
                                        class="text-red-500 hover:text-red-700 text-xs font-bold" title="Delete column">
                                        ×
                                    </button>
                                </div>
                            </th>
                            <th class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <!-- Table Body -->
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="(_, rowIndex) in (columnData[0] || [])" :key="rowIndex"
                            class="hover:bg-gray-50 transition-colors">
                            <td v-for="(header, colIndex) in headers" :key="colIndex"
                                class="px-4 py-3 text-sm text-gray-900 relative">
                                <div class="flex items-center">
                                    <input 
                                        :value="getValidatedValue(columnData[colIndex]?.[rowIndex])"
                                        @input="handleCellInput(rowIndex, colIndex, $event.target.value)"
                                        @blur="validateAndUpdateCell(rowIndex, colIndex, $event.target.value)"
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
                                <button @click="removeRow(rowIndex)"
                                    class="text-red-600 hover:text-red-900 font-medium text-sm" title="Delete row">
                                    Delete
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Empty State -->
            <div v-if="(columnData[0] || []).length === 0" class="text-center py-12 bg-gray-50">
                <div class="text-gray-500">
                    <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
                    </svg>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">No data available</h3>
                    <p class="text-gray-500">Click "Add Row" to start creating your data table</p>
                </div>
            </div>
        </div>

        <!-- Simulation Button -->
        <div class="simulation-section mt-6 text-center">
            <button ref="simulationButton" @click="openSimulationModal"
                :disabled="!isTableValid"
                class="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed"
                :class="{ 'opacity-50 cursor-not-allowed': !isTableValid }">
                {{ isTableValid ? 'Run Simulation' : 'Please Correct the Input' }}
            </button>
        </div>

        <!-- Floating Scroll Button -->
        <transition enter-active-class="transform ease-out duration-300 transition"
            enter-from-class="translate-y-2 opacity-0"
            enter-to-class="translate-y-0 opacity-100"
            leave-active-class="transform ease-in duration-200 transition"
            leave-from-class="translate-y-0 opacity-100"
            leave-to-class="translate-y-2 opacity-0">
            <button v-if="showFloatingButton"
                @click="scrollToSimulationButton"
                class="fixed bottom-6 right-6 z-40 p-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full shadow-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 transform hover:scale-110"
                style="transform: translateX(-50%);">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                </svg>
            </button>
        </transition>

        <!-- Simulation Modal -->
        <div v-if="showSimulationModal"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold text-gray-900">
                        Swarm Intelligence Simulation
                    </h3>
                    <button @click="closeSimulationModal" class="text-gray-400 hover:text-gray-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>

                <div class="space-y-4">
                    <p class="text-sm text-gray-600">Select algorithms to run on your current table data:</p>

                    <div class="space-y-3">
                        <label class="flex items-center space-x-3">
                            <input type="checkbox" v-model="selectedAlgorithms" value="ACO"
                                class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                            <div>
                                <span class="text-sm font-medium text-gray-700">Ant Colony Optimization (ACO)</span>
                                <p class="text-xs text-gray-500">Mimics ant foraging behavior</p>
                            </div>
                        </label>

                        <label class="flex items-center space-x-3">
                            <input type="checkbox" v-model="selectedAlgorithms" value="PSO"
                                class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                            <div>
                                <span class="text-sm font-medium text-gray-700">Particle Swarm Optimization (PSO)</span>
                                <p class="text-xs text-gray-500">Models bird flocking behavior</p>
                            </div>
                        </label>
                    </div>

                    <div class="flex space-x-3 pt-4">
                        <button @click="runSimulation"
                            class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium">
                            Run Simulation
                        </button>
                        <button @click="closeSimulationModal"
                            class="flex-1 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors font-medium">
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Delete Row Confirmation Modal -->
        <div v-if="showDeleteRowModal"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-6 max-w-sm w-full mx-4">
                <h3 class="text-lg font-semibold text-gray-900 mb-2">Confirm Delete</h3>
                <p class="text-sm text-gray-600 mb-4">Are you sure you want to delete this row? This action cannot be undone.</p>
                <div class="flex space-x-3">
                    <button @click="confirmDeleteRow"
                        class="flex-1 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors font-medium">
                        Delete
                    </button>
                    <button @click="showDeleteRowModal = false"
                        class="flex-1 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors font-medium">
                        Cancel
                    </button>
                </div>
            </div>
        </div>

        <!-- Delete Column Confirmation Modal -->
        <div v-if="showDeleteColumnModal"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-6 max-w-sm w-full mx-4">
                <h3 class="text-lg font-semibold text-gray-900 mb-2">Confirm Delete</h3>
                <p class="text-sm text-gray-600 mb-4">Are you sure you want to delete this column? This action cannot be undone.</p>
                <div class="flex space-x-3">
                    <button @click="confirmDeleteColumn"
                        class="flex-1 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors font-medium">
                        Delete
                    </button>
                    <button @click="showDeleteColumnModal = false"
                        class="flex-1 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors font-medium">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>
    <!-- Toast Notification -->
    <transition enter-active-class="transform ease-out duration-300 transition"
        enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
        enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
        leave-active-class="transform ease-in duration-200 transition"
        leave-from-class="translate-y-0 opacity-100 sm:translate-x-0"
        leave-to-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2">
        <div v-if="showToast" class="fixed top-4 right-4 z-50">
            <div class="bg-white shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 overflow-hidden">
                <div class="p-4">
                    <div class="flex items-center">
                        <div class="flex-shrink-0">
                            <svg class="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm font-medium text-gray-900">{{ toastMessage }}</p>
                        </div>
                        <div class="ml-auto pl-3">
                            <button @click="showToast = false" class="inline-flex text-gray-400 hover:text-gray-500">
                                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M6 18L18 6M6 6l12 12"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'

// Props and Emits
const props = defineProps({
  initialData: {
    type: Array,
    default: () => []
  }
})
const emit = defineEmits(['data-updated', 'run-simulation'])

// Reactive data
const headers = ref(['TaskID', 'Weight', 'Duration', 'Cost'])
const cellErrors = ref({}) // Track validation errors for individual cells

// Store data by column index instead of header name
const columnData = ref([])

// Initialize data from props
const initializeData = () => {
  if (props.initialData && props.initialData.length > 0) {
    const initialTableData = props.initialData.map(row => 
      Object.fromEntries(Object.entries(row).map(([key, value]) => [key, String(value)])));
    headers.value = Object.keys(props.initialData[0]);
    // Convert to column-based structure
    columnData.value = headers.value.map(header => 
      initialTableData.map(row => row[header] || '')
    );
  } else {
    // Default sample data
    const defaultData = [
      { TaskID: '1', Weight: '10', Duration: '25', Cost: '100' },
      { TaskID: '2', Weight: '15', Duration: '30', Cost: '150' },
      { TaskID: '3', Weight: '8', Duration: '20', Cost: '80' }
    ]
    headers.value = Object.keys(defaultData[0]);
    columnData.value = headers.value.map(header => 
      defaultData.map(row => row[header] || '')
    );
  }
  
  validateAllCells()
}





const jsonInput = ref('')
const jsonError = ref(false)
const showJsonEditor = ref(false)
const showSimulationModal = ref(false)
const selectedAlgorithms = ref([])
const toastMessage = ref('')
const showToast = ref(false)
const showDeleteRowModal = ref(false)
const showDeleteColumnModal = ref(false)
const pendingDeleteRowIndex = ref(null)
const pendingDeleteColumnIndex = ref(null)
const currentDatasetIndex = ref(0)
const simulationButton = ref(null)
const showFloatingButton = ref(false)

// Validation
const validationErrors = computed(() => {
  const errors = []
  
  // Check for empty headers
  headers.value.forEach((header, index) => {
    if (!header || header.trim() === '') {
      errors.push(`Column ${index + 1} header is required`)
    }
  })
  
  // Check for empty cells
  headers.value.forEach((header, colIndex) => {
    columnData.value[colIndex]?.forEach((value, rowIndex) => {
      if (!value || value.trim() === '') {
        errors.push(`Row ${rowIndex + 1}, Column "${header}" is empty`)
      }
    })
  })

  // Check for non-numeric values
headers.value.forEach((header, colIndex) => {
    columnData.value[colIndex]?.forEach((value, rowIndex) => {
      const trimmed = typeof value === 'string' ? value.trim() : String(value ?? '')
      if (!trimmed) return

      // Hanya gunakan satu regex validation yang kuat
      if (!/^-?(?:\d+(?:\.\d*)?|\.\d+)$/.test(trimmed)) {
    errors.push(`Row ${rowIndex + 1}, Column "${header}" must be a number`)
    return
  }
    })
  })


  return errors
})

const getTableData = () => {
  return Array.from({ length: columnData.value[0]?.length || 0 }, (_, rowIndex) => {
    const row = {}
    headers.value.forEach((header, colIndex) => {
      row[header] = columnData.value[colIndex]?.[rowIndex] || ''
    })
    return row
  })
}

const isTableValid = computed(() => {
  return validationErrors.value.length === 0 && (columnData.value[0]?.length || 0) > 0
})

// Validation functions
const validateCell = (value, header = '') => {
  if (value === null || value === undefined) return false
  if (typeof value !== 'string') return false
  if (value.trim() === '') return false
  
  // All columns must be numeric
  if (!/^-?(?:\d+(?:\.\d*)?|\.\d+)$/.test(value.trim())) return false
  
  return true
}

const getValidatedValue = (value) => {
  return value !== null && value !== undefined ? String(value) : ''
}

const hasCellError = (rowIndex, colIndex) => {
  const header = headers.value[colIndex]
  const key = `${rowIndex}-${header}`
  return cellErrors.value[key] || false
}

const getCellErrorMessage = (rowIndex, colIndex) => {
  const value = columnData.value[colIndex]?.[rowIndex] || ''
  if (value === null || value === undefined || value.trim() === '') return 'Required'
  
  // All columns must be numeric
  if (!/^-?(?:\d+(?:\.\d*)?|\.\d+)$/.test(value.trim())) return 'Must be a number'
  
  return ''
}

const validateAndUpdateCell = (rowIndex, colIndex, value) => {
  const header = headers.value[colIndex]
  const key = `${rowIndex}-${header}`
  
  // Ensure string type and validate
  const stringValue = String(value)
  
  // Validate - reject non-string inputs, empty strings, and invalid content
  if (typeof value !== 'string' || !validateCell(stringValue, header)) {
    cellErrors.value[key] = true
  } else {
    delete cellErrors.value[key]
  }
  
  // Update the actual data
  if (columnData.value[colIndex]) {
    columnData.value[colIndex][rowIndex] = stringValue
    emit('data-updated', getTableData())
  }
}

const handleCellInput = (rowIndex, colIndex, value) => {
  const header = headers.value[colIndex]
  
  // Real-time validation feedback - reject non-string inputs
  if (typeof value !== 'string') {
    const key = `${rowIndex}-${header}`
    cellErrors.value[key] = true
    return
  }
  
  const stringValue = String(value)
  const key = `${rowIndex}-${header}`
  
  // Validate content based on column type
  if (!validateCell(stringValue, header)) {
    cellErrors.value[key] = true
  } else {
    delete cellErrors.value[key]
  }
  
  // Update immediately but don't emit yet (wait for blur)
  if (colIndex >= 0 && columnData.value[colIndex]) {
    columnData.value[colIndex][rowIndex] = stringValue
  }
}

const validateAllCells = () => {
  cellErrors.value = {}
  headers.value.forEach((header, colIndex) => {
    columnData.value[colIndex]?.forEach((value, rowIndex) => {
      if (!validateCell(value, header)) {
        const key = `${rowIndex}-${header}`
        cellErrors.value[key] = true
      }
    })
  })
}

// Generic sample datasets for different domains
const sampleDatasets = {
    cloud: [
        {"Task_ID": "1", "CPU_Usage (%)": "37", "RAM_Usage (MB)": "2612", "Disk_IO (MB/s)": "55", "Network_IO (MB/s)": "40", "Priority": "2", "VM_ID": "107", "Execution_Time (s)": "1.27", "Target": "1"},
        {"Task_ID": "2", "CPU_Usage (%)": "86", "RAM_Usage (MB)": "11761", "Disk_IO (MB/s)": "120", "Network_IO (MB/s)": "85", "Priority": "5", "VM_ID": "108", "Execution_Time (s)": "3.71", "Target": "1"},
        {"Task_ID": "3", "CPU_Usage (%)": "44", "RAM_Usage (MB)": "4610", "Disk_IO (MB/s)": "65", "Network_IO (MB/s)": "25", "Priority": "3", "VM_ID": "109", "Execution_Time (s)": "8.53", "Target": "1"}
    ],
    manufacturing: [
        {"Job_ID": "1", "Processing_Time": "45", "Setup_Time": "5", "Material_Cost": "250", "Labor_Hours": "8", "Priority": "3", "Deadline": "120", "Quality_Score": "95"},
        {"Job_ID": "2", "Processing_Time": "120", "Setup_Time": "15", "Material_Cost": "800", "Labor_Hours": "20", "Priority": "5", "Deadline": "200", "Quality_Score": "88"},
        {"Job_ID": "3", "Processing_Time": "30", "Setup_Time": "2", "Material_Cost": "150", "Labor_Hours": "4", "Priority": "2", "Deadline": "72", "Quality_Score": "92"}
    ],
    logistics: [
        {"Order_ID": "1", "Distance_km": "250", "Weight_kg": "1500", "Volume_m3": "8.5", "Urgency": "4", "Fuel_Cost": "180", "Delivery_Time": "4.2", "Customer_Rating": "4.8", "Priority": "3"},
        {"Order_ID": "2", "Distance_km": "800", "Weight_kg": "3500", "Volume_m3": "15.2", "Urgency": "5", "Fuel_Cost": "420", "Delivery_Time": "12.5", "Customer_Rating": "4.2", "Priority": "5"},
        {"Order_ID": "3", "Distance_km": "120", "Weight_kg": "800", "Volume_m3": "4.1", "Urgency": "2", "Fuel_Cost": "95", "Delivery_Time": "2.1", "Customer_Rating": "4.9", "Priority": "2"}
    ],
    finance: [
        {"Investment_ID": "1", "Amount": "50000", "Risk_Score": "7.5", "Expected_Return": "12.5", "Duration_Months": "24", "Market_Volatility": "15.2", "Liquidity": "8.5", "Priority": "4"},
        {"Investment_ID": "2", "Amount": "75000", "Risk_Score": "4.2", "Expected_Return": "8.8", "Duration_Months": "12", "Market_Volatility": "8.7", "Liquidity": "9.2", "Priority": "3"},
        {"Investment_ID": "3", "Amount": "30000", "Risk_Score": "9.8", "Expected_Return": "18.5", "Duration_Months": "36", "Market_Volatility": "22.3", "Liquidity": "6.8", "Priority": "5"}
    ],
    healthcare: [
        {"Patient_ID": "1", "Age": "45", "Treatment_Duration": "14", "Medication_Cost": "2500", "Severity": "3", "Insurance_Coverage": "0.8", "Recovery_Rate": "0.85", "Risk_Factor": "2.1", "Priority": "2"},
        {"Patient_ID": "2", "Age": "67", "Treatment_Duration": "28", "Medication_Cost": "7500", "Severity": "5", "Insurance_Coverage": "0.9", "Recovery_Rate": "0.65", "Risk_Factor": "4.2", "Priority": "5"},
        {"Patient_ID": "3", "Age": "34", "Treatment_Duration": "7", "Medication_Cost": "1200", "Severity": "2", "Insurance_Coverage": "0.7", "Recovery_Rate": "0.95", "Risk_Factor": "1.3", "Priority": "1"}
    ]
}

// Methods
const addRow = () => {
  headers.value.forEach((_, colIndex) => {
    if (!columnData.value[colIndex]) {
      columnData.value[colIndex] = []
    }
    columnData.value[colIndex].push('')
  })
  validateAllCells()
  emit('data-updated', getTableData())
  showToastMessage('Row added successfully')
}

const addColumn = () => {
  const newHeader = `Column${headers.value.length + 1}`
  headers.value.push(newHeader)
  columnData.value.push(Array(columnData.value[0]?.length || 0).fill(''))
  validateAllCells()
  emit('data-updated', getTableData())
  showToastMessage('Column added successfully')
}

const removeRow = (index) => {
  pendingDeleteRowIndex.value = index
  showDeleteRowModal.value = true
}

const removeColumn = (index) => {
  pendingDeleteColumnIndex.value = index
  showDeleteColumnModal.value = true
}

const confirmDeleteRow = () => {
  if (pendingDeleteRowIndex.value !== null) {
    headers.value.forEach((_, colIndex) => {
      columnData.value[colIndex].splice(pendingDeleteRowIndex.value, 1)
    })
    validateAllCells()
    emit('data-updated', getTableData())
    showToastMessage('Row deleted successfully')
  }
  showDeleteRowModal.value = false
  pendingDeleteRowIndex.value = null
}

const confirmDeleteColumn = () => {
  if (pendingDeleteColumnIndex.value !== null) {
    headers.value.splice(pendingDeleteColumnIndex.value, 1)
    columnData.value.splice(pendingDeleteColumnIndex.value, 1)
    validateAllCells()
    emit('data-updated', getTableData())
    showToastMessage('Column deleted successfully')
  }
  showDeleteColumnModal.value = false
  pendingDeleteColumnIndex.value = null
}

const updateHeader = (index, newHeader) => {
  const oldHeader = headers.value[index]
  
  // Allow empty headers but show warning
  if (typeof newHeader !== 'string') {
    showToastMessage('Column header must be a string')
    headers.value[index] = oldHeader // Revert to original
    return
  }
  
  const trimmedNewHeader = newHeader.trim()
  
  // Check if header already exists (case-insensitive) - only for non-empty headers
  if (trimmedNewHeader !== '') {
    const headerExists = headers.value.some((h, i) => 
      i !== index && h.toLowerCase() === trimmedNewHeader.toLowerCase()
    )
    
    if (headerExists) {
      showToastMessage('Column header already exists')
      headers.value[index] = oldHeader // Revert to original
      return
    }
  }
  
  if (oldHeader !== trimmedNewHeader) {
    headers.value[index] = trimmedNewHeader
    // Data remains in columnData structure, no need to move data between headers
    validateAllCells()
    emit('data-updated', getTableData())
  }
}

const importJson = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result)
          if (Array.isArray(data) && data.length > 0) {
            // Ensure all values are strings
            headers.value = Object.keys(data[0])
            // Convert to column-based structure
            columnData.value = headers.value.map(header => 
              data.map(row => String(row[header] || ''))
            )
            jsonError.value = false
            validateAllCells()
            emit('data-updated', getTableData())
            showToastMessage('JSON imported successfully')
          } else {
            showToastMessage('Invalid JSON format or empty array')
          }
        } catch (error) {
          jsonError.value = true
          showToastMessage('Error parsing JSON file')
        }
      }
      reader.readAsText(file)
    }
  }
  input.click()
}

const importCsv = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.csv'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          const csv = e.target.result
          const lines = csv.split('\n').filter(line => line.trim() !== '')
          if (lines.length > 1) {
            const headersRow = lines[0].split(',').map(h => h.trim())
            const dataRows = lines.slice(1)
            
            headers.value = headersRow
            // Convert to column-based structure
            columnData.value = headersRow.map((header, colIndex) => 
              dataRows.map(row => {
                const values = row.split(',').map(v => v.trim())
                return values[colIndex] || ''
              })
            )
            validateAllCells()
            emit('data-updated', getTableData())
            showToastMessage('CSV imported successfully')
          }
        } catch (error) {
          showToastMessage('Error parsing CSV file')
        }
      }
      reader.readAsText(file)
    }
  }
  input.click()
}

const exportJson = () => {
  if (!isTableValid.value) {
    showToastMessage('Please fix validation errors before exporting')
    return
  }
  
  const dataStr = JSON.stringify(getTableData(), null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'table-data.json'
  link.click()
  URL.revokeObjectURL(url)
  showToastMessage('JSON exported successfully')
}

const exportCsv = () => {
  if (!isTableValid.value) {
    showToastMessage('Please fix validation errors before exporting')
    return
  }
  
  if (headers.value.length === 0 || (columnData.value[0]?.length || 0) === 0) return
  
  const tableData = getTableData()
  const csvContent = [
    headers.value.join(','),
    ...tableData.map(row => 
      headers.value.map(header => row[header] || '').join(',')
    )
  ].join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'table-data.csv'
  link.click()
  URL.revokeObjectURL(url)
  showToastMessage('CSV exported successfully')
}

const updateFromJson = () => {
  if (!jsonInput.value.trim()) {
    jsonError.value = false
    return
  }
  
  try {
    const data = JSON.parse(jsonInput.value)
    if (Array.isArray(data) && data.length > 0) {
        headers.value = Object.keys(data[0])
        // Convert to column-based structure
        columnData.value = headers.value.map(header => 
          data.map(row => String(row[header] || ''))
        )
        jsonError.value = false
        validateAllCells()
        emit('data-updated', getTableData())
      } else {
        jsonError.value = true
      }
  } catch (error) {
    jsonError.value = true
  }
}

const loadSampleData = () => {
  const domains = Object.keys(sampleDatasets)
  const domain = domains[currentDatasetIndex.value % domains.length]
  const sampleData = sampleDatasets[domain]
  
  headers.value = Object.keys(sampleData[0])
  // Convert to column-based structure
  columnData.value = headers.value.map(header => 
    sampleData.map(row => String(row[header] || ''))
  )
  currentDatasetIndex.value++
  
  validateAllCells()
  emit('data-updated', getTableData())
  showToastMessage(`Loaded ${domain} sample data`)
}

const toggleJsonEditor = () => {
  showJsonEditor.value = !showJsonEditor.value
  if (showJsonEditor.value) {
    jsonInput.value = JSON.stringify(getTableData(), null, 2)
    jsonError.value = false
  }
}

const openSimulationModal = () => {
  if (isTableValid.value) {
    showSimulationModal.value = true
  } else {
    showToastMessage('Please fix all validation errors before running simulation')
  }
}

const closeSimulationModal = () => {
  showSimulationModal.value = false
  selectedAlgorithms.value = []
}

const runSimulation = () => {
  if (selectedAlgorithms.value.length === 0) {
    showToastMessage('Please select at least one algorithm')
    return
  }
  
  emit('run-simulation', {
    tasks: getTableData(),
    algorithms: selectedAlgorithms.value
  })
  closeSimulationModal()
  showToastMessage('Simulation started')
}

const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const initializeJson = () => {
   jsonInput.value = JSON.stringify(getTableData(), null, 2)
   jsonError.value = false
 }

const updateJson = () => {
  jsonInput.value = JSON.stringify(getTableData(), null, 2)
}

// Watch for data changes
watch(columnData, () => {
  updateJson()
}, { deep: true })

// Intersection Observer untuk floating button
onMounted(() => {
  if (simulationButton.value) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          showFloatingButton.value = !entry.isIntersecting
        })
      },
      { threshold: 0.1 }
    )
    observer.observe(simulationButton.value)
  }
})

const scrollToSimulationButton = () => {
  if (simulationButton.value) {
    simulationButton.value.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

// Initialize
initializeData()
initializeJson()

</script>