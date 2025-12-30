<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white/95 backdrop-blur-sm shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-yellow-500 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                <circle cx="3" cy="3" r="1"/>
                <circle cx="10" cy="3" r="1"/>
                <circle cx="17" cy="3" r="1"/>
                <circle cx="6.5" cy="10" r="1"/>
                <circle cx="13.5" cy="10" r="1"/>
                <circle cx="10" cy="17" r="1"/>
                <line x1="3" y1="3" x2="6.5" y2="10" stroke="currentColor" stroke-width="0.5"/>
                <line x1="10" y1="3" x2="6.5" y2="10" stroke="currentColor" stroke-width="0.5"/>
                <line x1="10" y1="3" x2="13.5" y2="10" stroke="currentColor" stroke-width="0.5"/>
                <line x1="17" y1="3" x2="13.5" y2="10" stroke="currentColor" stroke-width="0.5"/>
                <line x1="6.5" y1="10" x2="10" y2="17" stroke="currentColor" stroke-width="0.5"/>
                <line x1="13.5" y1="10" x2="10" y2="17" stroke="currentColor" stroke-width="0.5"/>
              </svg>
            </div>
            <span @click="showSimulation = false"  class="text-xl font-bold text-gray-900">Swarm Wave</span>
          </div>

          <!-- Navigation Links -->
          <nav class="hidden md:flex items-center space-x-1">
              <a 
                href="#" 
                @click="showSimulation = false" 
                :class="!showSimulation ? 'text-blue-600 bg-blue-50/50' : 'text-gray-600 hover:text-gray-900'"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-gray-50"
              >
                Home
              </a>
              <NuxtLink to="/about" class="text-gray-600 hover:text-gray-900 px-4 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-gray-50">About</NuxtLink>
            </nav>

          <!-- Mobile Menu Button -->
          <div class="md:hidden">
            <button @click="isMobileMenuOpen = !isMobileMenuOpen" 
                  class="text-gray-600 hover:text-gray-900 p-2 rounded-lg transition-colors hover:bg-gray-50">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
          </div>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div v-if="isMobileMenuOpen" class="md:hidden fixed inset-0 top-16 bg-white backdrop-blur-sm border-t border-gray-200 z-40">
          <div class="px-4 py-3 space-y-2 bg-white/90">
            <a 
              href="#" 
              @click="showSimulation = false; isMobileMenuOpen = false" 
              :class="!showSimulation ? 'text-blue-600 bg-blue-50/50' : 'text-gray-700 hover:text-blue-600'"
              class="block px-3 py-2 rounded-lg transition-colors"
            >
              Home
            </a>
            <NuxtLink to="/about" @click="isMobileMenuOpen = false" class="block px-3 py-2 text-gray-700 hover:text-blue-600 transition-colors">About</NuxtLink>
          </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Data Table View -->
        <div v-if="!showSimulation">
          <div class="text-center mb-8">
            <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-2">Swarm Wave – Experimental Data Platform</h1>
            <p class="text-lg text-gray-600">Manage, analyze, and integrate data for swarm intelligence research, with support for JSON and CSV</p>
          </div>

          <!-- DynamicTable Component -->
        <DynamicTable :initial-data="tableData" @data-updated="onDataUpdated" @run-simulation="onRunSimulation" />
        </div>

        <!-- Simulation View -->
        <div v-else>
          <SimulationPage 
            :tasks="rawTasks" 
            :algorithms="selectedAlgorithms" 
            @back-to-table="showSimulation = false" 
            @edit-data="onEditData"
          />
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200/50 mt-16">
      <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <div class="flex justify-center mb-4">
            <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-yellow-500 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                <circle cx="3" cy="3" r="1"/>
                <circle cx="10" cy="3" r="1"/>
                <circle cx="17" cy="3" r="1"/>
                <circle cx="6.5" cy="10" r="1"/>
                <circle cx="13.5" cy="10" r="1"/>
                <circle cx="10" cy="17" r="1"/>
                <line x1="3" y1="3" x2="6.5" y2="10" stroke="currentColor" stroke-width="0.5"/>
                <line x1="10" y1="3" x2="6.5" y2="10" stroke="currentColor" stroke-width="0.5"/>
                <line x1="10" y1="3" x2="13.5" y2="10" stroke="currentColor" stroke-width="0.5"/>
                <line x1="17" y1="3" x2="13.5" y2="10" stroke="currentColor" stroke-width="0.5"/>
                <line x1="6.5" y1="10" x2="10" y2="17" stroke="currentColor" stroke-width="0.5"/>
                <line x1="13.5" y1="10" x2="10" y2="17" stroke="currentColor" stroke-width="0.5"/>
              </svg>
            </div>
          </div>
          <p class="text-gray-500 text-sm">
            © 2025 Swarm Wave. Experimental data platform for swarm intelligence research.
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DynamicTable from '~/components/dynamic-table/index.vue'
import SimulationPage from '~/components/simulations/index.vue'

// State
const showSimulation = ref(false)
const isMobileMenuOpen = ref(false)
const currentTasks = ref([]) // Processed tasks for simulation
const rawTasks = ref([]) // Original raw tasks data
const selectedAlgorithms = ref([])

// Reactive data
const tableData = ref([])

// Handle data updates from DynamicTable - preserve all original fields
const onDataUpdated = (data) => {
  if (!data || !Array.isArray(data)) {
    currentTasks.value = []
    rawTasks.value = []
    return
  }
  
  // Store raw data as-is for editing purposes
  rawTasks.value = [...data]
  
  // Process data for simulation
  currentTasks.value = data.map(task => {
    if (!task || typeof task !== 'object') {
      return {}
    }
    
    const processedTask = {}
    Object.keys(task).forEach(key => {
      const value = task[key]
      const numValue = Number(value)
      processedTask[key] = !isNaN(numValue) ? numValue : value
    })
    return processedTask
  })
}

// Handle edit data request from SimulationPage
const onEditData = (data) => {
  // If data provided, use it; otherwise use rawTasks (original data)
  const dataToEdit = data || rawTasks.value || []
  
  if (!Array.isArray(dataToEdit)) {
    tableData.value = []
    rawTasks.value = []
    currentTasks.value = []
    showSimulation.value = false
    return
  }
  
  tableData.value = dataToEdit
  onDataUpdated(dataToEdit)
  showSimulation.value = false
}

// Handle simulation request from DynamicTable
const onRunSimulation = (simulationData) => {
  console.log('Dashboard - Received simulation data:', {
    tasks: simulationData.tasks?.length,
    algorithms: simulationData.algorithms
  })

  // Switch to simulation view
  showSimulation.value = true
  
  // Ensure tasks are updated before running simulation - preserve all original fields
  if (simulationData.tasks && simulationData.tasks.length > 0) {
    // Store raw data
    rawTasks.value = [...simulationData.tasks]
    
    // Process data for simulation
    currentTasks.value = simulationData.tasks.map(task => {
      const processedTask = {}
      Object.keys(task).forEach(key => {
        const value = task[key]
        const numValue = Number(value)
        processedTask[key] = !isNaN(numValue) ? numValue : value
      })
      return processedTask
    })
  }
  
  // Store algorithms for SimulationPage
  if (simulationData.algorithms && simulationData.algorithms.length > 0) {
    console.log('Dashboard - Setting algorithms for SimulationPage:', simulationData.algorithms)
    selectedAlgorithms.value = [...simulationData.algorithms]
  }
}

// Initialize currentTasks with initial data
onMounted(() => {
  if (tableData.value && Array.isArray(tableData.value) && tableData.value.length > 0) {
    onDataUpdated(tableData.value)
  } else {
    currentTasks.value = []
    rawTasks.value = []
  }
})
</script>

<style scoped>
/* Custom scrollbar styles */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>