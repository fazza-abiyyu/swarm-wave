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
                                    <input v-model="headers[index]" @blur="updateHeader(index, headers[index])"
                                        @keyup.enter="updateHeader(index, headers[index])"
                                        class="bg-transparent border-none outline-none w-full font-medium"
                                        :placeholder="`Column ${index + 1}`" />
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
                        <tr v-for="(row, rowIndex) in tableData" :key="rowIndex"
                            class="hover:bg-gray-50 transition-colors">
                            <td v-for="(header, colIndex) in headers" :key="colIndex"
                                class="px-4 py-3 text-sm text-gray-900">
                                <input v-model="tableData[rowIndex][header]"
                                    @input="updateCell(rowIndex, header, tableData[rowIndex][header])"
                                    class="w-full bg-transparent border-none outline-none px-2 py-1 rounded focus:bg-blue-50 focus:ring-1 focus:ring-blue-300"
                                    :placeholder="`Cell ${rowIndex + 1}-${colIndex + 1}`" />
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
            <div v-if="tableData.length === 0" class="text-center py-12 bg-gray-50">
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
            <button @click="openSimulationModal"
                class="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
                Run Simulation
            </button>
        </div>

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
import { ref, computed, watch } from 'vue'

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
const tableData = ref([])

// Initialize data from props
const initializeData = () => {
  if (props.initialData && props.initialData.length > 0) {
    tableData.value = [...props.initialData]
    headers.value = Object.keys(props.initialData[0])
  } else {
    // Default sample data
    tableData.value = [
      { TaskID: 1, Weight: 10, Duration: 25, Cost: 100 },
      { TaskID: 2, Weight: 15, Duration: 30, Cost: 150 },
      { TaskID: 3, Weight: 8, Duration: 20, Cost: 80 }
    ]
  }
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
const pendingDeleteColumnIndex = ref(null)
const currentDatasetIndex = ref(0)

// Generic sample datasets for different domains
const sampleDatasets = {
    cloud: [
        {"Task_ID": 1, "CPU_Usage (%)": 37, "RAM_Usage (MB)": 2612, "Disk_IO (MB/s)": 55, "Network_IO (MB/s)": 40, "Priority": 2, "VM_ID": 107, "Execution_Time (s)": 1.27, "Target": 1},
        {"Task_ID": 2, "CPU_Usage (%)": 86, "RAM_Usage (MB)": 11761, "Disk_IO (MB/s)": 120, "Network_IO (MB/s)": 85, "Priority": 5, "VM_ID": 108, "Execution_Time (s)": 3.71, "Target": 1},
        {"Task_ID": 3, "CPU_Usage (%)": 44, "RAM_Usage (MB)": 4610, "Disk_IO (MB/s)": 65, "Network_IO (MB/s)": 25, "Priority": 3, "VM_ID": 109, "Execution_Time (s)": 8.53, "Target": 1}
    ],
    manufacturing: [
        {"Job_ID": 1, "Processing_Time": 45, "Setup_Time": 5, "Material_Cost": 250, "Labor_Hours": 8, "Machine_Type": "CNC", "Priority": 3, "Deadline": 120, "Quality_Score": 95},
        {"Job_ID": 2, "Processing_Time": 120, "Setup_Time": 15, "Material_Cost": 800, "Labor_Hours": 20, "Machine_Type": "Lathe", "Priority": 5, "Deadline": 200, "Quality_Score": 88},
        {"Job_ID": 3, "Processing_Time": 30, "Setup_Time": 2, "Material_Cost": 150, "Labor_Hours": 4, "Machine_Type": "Mill", "Priority": 2, "Deadline": 72, "Quality_Score": 92}
    ],
    logistics: [
        {"Order_ID": 1, "Distance_km": 250, "Weight_kg": 1500, "Volume_m3": 8.5, "Urgency": 4, "Fuel_Cost": 180, "Delivery_Time": 4.2, "Customer_Rating": 4.8, "Priority": 3},
        {"Order_ID": 2, "Distance_km": 800, "Weight_kg": 3500, "Volume_m3": 15.2, "Urgency": 5, "Fuel_Cost": 420, "Delivery_Time": 12.5, "Customer_Rating": 4.2, "Priority": 5},
        {"Order_ID": 3, "Distance_km": 120, "Weight_kg": 800, "Volume_m3": 4.1, "Urgency": 2, "Fuel_Cost": 95, "Delivery_Time": 2.1, "Customer_Rating": 4.9, "Priority": 2}
    ],
    finance: [
        {"Investment_ID": 1, "Amount": 50000, "Risk_Score": 7.5, "Expected_Return": 12.5, "Duration_Months": 24, "Market_Volatility": 15.2, "Sector": "Tech", "Liquidity": 8.5, "Priority": 4},
        {"Investment_ID": 2, "Amount": 75000, "Risk_Score": 4.2, "Expected_Return": 8.8, "Duration_Months": 12, "Market_Volatility": 8.7, "Sector": "Healthcare", "Liquidity": 9.2, "Priority": 3},
        {"Investment_ID": 3, "Amount": 30000, "Risk_Score": 9.8, "Expected_Return": 18.5, "Duration_Months": 36, "Market_Volatility": 22.1, "Sector": "Crypto", "Liquidity": 6.1, "Priority": 5}
    ],
    healthcare: [
        {"Patient_ID": 1, "Age": 45, "Treatment_Duration": 14, "Medication_Cost": 2500, "Recovery_Score": 8.5, "Risk_Factor": 3.2, "Priority": 4, "Resource_Usage": 85, "Success_Probability": 0.92},
        {"Patient_ID": 2, "Age": 67, "Treatment_Duration": 28, "Medication_Cost": 7500, "Recovery_Score": 6.8, "Risk_Factor": 7.5, "Priority": 5, "Resource_Usage": 95, "Success_Probability": 0.78},
        {"Patient_ID": 3, "Age": 32, "Treatment_Duration": 7, "Medication_Cost": 1200, "Recovery_Score": 9.2, "Risk_Factor": 1.8, "Priority": 2, "Resource_Usage": 65, "Success_Probability": 0.98}
    ]
}

// Computed property for JSON output
const jsonOutput = computed(() => {
    return JSON.stringify(tableData.value, null, 2)
})

// Initialize JSON input
const initializeJson = () => {
    jsonInput.value = jsonOutput.value
}

// Watch for initialData changes
watch(() => props.initialData, (newData) => {
  if (newData && newData.length > 0) {
    tableData.value = [...newData]
    headers.value = Object.keys(newData[0])
    updateJson()
  }
}, { immediate: true, deep: true })

// Import JSON data
const importJson = () => {
    try {
        const parsedData = JSON.parse(jsonInput.value)
        if (Array.isArray(parsedData) && parsedData.length > 0) {
            tableData.value = parsedData
            headers.value = Object.keys(parsedData[0])
            jsonError.value = false
        }
    } catch (error) {
        jsonError.value = true
        setTimeout(() => jsonError.value = false, 3000)
    }
}

// Update from JSON input
const updateFromJson = () => {
    try {
        const parsedData = JSON.parse(jsonInput.value)
        if (Array.isArray(parsedData) && parsedData.length > 0) {
            tableData.value = parsedData
            headers.value = Object.keys(parsedData[0])
            jsonError.value = false
        }
    } catch (error) {
        jsonError.value = true
    }
}

// Add new row
const addRow = () => {
    const newRow = {}
    headers.value.forEach(header => {
        // Initialize all fields as empty strings (will be converted to numbers if needed)
        newRow[header] = ''
    })
    tableData.value.push(newRow)
    updateJson()
}

// Remove row
const removeRow = (index) => {
    pendingDeleteRowIndex.value = index
    showDeleteRowModal.value = true
}

// Confirm delete row
const confirmDeleteRow = () => {
    if (pendingDeleteRowIndex.value !== null) {
        tableData.value.splice(pendingDeleteRowIndex.value, 1)
        updateJson()
        showDeleteRowModal.value = false
        pendingDeleteRowIndex.value = null
        showToastNotification('Row deleted successfully')
    }
}

// Add new column
const addColumn = () => {
    const newColumnName = `New Column ${headers.value.length + 1}`
    headers.value.push(newColumnName)
    tableData.value.forEach(row => {
        row[newColumnName] = ''
    })
    updateJson()
}

// Remove column
const removeColumn = (index) => {
    pendingDeleteColumnIndex.value = index
    showDeleteColumnModal.value = true
}

// Confirm delete column
const confirmDeleteColumn = () => {
    if (pendingDeleteColumnIndex.value !== null) {
        const columnName = headers.value[pendingDeleteColumnIndex.value]
        headers.value.splice(pendingDeleteColumnIndex.value, 1)
        tableData.value.forEach(row => {
            delete row[columnName]
        })
        updateJson()
        showDeleteColumnModal.value = false
        pendingDeleteColumnIndex.value = null
        showToastNotification('Column deleted successfully')
    }
}

// Update header
const updateHeader = (index, newValue) => {
    const oldValue = headers.value[index]
    if (oldValue !== newValue && newValue.trim() !== '') {
        headers.value[index] = newValue.trim()
        tableData.value.forEach(row => {
            if (row[oldValue] !== undefined) {
                row[newValue.trim()] = row[oldValue]
                delete row[oldValue]
            }
        })
        updateJson()
    }
}

// Update cell
const updateCell = (rowIndex, columnName, value) => {
    tableData.value[rowIndex][columnName] = value
    updateJson()
}

// Update JSON input
const updateJson = () => {
    jsonInput.value = jsonOutput.value
}

// Export JSON
const exportJson = () => {
    const blob = new Blob([jsonOutput.value], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'swarm-lab-data.json'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
}

// Export CSV
const exportCsv = () => {
    if (tableData.value.length === 0) {
        showToastNotification('No data to export', 'warning')
        return
    }

    const csvHeaders = headers.value.join(',')
    const csvRows = tableData.value.map(row =>
        headers.value.map(header => {
            const value = row[header] || ''
            // Escape commas and quotes in CSV
            return `"${String(value).replace(/"/g, '""')}"`
        }).join(',')
    )

    const csvContent = [csvHeaders, ...csvRows].join('\n')
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'swarm-lab-data.csv'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    showToastNotification('CSV exported successfully')
}

// Import CSV
const importCsv = () => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = '.csv'
    input.onchange = (event) => {
        const file = event.target.files[0]
        if (!file) return

        const reader = new FileReader()
        reader.onload = (e) => {
            try {
                const csvContent = e.target.result
                const parsedData = parseCsv(csvContent)
                if (parsedData.length > 0) {
                    headers.value = Object.keys(parsedData[0])
                    tableData.value = parsedData
                    updateJson()
                    showToastNotification(`CSV imported successfully! ${parsedData.length} rows loaded.`)
                }
            } catch (error) {
                showToastNotification('Error importing CSV: ' + error.message, 'warning')
            }
        }
        reader.readAsText(file)
    }
    input.click()
}

// Parse CSV content
const parseCsv = (csvContent) => {
    const lines = csvContent.trim().split('\n')
    if (lines.length < 2) {
        throw new Error('CSV must have at least a header row and one data row')
    }

    // Parse headers from first row
    const headersRow = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''))

    // Parse data rows
    const data = []
    for (let i = 1; i < lines.length; i++) {
        if (!lines[i].trim()) continue

        const values = parseCsvLine(lines[i])
        const row = {}
        headersRow.forEach((header, index) => {
            const value = values[index] || ''
            // Convert all values to numbers where possible, otherwise keep as-is
            const numValue = Number(value)
            row[header] = !isNaN(numValue) ? numValue : value
        })
        data.push(row)
    }

    return data
}

// Parse CSV line handling quoted fields
const parseCsvLine = (line) => {
    const result = []
    let current = ''
    let inQuotes = false

    for (let i = 0; i < line.length; i++) {
        const char = line[i]

        if (char === '"') {
            if (inQuotes && line[i + 1] === '"') {
                current += '"'
                i++ // Skip next quote
            } else {
                inQuotes = !inQuotes
            }
        } else if (char === ',' && !inQuotes) {
            result.push(current.trim())
            current = ''
        } else {
            current += char
        }
    }

    result.push(current.trim())
    return result.map(value => value.replace(/^"|"$/g, ''))
}

// Toggle JSON editor visibility
const toggleJsonEditor = () => {
    showJsonEditor.value = !showJsonEditor.value
}

// Load sample data - cycle through different dataset types
const loadSampleData = () => {
    const datasetTypes = Object.keys(sampleDatasets)
    currentDatasetIndex.value = (currentDatasetIndex.value + 1) % datasetTypes.length
    const currentType = datasetTypes[currentDatasetIndex.value]
    
    tableData.value = [...sampleDatasets[currentType]]
    headers.value = Object.keys(sampleDatasets[currentType][0])
    
    const typeNames = {
        cloud: 'Cloud Computing',
        manufacturing: 'Manufacturing',
        logistics: 'Logistics',
        finance: 'Finance',
        healthcare: 'Healthcare'
    }
    
    showToastNotification(`${typeNames[currentType]} sample data loaded successfully`)
    updateJson()
}

// Simulation modal controls
const openSimulationModal = () => {
    showSimulationModal.value = true
}

// Simulation methods
const runSimulation = () => {
  if (selectedAlgorithms.value.length === 0) {
    showToastNotification('Please select at least one algorithm', 'warning')
    return
  }

  if (tableData.value.length === 0) {
    showToastNotification('Please add some data to run simulation', 'warning')
    return
  }

  // Format data for simulation - preserve all original fields
  const simulationData = tableData.value.map((row, index) => {
    const task = {}
    headers.value.forEach(header => {
      // Convert numeric values when possible, otherwise keep as-is
      const value = row[header]
      const numValue = Number(value)
      task[header] = !isNaN(numValue) ? numValue : value
    })
    return task
  })

  // Store simulation data and navigate
  const simulationStore = {
    tasks: simulationData,
    algorithms: selectedAlgorithms.value
  }

  // Log the data being sent
  console.log('DynamicTable - Emitting simulation data:', {
    tasks: simulationData.length,
    algorithms: selectedAlgorithms.value
  })

  // Close modal and emit event to parent
  closeSimulationModal()
  emit('run-simulation', simulationStore)
  showToastNotification(`Preparing ${selectedAlgorithms.value.join(' and ')} simulation...`, 'info')
}

// Close simulation modal
const closeSimulationModal = () => {
    showSimulationModal.value = false
    selectedAlgorithms.value = []
}

// Toast notification helper
const showToastNotification = (message, type = 'info') => {
    toastMessage.value = message
    showToast.value = true
    
    setTimeout(() => {
        showToast.value = false
    }, 3000) // Auto-hide after 3 seconds
}



// Watch for data changes
watch(tableData, () => {
    updateJson()
}, { deep: true })

// Initialize
initializeData()
initializeJson()
</script>

<style scoped>
.dynamic-table-container {
    max-width: 100%;
    margin: 0 auto;
}

input:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

@media (max-width: 768px) {
    .controls-section {
        padding: 1rem;
    }

    .controls-section button {
        width: 100%;
        margin-bottom: 0.5rem;
    }

    .table-section {
        overflow-x: auto;
    }
}
</style>