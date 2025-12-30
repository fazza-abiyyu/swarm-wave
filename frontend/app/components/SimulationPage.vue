<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <!-- Toast Notification -->
    <div 
      v-if="toast.show"
      class="fixed top-4 right-4 z-50 px-4 py-3 rounded-lg border border-gray-200 shadow-none flex items-center animate-fade-in"
      :class="{
        'bg-red-500 text-white': toast.type === 'error',
        'bg-green-500 text-white': toast.type === 'success',
        'bg-blue-500 text-white': toast.type === 'info'
      }"
    >
      <svg v-if="toast.type === 'error'" class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      <svg v-else-if="toast.type === 'success'" class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
      </svg>
      <span>{{ toast.message }}</span>
    </div>

    <!-- Header -->
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">
          Swarm Intelligence Simulation
        </h1>
        <p class="text-gray-600">
          Run ACO or PSO algorithms on your experimental data
        </p>
      </div>

      <!-- Data Preview -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-none p-6 mb-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">Data Preview</h3>
          <button @click="editData"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
            Edit
          </button>
        </div>
        <div
          v-if="!filteredTasks || filteredTasks.length === 0"
          class="text-center py-8 text-gray-500"
        >
          <svg
            class="w-12 h-12 mx-auto mb-2 text-gray-400"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM4.332 8.027a6.012 6.012 0 011.912-2.706C6.512 5.73 6.974 6 7.5 6A1.5 1.5 0 019 7.5V8a2 2 0 004 0 2 2 0 011.523-1.943A5.522 5.522 0 0016 10c0 .973-.325 1.875-.923 2.627A5.994 5.994 0 0110 16c-1.567 0-3.02-.529-4.191-1.425a6.012 6.012 0 01-1.912-2.706z"
              clip-rule="evenodd"
            />
          </svg>
          <p>No data available</p>
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  v-for="header in datasetHeaders"
                  :key="header"
                  class="px-4 py-2 text-left text-xs font-medium text-gray-500 tracking-wider"
                >
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="(task, index) in filteredTasks.slice(0, 5)"
                :key="index"
                class="hover:bg-gray-50"
              >
                <td
                  v-for="header in datasetHeaders"
                  :key="header"
                  class="px-4 py-2 whitespace-nowrap text-sm text-gray-900"
                >
                  {{ task[header] }}
                </td>
              </tr>
            </tbody>
          </table>
          <div
            v-if="filteredTasks.length > 5"
            class="text-center py-2 text-sm text-gray-500"
          >
            Showing first 5 of {{ filteredTasks.length }} rows
          </div>
        </div>

        <!-- Data Filtering Controls -->
        <div v-if="props.tasks.length > 10" class="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <h4 class="text-sm font-medium text-gray-700 mb-3">Filter Data for Simulation</h4>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Limit Data Rows
              </label>
              <input
                v-model.number="dataLimit"
                type="number"
                :min="1"
                :max="props.tasks.length"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter number of rows"
                @input="validateDataLimitInput"
              />
              <p class="text-xs text-gray-500 mt-1">
                Showing {{ previewCount }} of {{ props.tasks.length }} rows
              </p>
            </div>
            
            <div>
              <label class="flex items-center cursor-pointer">
                <input
                  v-model="showAllData"
                  type="checkbox"
                  class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                />
                <span class="ml-2 text-sm text-gray-700">Select all data</span>
              </label>
            </div>

            <div class="text-sm text-gray-600">
              <p>Preview: {{ previewCount }} rows</p>
              <p class="text-xs">This affects simulation input only</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Algorithm Selection -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-none p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">
          Algorithm Selection
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="flex items-center">
            <input
              v-model="selectedAlgorithms"
              type="checkbox"
              value="ACO"
              id="aco-checkbox"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
            <label
              for="aco-checkbox"
              class="ml-2 text-sm font-medium text-gray-900"
              >Ant Colony Optimization (ACO)</label
            >
          </div>
          <div class="flex items-center">
            <input
              v-model="selectedAlgorithms"
              type="checkbox"
              value="PSO"
              id="pso-checkbox"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
            <label
              for="pso-checkbox"
              class="ml-2 text-sm font-medium text-gray-900"
              >Particle Swarm Optimization (PSO)</label
            >
          </div>
        </div>
      </div>

      <!-- Parameters Section -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-none p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-6">
          Algorithm Parameters
        </h2>

        <!-- Common Parameters -->
        <div class="mb-8">
          <h3 class="text-lg font-medium text-gray-800 mb-4">Common Parameters</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Common Parameters -->
            <div>
              <div class="flex items-center gap-1 mb-2">
                <label class="block text-sm font-medium text-gray-700">
                  Number of Agents
                </label>
                <span
                  class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                >
                  ?
                  <div
                    class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                  >
                    Number of worker agents (ants or particles) that will process
                    tasks simultaneously. More agents can explore more solutions
                    but increase computation time. Range: 1-10. Example: 3
                  </div>
                </span>
              </div>
              <input
                v-model.number="parameters.num_default_agents"
                type="number"
                min="1"
                max="10"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <div class="flex items-center gap-1 mb-2">
                <label class="block text-sm font-medium text-gray-700">
                  Iterations
                </label>
                <span
                  class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                >
                  ?
                  <div
                    class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                  >
                    Total number of optimization cycles the algorithm will
                    perform. More iterations allow better convergence but take
                    longer to complete. Range: 1-100. Example: 50
                  </div>
                </span>
              </div>
              <input
                v-model.number="parameters.n_iterations"
                type="number"
                min="1"
                max="100"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <div class="flex items-center gap-1 mb-2">
                <label class="block text-sm font-medium text-gray-700">
                  Task ID Column
                </label>
                <span v-if="parameters.task_id_col === datasetHeaders[0] && datasetHeaders.length > 0" 
                      class="px-2 py-1 text-xs bg-blue-100 text-blue-600 rounded-md">
                  Auto-selected
                </span>
                <span
                  class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                >
                  ?
                  <div
                    class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                  >
                    Column name for task IDs in your dataset. Automatically set to the first column of your data.
                  </div>
                </span>
              </div>
              <select
                v-model="parameters.task_id_col"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option v-if="datasetHeaders.length === 0" value="" disabled>
                  No columns available
                </option>
                <option v-for="header in datasetHeaders" :key="header" :value="header">
                  {{ header }}
                </option>
              </select>
            </div>
<!-- 
            <div>
              <div class="flex items-center gap-1 mb-2">
                <label class="block text-sm font-medium text-gray-700">
                  Agent ID Column
                </label>
                <span
                  class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                >
                  ?
                  <div
                    class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                    >
                    Column name for agent IDs in your dataset.
                    Default: 'id'
                  </div>
                </span>
              </div>
              <select
                v-model="parameters.agent_id_col"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">None</option>
                <option v-for="header in datasetHeaders" :key="header" :value="header">
                  {{ header }}
                </option>
              </select>
            </div> -->
            
            <!-- Dependency Column Selection -->
            <div>
              <div class="flex items-center gap-1 mb-2">
                <label class="block text-sm font-medium text-gray-700">
                  Dependencies Column
                </label>
                <span v-if="hasDependencyColumn && parameters.dependency_col === dependencyColumn" 
                      class="px-2 py-1 text-xs bg-blue-100 text-blue-600 rounded-md">
                  Auto-selected
                </span>
                <span v-if="hasDependencyColumn && parameters.enable_dependencies" 
                      class="px-2 py-1 text-xs bg-green-100 text-green-600 rounded-md">
                  Enabled
                </span>
                <span
                  class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                >
                  ?
                  <div
                    class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                  >
                    Column containing task dependencies/prerequisites. 
                    Auto-detected from columns with names like 'dependencies', 'depends_on', 'prerequisites', or 'requires'.
                    Dependencies are automatically enabled when this column is selected.
                  </div>
                </span>
              </div>
              <select
                v-model="parameters.dependency_col"
                @change="parameters.enable_dependencies = parameters.dependency_col !== ''"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">None (No Dependencies)</option>
                <option v-for="header in datasetHeaders" :key="header" :value="header">
                  {{ header }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- Algorithm-Specific Parameters -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- ACO Specific Parameters -->
          <template v-if="selectedAlgorithms.includes('ACO')">
            <div>
              <h3 class="text-lg font-medium text-gray-800 mb-4">
                ACO Parameters
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <div class="flex items-center gap-1 mb-2">
                    <label class="block text-sm font-medium text-gray-700"
                      >Alpha (Pheromone Influence)</label
                    >
                    <span
                      class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                    >
                      ?
                      <div
                        class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                      >
                        Controls how strongly ants are guided by pheromone
                        trails. Higher values make ants follow existing paths
                        more closely. Range: 0-5. Example: 0.7
                      </div>
                    </span>
                  </div>

                  <input
                    v-model.number="parameters.alpha"
                    type="number"
                    step="0.1"
                    min="0"
                    max="5"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <div class="flex items-center gap-1 mb-2">
                    <label class="block text-sm font-medium text-gray-700">
                      Beta (Heuristic Influence)
                    </label>
                    <span
                      class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                    >
                      ?
                      <div
                        class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                      >
                        Controls how strongly ants consider task priorities or
                        distances. Higher values make ants prefer more important
                        or closer tasks. Range: 0-5. Example: 3.0
                      </div>
                    </span>
                  </div>
                  <input
                    v-model.number="parameters.beta"
                    type="number"
                    step="0.1"
                    min="0"
                    max="5"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <div class="flex items-center gap-1 mb-2">
                    <label class="block text-sm font-medium text-gray-700">
                      Evaporation Rate
                    </label>
                    <span
                      class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                    >
                      ?
                      <div
                        class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                      >
                        Rate at which pheromone trails evaporate over time.
                        Higher values help prevent premature convergence but may
                        lose good solutions. Range: 0-1. Example: 0.5
                      </div>
                    </span>
                  </div>
                  <input
                    v-model.number="parameters.evaporation_rate"
                    type="number"
                    step="0.1"
                    min="0"
                    max="1"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <div class="flex items-center gap-1 mb-2">
                    <label class="block text-sm font-medium text-gray-700">
                      Pheromone Deposit
                    </label>
                    <span
                      class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                    >
                      ?
                      <div
                        class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                      >
                        Amount of pheromone deposited by ants on successful paths.
                        Higher values strengthen pheromone trails faster.
                        Range: 1-500. Example: 100.0
                      </div>
                    </span>
                  </div>
                  <input
                    v-model.number="parameters.pheromone_deposit"
                    type="number"
                    step="1"
                    min="1"
                    max="500"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <div class="flex items-center gap-1 mb-2">
                    <label class="block text-sm font-medium text-gray-700">
                      Number of Ants
                    </label>
                    <span
                      class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                    >
                      ?
                      <div
                        class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                      >
                        Number of ants exploring solutions in each iteration.
                        More ants explore more solutions but increase computation time.
                        Range: 1-100. Example: 25
                      </div>
                    </span>
                  </div>
                  <input
                    v-model.number="parameters.n_ants"
                    type="number"
                    min="1"
                    max="100"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>
          </template>

          <!-- PSO Specific Parameters -->
          <template v-if="selectedAlgorithms.includes('PSO')">
            <div>
              <h3 class="text-lg font-medium text-gray-800 mb-4">
                PSO Parameters
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <div class="flex items-center gap-1 mb-2">
                    <label class="block text-sm font-medium text-gray-700">
                      Particles
                    </label>
                    <span
                      class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                    >
                      ?
                      <div
                        class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                      >
                        Number of particles in the swarm that search for optimal
                        task assignments. More particles explore more solutions
                        but increase computation time. Range: 1-100. Example: 30
                      </div>
                    </span>
                  </div>
                  <input
                    v-model.number="parameters.n_particles"
                    type="number"
                    min="1"
                    max="100"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <div class="flex items-center gap-1 mb-2">
                    <label class="block text-sm font-medium text-gray-700">
                      Inertia (w)
                    </label>
                    <span
                      class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                    >
                      ?
                      <div
                        class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                      >
                        Controls particle momentum - how much particles continue
                        in their current direction. Higher values promote
                        exploration, lower values promote exploitation. Range:
                        0-1. Example: 0.7
                      </div>
                    </span>
                  </div>
                  <input
                    v-model.number="parameters.w"
                    type="number"
                    step="0.1"
                    min="0"
                    max="1"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <div class="flex items-center gap-1 mb-2">
                    <label class="block text-sm font-medium text-gray-700">
                      Cognitive (c1)
                    </label>
                    <span
                      class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                    >
                      ?
                      <div
                        class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                      >
                        Particle's attraction to its own best known position.
                        Higher values make particles more likely to return to
                        their personal best solutions. Range: 0-3. Example: 1.5
                      </div>
                    </span>
                  </div>
                  <input
                    v-model.number="parameters.c1"
                    type="number"
                    step="0.1"
                    min="0"
                    max="3"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <div class="flex items-center gap-1 mb-2">
                    <label class="block text-sm font-medium text-gray-700">
                      Social (c2)
                    </label>
                    <span
                      class="relative group cursor-pointer text-gray-400 text-xs font-bold"
                    >
                      ?
                      <div
                        class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                      >
                        Particle's attraction to the swarm's best known
                        position. Higher values promote convergence to global
                        best solutions. Range: 0-3. Example: 1.5
                      </div>
                    </span>
                  </div>
                  <input
                    v-model.number="parameters.c2"
                    type="number"
                    step="0.1"
                    min="0"
                    max="3"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>
          </template>
        </div>

        <div class="mt-6 flex gap-3">
          <button
          @click="runSimulation"
          :disabled="
            isRunning ||
            selectedAlgorithms.length === 0 ||
            !dataValidation.isValid ||
            filteredTasks.length === 0
          "
          class="flex-1 md:flex-none px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          <span v-if="isRunning">Running...</span>
          <span v-else-if="filteredTasks.length === 0">No Data Available</span>
          <span v-else-if="!dataValidation.isValid">Invalid Data</span>
          <span v-else>{{
            `Run ${selectedAlgorithms.join(" & ")} Simulation`
          }}</span>
        </button>
        
        <button
          v-if="isRunning"
          @click="stopSimulation"
          class="px-6 py-3 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <rect x="6" y="6" width="8" height="8" rx="1" />
          </svg>
          Stop
        </button>
        </div>
      </div>

      <!-- Algorithm Results -->
      <div v-if="selectedAlgorithms.length > 0" class="space-y-6">
        <!-- ACO Results -->
        <div
          v-if="selectedAlgorithms.includes('ACO')"
          class="bg-white rounded-xl border border-gray-200 shadow-none p-6"
        >
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-900">
              Ant Colony Optimization (ACO) Results
            </h2>
            <div class="flex items-center gap-2">
              <span
                :class="[
                  'px-3 py-1 rounded-full text-xs font-medium',
                  status.ACO === 'Idle'
                    ? 'bg-gray-100 text-gray-800'
                    : status.ACO === 'Running...'
                    ? 'bg-blue-100 text-blue-800'
                    : status.ACO === 'Completed'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800',
                ]"
              >
                Status: {{ status.ACO }}
              </span>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- ACO Logs -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">ACO Logs</h3>
              <div class="bg-gray-50 rounded-lg p-4 h-64 overflow-y-auto" ref="acoLogsContainer">
                <div
                  v-if="!logs.ACO || logs.ACO.length === 0"
                  class="text-gray-500 text-center"
                >
                  Run simulation to see ACO logs
                </div>
                <div v-else class="space-y-1 text-sm font-mono">
                  <div
                    v-for="(log, index) in logs.ACO"
                    :key="index"
                    class="text-gray-700"
                  >
                    {{ log }}
                  </div>
                </div>
              </div>
            </div>

            <!-- ACO Chart -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">
                ACO Convergence Chart
              </h3>
              <div class="h-64">
                <canvas ref="chartCanvasACO" class="w-full h-full"></canvas>
              </div>
            </div>
          </div>

          <!-- ACO Assignment -->
          <div class="mt-6">
            <div class="flex justify-between items-center mb-2">
              <h3 class="text-lg font-medium text-gray-900">
                ACO Final Assignment
                <span v-if="bestMakespan.ACO"
                  >(Best Makespan: {{ parseFloat(bestMakespan.ACO).toFixed(2) }}s)</span
                >
              </h3>
              <div class="flex gap-2">
                <button
                  @click="exportJSON('ACO')"
                  class="px-3 py-1 text-xs bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  Export JSON
                </button>
                <button
                  @click="exportCSV('ACO')"
                  class="px-3 py-1 text-xs bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                >
                  Export CSV
                </button>
              </div>
            </div>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Agent
                    </th>
                    <th
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Task List
                    </th>
                    <th
                      class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Total Time
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="acoFinalAssignment.length === 0">
                     <td colspan="3" class="px-6 py-4 text-center text-sm text-gray-500">
                        No assignment data yet.
                     </td>
                  </tr>
                  <tr
                    v-for="assignment in acoFinalAssignment"
                    :key="assignment.agent"
                  >
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                    >
                      {{ assignment.agent }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500">
                      <div class="max-w-xs">
                        <div
                          v-if="
                            !expandedTasks.ACO[assignment.agent] &&
                            assignment.tasks &&
                            assignment.tasks.length > 10
                          "
                        >
                          {{ assignment.tasks.slice(0, 10).join(", ") }}
                          <button
                            @click="
                              toggleTaskExpansion('ACO', assignment.agent)
                            "
                            class="text-blue-600 hover:text-blue-800 ml-1"
                          >
                            ... (+{{ assignment.tasks.length - 10 }} more)
                          </button>
                        </div>
                        <div
                          v-else
                        >
                          <div class="max-h-32 overflow-y-auto">
                            {{
                              Array.isArray(assignment.tasks)
                                ? assignment.tasks.join(", ")
                                : assignment.tasks
                            }}
                          </div>
                          <button
                            v-if="
                              assignment.tasks.length > 10 &&
                              expandedTasks.ACO[assignment.agent]
                            "
                            @click="
                              toggleTaskExpansion('ACO', assignment.agent)
                            "
                            class="text-blue-600 hover:text-blue-800 text-xs mt-1"
                          >
                            Show less
                          </button>
                        </div>
                      </div>
                    </td>
                    <td
                      class="px-6 py-4 text-sm text-gray-500 text-right font-mono"
                    >
                      <span>
                        {{
                          typeof assignment.total_time === "number"
                            ? assignment.total_time.toFixed(2)
                            : assignment.total_time
                        }}s
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- PSO Results -->
        <div
          v-if="selectedAlgorithms.includes('PSO')"
          class="bg-white rounded-xl border border-gray-200 shadow-none p-6"
        >
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-900">
              Particle Swarm Optimization (PSO) Results
            </h2>
            <div class="flex items-center gap-2">
              <span
                :class="[
                  'px-3 py-1 rounded-full text-xs font-medium',
                  status.PSO === 'Idle'
                    ? 'bg-gray-100 text-gray-800'
                    : status.PSO === 'Running...'
                    ? 'bg-blue-100 text-blue-800'
                    : status.PSO === 'Completed'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800',
                ]"
              >
                Status: {{ status.PSO }}
              </span>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- PSO Logs -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">PSO Logs</h3>
              <div class="bg-gray-50 rounded-lg p-4 h-64 overflow-y-auto" ref="psoLogsContainer">
                <div
                  v-if="!logs.PSO || logs.PSO.length === 0"
                  class="text-gray-500 text-center"
                >
                  Run simulation to see PSO logs
                </div>
                <div v-else class="space-y-1 text-sm font-mono">
                  <div
                    v-for="(log, index) in logs.PSO"
                    :key="index"
                    class="text-gray-700"
                  >
                    {{ log }}
                  </div>
                </div>
              </div>
            </div>

            <!-- PSO Chart -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">
                PSO Convergence Chart
              </h3>
              <div class="h-64">
                <canvas ref="chartCanvasPSO" class="w-full h-full"></canvas>
              </div>
            </div>
          </div>

          <!-- PSO Assignment -->
          <div class="mt-6">
            <div class="flex justify-between items-center mb-2">
              <h3 class="text-lg font-medium text-gray-900">
                PSO Final Assignment
                <span v-if="bestMakespan.PSO"
                  >(Best Makespan: {{ parseFloat(bestMakespan.PSO).toFixed(2) }}s)</span
                >
              </h3>
              <div class="flex gap-2">
                <button
                  @click="exportJSON('PSO')"
                  class="px-3 py-1 text-xs bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  Export JSON
                </button>
                <button
                  @click="exportCSV('PSO')"
                  class="px-3 py-1 text-xs bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                >
                  Export CSV
                </button>
              </div>
            </div>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Agent
                    </th>
                    <th
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Task List
                    </th>
                    <th
                      class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Total Time
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                   <tr v-if="psoFinalAssignment.length === 0">
                     <td colspan="3" class="px-6 py-4 text-center text-sm text-gray-500">
                        No assignment data yet.
                     </td>
                  </tr>
                  <tr
                    v-for="assignment in psoFinalAssignment"
                    :key="assignment.agent"
                  >
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                    >
                      {{ assignment.agent }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500">
                      <div class="max-w-xs">
                        <div
                          v-if="
                            !expandedTasks.PSO[assignment.agent] &&
                            assignment.tasks &&
                            assignment.tasks.length > 10
                          "
                        >
                          {{ assignment.tasks.slice(0, 10).join(", ") }}
                          <button
                            @click="
                              toggleTaskExpansion('PSO', assignment.agent)
                            "
                            class="text-blue-600 hover:text-blue-800 ml-1"
                          >
                            ... (+{{ assignment.tasks.length - 10 }} more)
                          </button>
                        </div>
                        <div
                          v-else
                        >
                          <div class="max-h-32 overflow-y-auto">
                            {{
                              Array.isArray(assignment.tasks)
                                ? assignment.tasks.join(", ")
                                : assignment.tasks
                            }}
                          </div>
                          <button
                            v-if="
                              assignment.tasks &&
                              assignment.tasks.length > 10 &&
                              expandedTasks.PSO[assignment.agent]
                            "
                            @click="
                              toggleTaskExpansion('PSO', assignment.agent)
                            "
                            class="text-blue-600 hover:text-blue-800 text-xs mt-1"
                          >
                            Show less
                          </button>
                        </div>
                      </div>
                    </td>
                    <td
                      class="px-6 py-4 text-sm text-gray-500 text-right font-mono"
                    >
                      <span>
                        {{
                          typeof assignment.total_time === "number"
                            ? assignment.total_time.toFixed(2)
                            : assignment.total_time
                        }}s
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Validation -->
      <div
        v-if="
          dataValidation.errors.length > 0 || dataValidation.warnings.length > 0
        "
        class="bg-white rounded-xl border border-gray-200 shadow-none p-6 mb-6"
      >
        <h3 class="text-lg font-medium text-gray-900 mb-4">Data Validation</h3>

        <!-- Validation Results -->
        <div v-if="dataValidation.errors.length > 0" class="mb-4">
          <div
            v-for="error in dataValidation.errors"
            :key="error"
            class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-2 text-sm"
          >
            <svg
              class="w-4 h-4 inline mr-2"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"
              />
            </svg>
            {{ error }}
          </div>
        </div>

        <div v-if="dataValidation.warnings.length > 0" class="mb-4">
          <div
            v-for="warning in dataValidation.warnings"
            :key="warning"
            class="bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded-md mb-2 text-sm"
          >
            <svg
              class="w-4 h-4 inline mr-2"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                clip-rule="evenodd"
              />
            </svg>
            {{ warning }}
          </div>
        </div>
      </div>

      <!-- No Data State -->
      <div
        v-if="props.tasks.length === 0"
        class="bg-white rounded-xl border border-gray-200 shadow-none p-6"
      >
        <div class="text-center py-12">
          <div class="text-gray-400 mb-4">
            <svg
              class="w-16 h-16 mx-auto"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
              />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            No Data Available
          </h3>
          <p class="text-gray-500 mb-4">
            Please add some tasks to the data table before running simulations.
          </p>
          <button
            @click="$emit('back-to-table')"
            class="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <svg
              class="w-4 h-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
            Go to Data Table
          </button>
        </div>
      </div>

      <!-- Overall Best Result Section -->
      <div
        v-if="bestMakespan.ACO && bestMakespan.PSO && selectedAlgorithms.includes('ACO') && selectedAlgorithms.includes('PSO')"
        class="bg-white rounded-xl border border-gray-200 shadow-none p-6 mt-6"
      >
        <h2 class="text-xl font-semibold text-gray-900 mb-4">
          Overall Best Result
        </h2>

        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Algorithm
                </th>
                <th
                  class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Best Makespan (s)
                </th>
                <th
                  class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Total Execution Time (ms)
                </th>
                <th
                  class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Load Balancing Index
                </th>
                <th
                  class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Computation Time (ms)
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                :class="[
                  isWinner.ACO
                    ? 'bg-blue-50 text-blue-700 font-bold'
                    : 'text-gray-900',
                ]"
              >
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm"
                  :class="{
                    'font-bold': isWinner.ACO,
                  }"
                >
                  ACO
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{
                    'font-bold': isWinner.ACO,
                  }"
                >
                  {{
                    bestMakespan.ACO
                      ? parseFloat(bestMakespan.ACO).toFixed(2)
                      : "N/A"
                  }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{
                    'font-bold': isWinner.ACO,
                  }"
                >
                  {{
                    executionTime.ACO
                      ? parseFloat(executionTime.ACO).toFixed(2)
                      : "N/A"
                  }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{
                    'font-bold': isWinner.ACO,
                  }"
                >
                  {{
                    loadBalanceIndex.ACO
                      ? parseFloat(loadBalanceIndex.ACO).toFixed(4)
                      : "N/A"
                  }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{
                    'font-bold': isWinner.ACO,
                  }"
                >
                  {{
                    computationTime.ACO
                      ? parseFloat(computationTime.ACO).toFixed(2)
                      : "N/A"
                  }}
                </td>
              </tr>
              <tr
                :class="[
                  isWinner.PSO
                    ? 'bg-blue-50 text-blue-700 font-bold'
                    : 'text-gray-900',
                ]"
              >
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm"
                  :class="{
                    'font-bold': isWinner.PSO,
                  }"
                >
                  PSO
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{
                    'font-bold': isWinner.PSO,
                  }"
                >
                  {{
                    bestMakespan.PSO
                      ? parseFloat(bestMakespan.PSO).toFixed(2)
                      : "N/A"
                  }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{
                    'font-bold': isWinner.PSO,
                  }"
                >
                  {{
                    executionTime.PSO
                      ? parseFloat(executionTime.PSO).toFixed(2)
                      : "N/A"
                  }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{
                    'font-bold': isWinner.PSO,
                  }"
                >
                  {{
                    loadBalanceIndex.PSO
                      ? parseFloat(loadBalanceIndex.PSO).toFixed(4)
                      : "N/A"
                  }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{
                    'font-bold': isWinner.PSO,
                  }"
                >
                  {{
                    computationTime.PSO
                      ? parseFloat(computationTime.PSO).toFixed(2)
                      : "N/A"
                  }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-6 pt-4 border-t border-gray-200 text-center">
          <span class="text-lg font-bold text-blue-600">
            Winner: {{ winner }}
          </span>
          <div v-if="winner !== 'Pending' && bestMakespan.ACO && bestMakespan.PSO" class="text-sm text-gray-600 mt-2">
            <span v-if="parseFloat(bestMakespan.ACO) === parseFloat(bestMakespan.PSO)">
              (Tied on makespan - {{ winner }} wins by execution time)
            </span>
            <span v-else>
              ({{ winner }} has better makespan: {{ winner === 'ACO' ? parseFloat(bestMakespan.ACO).toFixed(2) : parseFloat(bestMakespan.PSO).toFixed(2) }}s vs {{ winner === 'ACO' ? parseFloat(bestMakespan.PSO).toFixed(2) : parseFloat(bestMakespan.ACO).toFixed(2) }}s)
            </span>
          </div>
        </div>
      </div>

      <!-- AI Chat Assistant - Floating Design -->
      <div>
        <!-- Floating Chat Bubble -->
        <div
          v-if="!isChatOpen"
          @click="openChat"
          class="fixed bottom-6 right-6 w-14 h-14 bg-blue-500 text-white rounded-full shadow-none hover:bg-blue-600 cursor-pointer flex items-center justify-center z-50 transition-all duration-200 hover:scale-110"
          title="Ask Swarm Wave AI"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        </div>

        <!-- Draggable Chat Window -->
        <div
          v-if="isChatOpen"
          class="fixed bottom-6 right-6 bg-white rounded-xl border border-gray-200 shadow-none z-50 flex flex-col transition-all duration-300 ease-in-out"
          :class="{
            'translate-y-0 opacity-100': isChatOpen,
            'translate-y-full opacity-0': !isChatOpen,
            'cursor-move': isDragging,
            'cursor-se-resize': isResizing && resizeDirection === 'bottom-right',
            'cursor-sw-resize': isResizing && resizeDirection === 'bottom-left',
            'cursor-ne-resize': isResizing && resizeDirection === 'top-right',
            'cursor-nw-resize': isResizing && resizeDirection === 'top-left',
            'cursor-ew-resize': isResizing && (resizeDirection === 'right' || resizeDirection === 'left'),
            'cursor-ns-resize': isResizing && (resizeDirection === 'bottom' || resizeDirection === 'top'),
          }"
          :style="{
            transform: `translate(${draggablePosition.x}px, ${draggablePosition.y}px)`,
            width: `${chatWindowSize.width}px`,
            height: `${chatWindowSize.height}px`,
            minWidth: '320px',
            minHeight: '400px',
            maxWidth: '90vw',
            maxHeight: '90vh',
          }"
          ref="chatWindow"
        >
          <!-- Draggable Header -->
          <div
            class="flex items-center justify-between p-4 border-b border-gray-200 cursor-move"
            @mousedown="startDrag"
            @touchstart="startDrag"
          >
            <h3 class="text-lg font-semibold text-gray-900">Swarm Wave AI</h3>
            <div class="flex items-center space-x-2">
              <!-- Language Selector -->
              <select
                v-model="aiLanguage"
                class="text-sm px-2 py-1 border border-gray-300 rounded-md focus:ring-1 focus:ring-blue-500 bg-white"
              >
                <option value="English">EN</option>
                <option value="Indonesian">ID</option>
                <option value="Chinese">CN</option>
              </select>
              <!-- Close Button -->
              <button
                @click="closeChat"
                class="text-gray-500 hover:text-gray-700 p-1 rounded-md hover:bg-gray-100"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>

          <!-- Chat Body -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 bg-gray-50">
            <div
              v-if="chatHistory.length === 0"
              class="text-center text-gray-500 py-8"
            >
              <svg
                class="w-12 h-12 mx-auto mb-3 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
              <p class="text-sm">
                Ask me anything about your simulation results!
              </p>
            </div>

            <div v-else class="space-y-4">
              <div
                v-for="(message, index) in chatHistory"
                :key="index"
                :class="[
                  'flex',
                  message.role === 'user' ? 'justify-end' : 'justify-start',
                ]"
              >
                <div
                    :class="[
                      'rounded-lg shadow-sm',
                      message.role === 'user'
                        ? 'bg-blue-500 text-white ml-8 px-4 py-3 max-w-[85%]'
                        : 'bg-white border border-gray-200 text-gray-900 mr-4 max-w-[95%] overflow-hidden',
                      message.isStreaming ? 'streaming-message' : ''
                    ]"
                  >
                    <!-- User Message -->
                    <div v-if="message.role === 'user'" class="text-sm font-medium">
                      {{ message.content }}
                    </div>

                    <!-- Assistant Message with Enhanced Markdown -->
                    <div v-else class="ai-message-content px-4 py-3">
                      <div class="markdown-wrapper overflow-x-auto">
                        <div
                          class="markdown-content text-sm leading-relaxed min-w-0"
                          v-html="renderMarkdown(message.content)"
                        ></div>
                      </div>

                      <!-- Streaming indicator -->
                      <div v-if="message.isStreaming" class="flex items-center mt-3 text-xs text-gray-500">
                        <div class="flex space-x-1">
                          <div class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce"></div>
                          <div class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                          <div class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                        </div>
                        <span class="ml-2">AI is typing...</span>
                      </div>

                      <!-- Copy Button for AI responses -->
                      <div v-if="!message.isStreaming" class="mt-3 flex justify-end border-t border-gray-100 pt-2">
                        <button
                          @click="copyToClipboard(message.content)"
                          class="text-xs text-gray-500 hover:text-blue-600 flex items-center gap-1 px-2 py-1 rounded hover:bg-gray-50 transition-colors"
                          title="Copy response"
                        >
                          <svg
                            class="w-3 h-3"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                            />
                          </svg>
                          Copy
                        </button>
                      </div>
                    </div>
                  </div>
              </div>

              <!-- Loading Indicator -->
              <div v-if="aiLoading && !isStreaming" class="flex justify-start">
                <div
                  class="bg-white border border-gray-200 text-gray-900 px-3 py-2 rounded-lg"
                >
                  <div class="flex items-center space-x-1">
                    <div
                      class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    ></div>
                    <div
                      class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                      style="animation-delay: 0.1s"
                    ></div>
                    <div
                      class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                      style="animation-delay: 0.2s"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div
            v-if="aiError"
            class="px-4 py-2 bg-red-50 border-t border-red-200"
          >
            <div class="flex items-center">
              <svg
                class="w-4 h-4 text-red-500 mr-2"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                  clip-rule="evenodd"
                />
              </svg>
              <span class="text-xs text-red-600">{{ aiError }}</span>
            </div>
          </div>

          <!-- Resize Handles -->
          <!-- Left edge resize handle -->
          <div 
            class="absolute top-0 left-0 w-2 h-full cursor-ew-resize bg-transparent hover:bg-blue-200 hover:bg-opacity-30 transition-colors"
            @mousedown="startResize($event, 'left')"
            @touchstart="startResize($event, 'left')"
          ></div>
          
          <!-- Top edge resize handle -->
          <div 
            class="absolute top-0 left-0 w-full h-2 cursor-ns-resize bg-transparent hover:bg-blue-200 hover:bg-opacity-30 transition-colors"
            @mousedown="startResize($event, 'top')"
            @touchstart="startResize($event, 'top')"
          ></div>
          
          <!-- Right edge resize handle -->
          <div 
            class="absolute top-0 right-0 w-2 h-full cursor-ew-resize bg-transparent hover:bg-blue-200 hover:bg-opacity-30 transition-colors"
            @mousedown="startResize($event, 'right')"
            @touchstart="startResize($event, 'right')"
          ></div>
          
          <!-- Bottom edge resize handle -->
          <div 
            class="absolute bottom-0 left-0 w-full h-2 cursor-ns-resize bg-transparent hover:bg-blue-200 hover:bg-opacity-30 transition-colors"
            @mousedown="startResize($event, 'bottom')"
            @touchstart="startResize($event, 'bottom')"
          ></div>
          
          <!-- Corner resize handles -->
          <!-- Top-left corner -->
          <div 
            class="absolute top-0 left-0 w-4 h-4 cursor-nw-resize bg-transparent hover:bg-blue-200 hover:bg-opacity-50 transition-colors"
            @mousedown="startResize($event, 'top-left')"
            @touchstart="startResize($event, 'top-left')"
          ></div>
          
          <!-- Top-right corner -->
          <div 
            class="absolute top-0 right-0 w-4 h-4 cursor-ne-resize bg-transparent hover:bg-blue-200 hover:bg-opacity-50 transition-colors"
            @mousedown="startResize($event, 'top-right')"
            @touchstart="startResize($event, 'top-right')"
          ></div>
          
          <!-- Bottom-left corner -->
          <div 
            class="absolute bottom-0 left-0 w-4 h-4 cursor-sw-resize bg-transparent hover:bg-blue-200 hover:bg-opacity-50 transition-colors"
            @mousedown="startResize($event, 'bottom-left')"
            @touchstart="startResize($event, 'bottom-left')"
          ></div>
          
          <!-- Bottom-right corner -->
          <div 
            class="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize bg-transparent hover:bg-blue-200 hover:bg-opacity-50 transition-colors group"
            @mousedown="startResize($event, 'bottom-right')"
            @touchstart="startResize($event, 'bottom-right')"
          >
            <!-- Visual indicator -->
            <div class="absolute bottom-1 right-1 w-3 h-3">
              <svg class="w-3 h-3 text-gray-400 group-hover:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7l10 10M17 7l-10 10" />
              </svg>
            </div>
          </div>

          <!-- Footer Input -->
          <div class="p-4 border-t border-gray-200 bg-white">
            <div class="flex gap-2">
              <textarea
                v-model="userMessage"
                @keydown.enter.prevent="sendUserMessage"
                placeholder="Ask about your simulation..."
                class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:ring-1 focus:ring-blue-500 resize-none"
                rows="2"
                :disabled="aiLoading"
              ></textarea>
              <div class="flex flex-col gap-1">
                <button
                  @click="sendUserMessage"
                  :disabled="!userMessage.trim() || aiLoading"
                  class="px-3 py-1 bg-blue-500 text-white text-sm rounded-md hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  Send
                </button>
                <button
                  @click="clearChat"
                  class="px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded-md hover:bg-gray-300"
                  title="Clear chat"
                >
                  Clear
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-if="selectedAlgorithms.length === 0"
        class="bg-white rounded-xl shadow-lg p-6"
      >
        <div class="text-center py-12">
          <div class="text-gray-400 mb-4">
            <svg
              class="w-16 h-16 mx-auto"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            Select Algorithms to Compare
          </h3>
          <p class="text-gray-500">
            Choose ACO, PSO, or both to run parallel simulations and compare
            their performance.
          </p>
          <div
            class="mt-4 text-sm text-orange-600 bg-orange-50 border border-orange-200 rounded-md p-3"
          >
            <svg
              class="w-5 h-5 inline mr-1"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                clip-rule="evenodd"
              />
            </svg>
            <span class="font-medium">Warning:</span> No algorithms selected.
            Please choose at least one algorithm above to begin simulation.
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="mt-8 flex justify-center gap-4">
        <button
          @click="resetSimulation"
          class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition duration-200"
        >
          Reset Result
        </button>
        <button
          @click="$emit('back-to-table')"
          class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg transition duration-200"
        >
          Back to Dashboard
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, nextTick, onMounted, onUnmounted, computed } from "vue";
import Chart from "chart.js/auto";
import { marked } from "marked";
import { useAiChatStream } from "~/composables/useAiChatStream";

// Props & Emits
const props = defineProps({
  tasks: { type: Array, required: true },
  algorithms: { type: Array, default: () => [] },
});
const emit = defineEmits(["back-to-table", "edit-data"]);

// AI Chat Composable
const {
  chatHistory,
  aiLoading,
  aiError,
  aiLanguage,
  isStreaming,
  sendMessage,
  clearChat,
} = useAiChatStream();


// --- STATE MANAGEMENT ---
const selectedAlgorithms = ref([]);
const isRunning = ref(false);
const logs = ref({ ACO: [], PSO: [] });
const bestMakespan = ref({ ACO: null, PSO: null });
const executionTime = ref({ ACO: null, PSO: null });
const loadBalanceIndex = ref({ ACO: null, PSO: null });
const computationTime = ref({ ACO: null, PSO: null });
const status = ref({ ACO: "Idle", PSO: "Idle" });
const acoFinalAssignment = ref([]);
const psoFinalAssignment = ref([]);
const fullScheduleTable = ref({ aco: null, pso: null }); // Full schedule table untuk export
const fullResultData = ref({ aco: null, pso: null }); // Full result data untuk export lengkap
const agentInfoTable = ref({ aco: null, pso: null }); // Agent info table dengan heterogenitas
const chartCanvasACO = ref(null);
const chartCanvasPSO = ref(null);
const acoLogsContainer = ref(null);
const psoLogsContainer = ref(null);
let chartACO = null;
let chartPSO = null;
const toast = ref({ show: false, message: "", type: "error" });
const dataValidation = ref({ isValid: true, errors: [], warnings: [], summary: {} });
const dataLimit = ref(Math.max(1, Array.isArray(props.tasks) ? props.tasks.length : 1));
const showAllData = ref(false);

// Computed property for determining winner
const winner = computed(() => {
  if (!bestMakespan.value.ACO || !bestMakespan.value.PSO) {
    return "Pending";
  }
  
  const acoMakespan = parseFloat(bestMakespan.value.ACO);
  const psoMakespan = parseFloat(bestMakespan.value.PSO);
  
  // First priority: Best makespan (lower is better)
  if (acoMakespan < psoMakespan) {
    return "ACO";
  } else if (psoMakespan < acoMakespan) {
    return "PSO";
  }
  
  // If makespan is tied, use execution time as tiebreaker (lower is better)
  if (executionTime.value.ACO && executionTime.value.PSO) {
    const acoTime = parseFloat(executionTime.value.ACO);
    const psoTime = parseFloat(executionTime.value.PSO);
    
    if (acoTime < psoTime) {
      return "ACO";
    } else if (psoTime < acoTime) {
      return "PSO";
    }
  }
  
  // If still tied, use load balancing index as second tiebreaker (higher is better)
  if (loadBalanceIndex.value.ACO && loadBalanceIndex.value.PSO) {
    const acoBalance = parseFloat(loadBalanceIndex.value.ACO);
    const psoBalance = parseFloat(loadBalanceIndex.value.PSO);
    
    if (acoBalance > psoBalance) {
      return "ACO";
    } else if (psoBalance > acoBalance) {
      return "PSO";
    }
  }
  
  // If completely tied, default to ACO
  return "ACO";
});

const isWinner = computed(() => ({
  ACO: winner.value === "ACO",
  PSO: winner.value === "PSO"
}));

const parameters = reactive({
  num_default_agents: 10, n_iterations: 100, task_id_col: '', agent_id_col: '', dependency_col: '',
  random_seed: 42,
  n_ants: 50, alpha: 0.9, beta: 2.0, evaporation_rate: 0.3, pheromone_deposit: 100,
  n_particles: 50, w: 0.3, c1: 0.3, c2: 0.4,
  enable_dependencies: false
});
const expandedTasks = ref({ ACO: {}, PSO: {} });
const abortControllers = ref(new Map()); // Store abort controllers for each algorithm

// Toast notification function
const showToast = (message, type = 'error') => {
  toast.value = { show: true, message, type };
  setTimeout(() => {
    toast.value.show = false;
  }, 3000);
};

// --- COMPUTED PROPERTIES ---
const filteredTasks = computed(() => {
  if (!props.tasks || !Array.isArray(props.tasks) || props.tasks.length === 0) {
    return [];
  }
  if (showAllData.value) {
    return props.tasks;
  }
  const actualLimit = Math.min(Math.max(1, dataLimit.value), props.tasks.length);
  return props.tasks.slice(0, actualLimit);
});

const datasetHeaders = computed(() => {
  if (!props.tasks || !Array.isArray(props.tasks) || props.tasks.length === 0) {
    return [];
  }
  const firstTask = props.tasks[0];
  if (!firstTask || typeof firstTask !== 'object') {
    return [];
  }
  return Object.keys(firstTask);
});

// Detect dependency columns automatically
const dependencyColumn = computed(() => {
  const headers = datasetHeaders.value;
  const dependencyFields = ['dependencies', 'depends_on', 'prerequisites', 'requires'];
  return headers.find(header => 
    dependencyFields.some(field => header.toLowerCase().includes(field.toLowerCase()))
  ) || '';
});

// Check if dependency column exists
const hasDependencyColumn = computed(() => {
  return dependencyColumn.value !== '';
});

// Preview count for data limit display
const previewCount = computed(() => {
  if (!props.tasks || !Array.isArray(props.tasks) || props.tasks.length === 0) {
    return 0;
  }
  if (showAllData.value) {
    return props.tasks.length;
  }
  // Ensure minimum 1 and maximum available tasks
  return Math.max(1, Math.min(dataLimit.value, props.tasks.length));
});

// Auto-set task_id_col to the first column header when data changes
watch(datasetHeaders, (newHeaders) => {
  if (newHeaders.length > 0 && (!parameters.task_id_col || parameters.task_id_col === '')) {
    parameters.task_id_col = newHeaders[0];
  }
}, { immediate: true });

// Auto-set dependency_col when dependency column is detected
watch([datasetHeaders, dependencyColumn], ([newHeaders, newDependencyCol]) => {
  if (newDependencyCol && (!parameters.dependency_col || parameters.dependency_col === '')) {
    parameters.dependency_col = newDependencyCol;
    parameters.enable_dependencies = true; // Auto-enable when dependency column found
  } else if (!newDependencyCol && parameters.dependency_col) {
    // Reset if dependency column is no longer available
    parameters.dependency_col = '';
    parameters.enable_dependencies = false;
  }
}, { immediate: true });

// Also watch for props.tasks changes to ensure columns are set
watch(() => props.tasks, (newTasks) => {
  if (newTasks && newTasks.length > 0) {
    const headers = datasetHeaders.value;
    if (headers.length > 0 && (!parameters.task_id_col || parameters.task_id_col === '')) {
      parameters.task_id_col = headers[0];
    }
    
    // Auto-set dependency column if available
    const depCol = dependencyColumn.value;
    if (depCol && (!parameters.dependency_col || parameters.dependency_col === '')) {
      parameters.dependency_col = depCol;
      parameters.enable_dependencies = true;
    }
  }
}, { immediate: true });

// --- SIMULATION LOGIC (STREAMING) ---

const resetSimulationStateForAlgo = (algo) => {
  status.value[algo] = "Idle";
  logs.value[algo] = [];
  bestMakespan.value[algo] = null;
  executionTime.value[algo] = null;
  loadBalanceIndex.value[algo] = null;
  computationTime.value[algo] = null;
  if (algo === 'ACO') acoFinalAssignment.value = [];
  if (algo === 'PSO') psoFinalAssignment.value = [];

  const chart = algo === 'ACO' ? chartACO : chartPSO;
  if (chart) {
    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    chart.data.datasets[1].data = [];
    chart.update();
  } else {
    console.warn(`Chart for ${algo} not initialized yet`);
  }
};

const runSimulation = async () => {
  validateData();
  if (!filteredTasks.value || filteredTasks.value.length === 0) {
    showToast("Please add at least one task to the data.", 'error');
    return;
  }
  if (!dataValidation.value.isValid || selectedAlgorithms.value.length === 0) {
    showToast("Please select an algorithm and ensure data is valid.", 'error');
    return;
  }

  await resetSimulation();

  isRunning.value = true;
  
  // Ensure charts are initialized for selected algorithms
  await nextTick();
  initCharts();
  await nextTick();
  
  // Clear any existing abort controllers
  abortControllers.value.clear();

  const runningSims = selectedAlgorithms.value.map(async (algorithm) => {
    const requestBody = {
      algorithm: algorithm,
      tasks: filteredTasks.value,
      parameters: { ...parameters }
    };

    // Create abort controller for this algorithm
    const controller = new AbortController();
    abortControllers.value.set(algorithm, controller);

    const config = useRuntimeConfig();

    try {
      const response = await fetch(`${config.public.API_URL}/stream_scheduling`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
        signal: controller.signal // Add abort signal
      });

      if (!response.ok) {
        let errorMessage = response.statusText;
        try {
          const errorData = await response.json();
          if (errorData && errorData.error) {
            errorMessage = errorData.error;
          }
        } catch (e) {
          // Fallback to status text
        }
        throw new Error(errorMessage);
      }

      if (!response.body) {
        throw new Error("Server error: No response body");
      }

      status.value[algorithm] = "Running...";
      const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
      let buffer = ''; // Buffer for incomplete JSON data

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        // Check if request was aborted
        if (controller.signal.aborted) {
          break;
        }
        
        // Add new chunk to buffer
        buffer += value;
        
        // Split by double newlines to get complete SSE messages
        const messages = buffer.split('\n\n');
        
        // Keep the last incomplete message in buffer
        buffer = messages.pop() || '';
        
        // Process complete messages
        for (const message of messages) {
          if (message.startsWith('data:')) {
            const jsonData = message.substring(5).trim();
            if (jsonData && jsonData !== '') {
              try {
                const parsedData = JSON.parse(jsonData);
                handleStreamEvent(algorithm, parsedData);
              } catch (jsonError) {
                console.warn(`JSON parse error for ${algorithm}:`, jsonError.message);
                console.warn('Problematic data:', jsonData);
                // Log the error but continue processing
                logs.value[algorithm].push(`⚠️ Data parsing warning: ${jsonError.message}`);
              }
            }
          }
        }
      }
      
      // Process any remaining buffer data
      if (buffer.trim() && buffer.startsWith('data:')) {
        const jsonData = buffer.substring(5).trim();
        if (jsonData) {
          try {
            const parsedData = JSON.parse(jsonData);
            handleStreamEvent(algorithm, parsedData);
          } catch (jsonError) {
            console.warn(`Final buffer JSON parse error for ${algorithm}:`, jsonError.message);
            logs.value[algorithm].push(`⚠️ Final data parsing warning: ${jsonError.message}`);
          }
        }
      }
    } catch (error) {
      if (error.name === 'AbortError') {
        // Don't show error for user-initiated stops
        console.log(`${algorithm} simulation was aborted by user`);
      } else {
        console.error(`Error with ${algorithm} simulation:`, error);
        logs.value[algorithm].push(`❌ Simulation failed: ${error.message}`);
        status.value[algorithm] = "Failed";
      }
    } finally {
      // Remove abort controller when done
      abortControllers.value.delete(algorithm);
    }
  });

  await Promise.all(runningSims);
  
  // Clear any remaining abort controllers
  abortControllers.value.clear();
  isRunning.value = false;
};

const handleStreamEvent = (algorithm, data) => {
  try {
    // Validate data structure
    if (!data || typeof data !== 'object') {
      console.warn(`Invalid data received for ${algorithm}:`, data);
      return;
    }

    const chart = algorithm === 'ACO' ? chartACO : chartPSO;
    const logsContainer = algorithm === 'ACO' ? acoLogsContainer.value : psoLogsContainer.value;

    const processLog = (message) => {
        if (message && typeof message === 'string') {
          logs.value[algorithm].push(message);
          nextTick(() => {
              if (logsContainer) {
                  logsContainer.scrollTop = logsContainer.scrollHeight;
              }
          });
        }
    };

    switch (data.type) {
      case 'log':
      case 'start':
        if (data.message) {
          processLog(data.message);
        }
        break;
      
      case 'iteration':
        if (data.log_message) {
          processLog(data.log_message);
        }
        if (typeof data.makespan === 'number') {
          bestMakespan.value[algorithm] = data.makespan;
        }
        if (chart && typeof data.iteration === 'number' && typeof data.makespan === 'number') {
          try {
            chart.data.labels.push(data.iteration);
            chart.data.datasets[0].data.push(data.makespan);
            // Only show the best point marker
            const bestVal = Math.min(...chart.data.datasets[0].data);
            const bestIndex = chart.data.datasets[0].data.indexOf(bestVal);
            chart.data.datasets[1].data = chart.data.datasets[0].data.map((val, idx) => idx === bestIndex ? val : null);

            chart.update('none'); // Use 'none' for smoother updates
          } catch (chartError) {
            console.warn(`Chart update error for ${algorithm}:`, chartError.message);
          }
        } else if (!chart && typeof data.iteration === 'number' && typeof data.makespan === 'number') {
          // Chart not available, try to initialize it
          console.warn(`Chart for ${algorithm} not available during iteration update, attempting to initialize...`);
          nextTick(() => {
            initCharts();
          });
        }
        break;

      case 'done':
        if (data.log_message) {
          processLog(data.log_message);
        }
        if (typeof data.makespan === 'number') {
          bestMakespan.value[algorithm] = data.makespan;
        }
        if (typeof data.computation_time === 'number') {
          computationTime.value[algorithm] = data.computation_time;
        }
        if (data.schedule && Array.isArray(data.schedule)) {
          try {
            const finalAssignments = transformAssignmentData(data.schedule);
            if (algorithm === 'ACO') acoFinalAssignment.value = finalAssignments;
            if (algorithm === 'PSO') psoFinalAssignment.value = finalAssignments;
          } catch (transformError) {
            console.warn(`Data transformation error for ${algorithm}:`, transformError.message);
            processLog(`⚠️ Assignment data processing warning: ${transformError.message}`);
          }
        }
        break;

      case 'final_metrics':
        if (typeof data.total_execution_time === 'number') {
          executionTime.value[algorithm] = data.total_execution_time;
        }
        if (typeof data.computation_time === 'number') {
          computationTime.value[algorithm] = data.computation_time;
        }
        if (typeof data.load_balance_index === 'number') {
          loadBalanceIndex.value[algorithm] = data.load_balance_index;
        }
        
        // Simpan full_schedule_table untuk export
        if (data.full_schedule_table) {
          if (algorithm === 'ACO') {
            fullScheduleTable.value.aco = data.full_schedule_table;
          } else if (algorithm === 'PSO') {
            fullScheduleTable.value.pso = data.full_schedule_table;
          }
          processLog(`Full schedule table received: ${data.full_schedule_table.total_rows} rows`);
        }
        
        // Simpan full_result untuk export lengkap
        if (data.full_result) {
          if (algorithm === 'ACO') {
            fullResultData.value.aco = data.full_result;
          } else if (algorithm === 'PSO') {
            fullResultData.value.pso = data.full_result;
          }
          processLog(`Full result data saved for export`);
        }
        
        // Simpan agent_info_table untuk export agent heterogenitas
        if (data.agent_info_table) {
          if (algorithm === 'ACO') {
            agentInfoTable.value.aco = data.agent_info_table;
          } else if (algorithm === 'PSO') {
            agentInfoTable.value.pso = data.agent_info_table;
          }
          processLog(`Agent info table received: ${data.agent_info_table.total_rows} agents`);
        }
        
        status.value[algorithm] = "Completed";
        break;

      case 'error':
        const errorMessage = data.message || 'Unknown error occurred';
        processLog(`❌ ERROR: ${errorMessage}`);
        status.value[algorithm] = "Failed";
        break;
        
      default:
        console.warn(`Unknown event type for ${algorithm}:`, data.type, data);
        break;
    }
  } catch (error) {
    console.error(`Error handling stream event for ${algorithm}:`, error);
    logs.value[algorithm].push(`⚠️ Event processing error: ${error.message}`);
  }
};

const transformAssignmentData = (schedule) => {
  if (!schedule || !Array.isArray(schedule) || schedule.length === 0) {
    console.warn('Invalid or empty schedule data:', schedule);
    return [];
  }
  
  const agentMap = new Map();

  try {
    schedule.forEach((task, index) => {
      // Validate task structure
      if (!task || typeof task !== 'object') {
        console.warn(`Invalid task at index ${index}:`, task);
        return;
      }
      
      if (!task.hasOwnProperty('agent_id') || !task.hasOwnProperty('task_id')) {
        console.warn(`Missing required fields in task at index ${index}:`, task);
        return;
      }

      const agentId = task.agent_id;
      const taskId = task.task_id;
      const finishTime = typeof task.finish_time === 'number' ? task.finish_time : 0;
      
      if (!agentMap.has(agentId)) {
        agentMap.set(agentId, { tasks: [], finish_time: 0 });
      }
      
      const agentData = agentMap.get(agentId);
      agentData.tasks.push(taskId);
      agentData.finish_time = Math.max(agentData.finish_time, finishTime);
    });

    return Array.from(agentMap.entries()).map(([agent, data]) => ({
      agent: agent,
      tasks: data.tasks,
      total_time: data.finish_time
    }));
  } catch (error) {
    console.error('Error transforming assignment data:', error);
    return [];
  }
};

// --- UI & HELPER FUNCTIONS ---

const initCharts = () => {
    const createChart = (canvasRef, label, color) => {
        if (!canvasRef.value) {
            console.warn(`Canvas ref for ${label} not available yet`);
            return null;
        }
        
        // Destroy existing chart on this canvas first
        const existingChart = Chart.getChart(canvasRef.value);
        if (existingChart) {
            existingChart.destroy();
        }
        
        const ctx = canvasRef.value.getContext("2d");
        return new Chart(ctx, {
            type: "line",
            data: {
                labels: [],
                datasets: [
                    { label: `${label} Best Makespan`, data: [], borderColor: color, backgroundColor: 'transparent', tension: 0.1, fill: true },
                    { label: "Best Point", data: [], backgroundColor: color, borderColor: color, pointRadius: 5, pointHoverRadius: 7, showLine: false }
                ]
            },
            options: { 
                responsive: true, 
                maintainAspectRatio: false,
                animation: { duration: 200 },
                scales: { 
                    y: { beginAtZero: false, title: { display: true, text: "Makespan" } }, 
                    x: { title: { display: true, text: "Iteration" } } 
                } 
            }
        });
    };
    
    // Destroy existing charts
    if (chartACO) {
        chartACO.destroy();
        chartACO = null;
    }
    if (chartPSO) {
        chartPSO.destroy();
        chartPSO = null;
    }
    
    // Initialize charts for selected algorithms only
    nextTick(() => {
        if (selectedAlgorithms.value.includes('ACO')) {
            chartACO = createChart(chartCanvasACO, 'ACO', 'rgb(59, 130, 246)');
        }
        if (selectedAlgorithms.value.includes('PSO')) {
            chartPSO = createChart(chartCanvasPSO, 'PSO', 'rgb(239, 68, 68)');
        }
    });
};

const validateDataLimitInput = () => {
  // Ensure dataLimit is never 0 or negative
  if (dataLimit.value <= 0) {
    dataLimit.value = 1;
  } else if (dataLimit.value > props.tasks.length) {
    dataLimit.value = props.tasks.length;
  }
};

const validateData = () => {
  const errors = [];
  const warnings = [];
  
  if (!props.tasks || !Array.isArray(props.tasks)) {
    errors.push("Invalid tasks data format.");
  } else if (props.tasks.length === 0) {
    errors.push("No tasks available.");
  } else {
    // Check if all tasks have consistent structure
    const firstTask = props.tasks[0];
    if (!firstTask || typeof firstTask !== 'object') {
      errors.push("Invalid task data structure.");
    } else {
      const expectedKeys = Object.keys(firstTask);
      const inconsistentTasks = props.tasks.filter(task => {
        if (!task || typeof task !== 'object') return true;
        const taskKeys = Object.keys(task);
        return expectedKeys.length !== taskKeys.length || 
               !expectedKeys.every(key => taskKeys.includes(key));
      });
      
      if (inconsistentTasks.length > 0) {
        warnings.push(`${inconsistentTasks.length} tasks have inconsistent structure.`);
      }
    }
  }
  
  dataValidation.value = {
    isValid: errors.length === 0,
    errors,
    warnings,
  };
};

const resetSimulation = async () => {
  // Reset ALL algorithms, not just selected ones
  ['ACO', 'PSO'].forEach(resetSimulationStateForAlgo);
  isRunning.value = false;
};

const stopSimulation = () => {
  // Abort all running requests
  abortControllers.value.forEach((controller, algorithm) => {
    controller.abort();
    logs.value[algorithm].push(`🛑 Simulation stopped by user`);
    status.value[algorithm] = "Stopped";
  });
  
  // Clear abort controllers
  abortControllers.value.clear();
  isRunning.value = false;
  
  showToast("Simulation stopped", 'info');
};

const editData = () => {
  // Send the original/raw tasks data back to parent for editing, not filtered data
  emit("edit-data", props.tasks);
};

const exportData = (algorithm, format) => {
    const algoKey = algorithm.toLowerCase();
    const fullResult = fullResultData.value[algoKey];
    const scheduleTable = fullScheduleTable.value[algoKey];
    
    // Fallback ke assignment lama jika full data tidak tersedia
    const assignment = algorithm === 'ACO' ? acoFinalAssignment.value : psoFinalAssignment.value;
    
    if (!fullResult && (!assignment || assignment.length === 0)) {
        showToast(`No data to export for ${algorithm}`, 'info');
        return;
    }

    let content = '';
    let mimeType = '';
    let fileExtension = '';
    const timestamp = new Date().toISOString().replace(/:/g, '-').split('.')[0];

    if (format === 'json') {
        // Export full result data (lebih lengkap)
        if (fullResult) {
            content = JSON.stringify(fullResult, null, 2);
        } else {
            // Fallback ke format lama
            content = JSON.stringify(assignment, null, 2);
        }
        mimeType = 'application/json';
        fileExtension = 'json';
    } else { // csv
        if (scheduleTable && scheduleTable.data) {
            // Export dengan format rapi untuk Numbers/Excel
            const csvLines = [];
            const agentInfo = agentInfoTable.value[algoKey];
            
            // Metadata header
            if (fullResult) {
                csvLines.push(`${fullResult.algorithm} Schedule Export`);
                csvLines.push(`Generated,${fullResult.timestamp || timestamp}`);
                csvLines.push(`Makespan,${fullResult.makespan || 'N/A'}`);
                csvLines.push(`Load Balance Index,${fullResult.load_balance_index || 'N/A'}`);
                csvLines.push(`Computation Time (ms),${fullResult.computation_time || 'N/A'}`);
                csvLines.push(`Total Tasks,${fullResult.total_tasks || scheduleTable.total_rows}`);
                csvLines.push(`Total Agents,${fullResult.total_agents || 'N/A'}`);
                csvLines.push(''); // Empty line separator
            }
            
            // Agent Info Table (Heterogenitas)
            if (agentInfo && agentInfo.data) {
                csvLines.push('AGENT HETEROGENITAS');
                csvLines.push(agentInfo.columns.join(','));
                agentInfo.data.forEach(row => {
                    csvLines.push(row.join(','));
                });
                csvLines.push(''); // Empty line separator
            }
            
            // Group data by agent
            const agentGroups = {};
            const agentIdIndex = scheduleTable.columns.indexOf('agent_id');
            
            scheduleTable.data.forEach(row => {
                const agentId = row[agentIdIndex];
                if (!agentGroups[agentId]) {
                    agentGroups[agentId] = [];
                }
                agentGroups[agentId].push(row);
            });
            
            // Sort agents naturally
            const sortedAgents = Object.keys(agentGroups).sort((a, b) => {
                const numA = parseInt(a.match(/\d+/) || 0);
                const numB = parseInt(b.match(/\d+/) || 0);
                return numA - numB;
            });
            
            // Export per agent dengan format clean
            sortedAgents.forEach((agentId, index) => {
                // Get agent info untuk header yang lebih informatif
                let agentHeader = agentId;
                if (agentInfo && agentInfo.data) {
                    const agentData = agentInfo.data.find(a => a[0] === agentId);
                    if (agentData) {
                        const [id, type, capacity, efficiency] = agentData;
                        agentHeader = `${id} (${type} - Capacity: ${capacity} - Efficiency: ${efficiency})`;
                    }
                }
                
                csvLines.push(agentHeader);
                csvLines.push(scheduleTable.columns.join(','));
                
                // Agent data
                agentGroups[agentId].forEach(row => {
                    const formattedRow = row.map(cell => {
                        if (typeof cell === 'string' && isNaN(cell)) {
                            return cell; // No quotes for cleaner look
                        }
                        return cell;
                    }).join(',');
                    csvLines.push(formattedRow);
                });
                
                // Agent summary
                const totalTasks = agentGroups[agentId].length;
                const finishTimeIndex = scheduleTable.columns.indexOf('finish_time');
                const maxFinishTime = Math.max(...agentGroups[agentId].map(r => r[finishTimeIndex]));
                csvLines.push(`${agentId} Total,${totalTasks} tasks,Total Time,${maxFinishTime.toFixed(2)}`);
                csvLines.push(''); // Empty line between agents
            });
            
            content = csvLines.join('\n');
        } else {
            // Fallback ke format lama
            const headers = ["Agent", "Tasks", "Total Time"];
            const rows = assignment.map(row => [
                `"${row.agent}"`,
                `"${Array.isArray(row.tasks) ? row.tasks.join(";") : row.tasks}"`,
                `"${row.total_time}"`
            ]);
            content = [headers.join(","), ...rows.map(row => row.join(","))].join("\n");
        }
        mimeType = 'text/csv;charset=utf-8;';
        fileExtension = 'csv';
    }

    const blob = new Blob([content], { type: mimeType });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${algorithm.toLowerCase()}_schedule_${timestamp}.${fileExtension}`;
    link.click();
    URL.revokeObjectURL(link.href);
    
    showToast(`${algorithm} data exported successfully`, 'success');
};

const exportJSON = (algorithm) => exportData(algorithm, 'json');
const exportCSV = (algorithm) => exportData(algorithm, 'csv');

const toggleTaskExpansion = (algorithm, agentId) => {
  if (!expandedTasks.value[algorithm]) expandedTasks.value[algorithm] = {};
  expandedTasks.value[algorithm][agentId] = !expandedTasks.value[algorithm][agentId];
};

// --- LIFECYCLE HOOKS ---
onMounted(() => {
  if (props.algorithms && props.algorithms.length > 0) {
    selectedAlgorithms.value = [...props.algorithms];
  }
  validateData();
  initCharts();
});

onUnmounted(() => {
  // Cleanup: abort all running requests when component unmounts
  abortControllers.value.forEach((controller) => {
    controller.abort();
  });
  abortControllers.value.clear();
});

watch(props.tasks, () => {
    validateData();
    dataLimit.value = props.tasks.length;
}, { deep: true, immediate: true });

// Watch dataLimit to prevent 0 or negative values
watch(dataLimit, (newValue) => {
  if (newValue <= 0) {
    dataLimit.value = 1;
  } else if (newValue > props.tasks.length) {
    dataLimit.value = props.tasks.length;
  }
}, { immediate: true });

// Watch for changes in selected algorithms to reinitialize charts
watch(selectedAlgorithms, () => {
    nextTick(() => {
        initCharts();
    });
}, { deep: true });

// --- AI & CHAT WINDOW (UNCHANGED) ---
const userMessage = ref("");
const isChatOpen = ref(false);
const draggablePosition = ref({ x: 0, y: 0 });
const isDragging = ref(false);
const dragStart = ref({ x: 0, y: 0 });
const chatWindow = ref(null);
const chatWindowSize = ref({ width: 480, height: 520 });
const isResizing = ref(false);
const resizeDirection = ref('corner');
const resizeStart = ref({ x: 0, y: 0, width: 0, height: 0 });
const messagesContainer = ref(null);

const openChat = () => isChatOpen.value = true;
const closeChat = () => isChatOpen.value = false;
const renderMarkdown = (text) => {
  const html = marked(text || '');
  // Wrap tables in scrollable div
  return html.replace(/<table/g, '<div class="table-scroll-wrapper"><table')
             .replace(/<\/table>/g, '</table></div>');
};
const copyToClipboard = (text) => navigator.clipboard.writeText(text).then(() => showToast('Copied to clipboard', 'success'));

const getDataTypes = () => {
  if (!filteredTasks.value.length || !datasetHeaders.value.length) return {};
  
  const types = {};
  const sampleSize = Math.min(10, filteredTasks.value.length); // Check first 10 rows
  
  datasetHeaders.value.forEach(header => {
    const sampleValues = filteredTasks.value.slice(0, sampleSize)
      .map(task => task[header])
      .filter(val => val !== null && val !== undefined && val !== '');
    
    if (sampleValues.length === 0) {
      types[header] = 'empty';
      return;
    }
    
    // Check if all values are numbers
    const numericValues = sampleValues.filter(val => !isNaN(val) && isFinite(val));
    if (numericValues.length === sampleValues.length) {
      // Check if integers or floats
      const hasDecimals = numericValues.some(val => val % 1 !== 0);
      types[header] = hasDecimals ? 'float' : 'integer';
    } else {
      // Check for common patterns
      const stringValues = sampleValues.map(val => String(val).toLowerCase());
      const uniqueValues = [...new Set(stringValues)];
      
      if (uniqueValues.length <= 5 && sampleValues.length > 5) {
        types[header] = 'categorical';
      } else if (stringValues.some(val => val.includes('-') && val.length === 10)) {
        types[header] = 'date';
      } else {
        types[header] = 'text';
      }
    }
  });
  
  return types;
};

const sendUserMessage = async () => {
    if (!userMessage.value.trim() && chatHistory.value.length === 0) {
        userMessage.value = "Explain these simulation results.";
    }
    if (!userMessage.value.trim()) return;

    // Prepare data specification
    const dataSpecification = {
        totalRows: filteredTasks.value.length,
        totalColumns: datasetHeaders.value.length,
        columns: datasetHeaders.value,
        sampleData: filteredTasks.value.slice(0, 3), // First 3 rows as sample
        dataTypes: getDataTypes(),
        dataLimitations: {
            originalRows: props.tasks.length,
            filteredRows: filteredTasks.value.length,
            showAllData: showAllData.value,
            dataLimit: dataLimit.value
        }
    };

    // Prepare algorithm parameters
    const algorithmParameters = {
        common: {
            num_default_agents: parameters.num_default_agents,
            n_iterations: parameters.n_iterations,
            task_id_col: parameters.task_id_col,
            agent_id_col: parameters.agent_id_col
        },
        aco: selectedAlgorithms.value.includes('ACO') ? {
            alpha: parameters.alpha,
            beta: parameters.beta,
            evaporation_rate: parameters.evaporation_rate,
            pheromone_deposit: parameters.pheromone_deposit,
            n_ants: parameters.n_ants
        } : null,
        pso: selectedAlgorithms.value.includes('PSO') ? {
            n_particles: parameters.n_particles,
            w: parameters.w,
            c1: parameters.c1,
            c2: parameters.c2
        } : null
    };

    const simulationData = {
        aco: selectedAlgorithms.value.includes('ACO') ? {
            bestMakespan: bestMakespan.value.ACO,
            executionTime: executionTime.value.ACO,
            loadBalanceIndex: loadBalanceIndex.value.ACO,
            finalAssignment: acoFinalAssignment.value,
            totalAgents: parameters.num_default_agents,
            totalTasks: filteredTasks.value.length,
            parameters: algorithmParameters.aco
        } : null,
        pso: selectedAlgorithms.value.includes('PSO') ? {
            bestMakespan: bestMakespan.value.PSO,
            executionTime: executionTime.value.PSO,
            loadBalanceIndex: loadBalanceIndex.value.PSO,
            finalAssignment: psoFinalAssignment.value,
            totalAgents: parameters.num_default_agents,
            totalTasks: filteredTasks.value.length,
            parameters: algorithmParameters.pso
        } : null,
        dataSpecification: dataSpecification,
        algorithmParameters: algorithmParameters
    };
    
    await sendMessage(userMessage.value, simulationData, selectedAlgorithms.value.join('_'));
    userMessage.value = "";
};

const startDrag = (event) => {
  isDragging.value = true;
  const clientX = event.clientX || event.touches[0].clientX;
  const clientY = event.clientY || event.touches[0].clientY;
  dragStart.value = { x: clientX - draggablePosition.value.x, y: clientY - draggablePosition.value.y };
  
  const handleMove = (e) => {
    if (!isDragging.value) return;
    const moveX = e.clientX || e.touches[0].clientX;
    const moveY = e.clientY || e.touches[0].clientY;
    draggablePosition.value = { x: moveX - dragStart.value.x, y: moveY - dragStart.value.y };
  };
  const handleUp = () => {
    isDragging.value = false;
    document.removeEventListener('mousemove', handleMove);
    document.removeEventListener('mouseup', handleUp);
    document.removeEventListener('touchmove', handleMove);
    document.removeEventListener('touchend', handleUp);
  };
  
  document.addEventListener('mousemove', handleMove);
  document.addEventListener('mouseup', handleUp);
  document.addEventListener('touchmove', handleMove);
  document.addEventListener('touchend', handleUp);
};

const startResize = (event, direction = 'bottom-right') => {
  isResizing.value = true;
  resizeDirection.value = direction;
  const clientX = event.clientX || event.touches[0].clientX;
  const clientY = event.clientY || event.touches[0].clientY;
  resizeStart.value = { 
    x: clientX, 
    y: clientY, 
    width: chatWindowSize.value.width, 
    height: chatWindowSize.value.height,
    startPosX: draggablePosition.value.x,
    startPosY: draggablePosition.value.y
  };
  
  const handleMove = (e) => {
    if (!isResizing.value) return;
    const moveX = e.clientX || e.touches[0].clientX;
    const moveY = e.clientY || e.touches[0].clientY;
    const deltaX = moveX - resizeStart.value.x;
    const deltaY = moveY - resizeStart.value.y;
    
    let newWidth = chatWindowSize.value.width;
    let newHeight = chatWindowSize.value.height;
    let newPosX = draggablePosition.value.x;
    let newPosY = draggablePosition.value.y;
    
    const minWidth = 320;
    const minHeight = 400;
    const maxWidth = window.innerWidth * 0.9;
    const maxHeight = window.innerHeight * 0.9;
    
    // Apply changes based on resize direction
    switch (resizeDirection.value) {
      case 'right':
        newWidth = Math.max(minWidth, Math.min(maxWidth, resizeStart.value.width + deltaX));
        break;
      case 'left':
        newWidth = Math.max(minWidth, Math.min(maxWidth, resizeStart.value.width - deltaX));
        if (newWidth > minWidth) {
          newPosX = resizeStart.value.startPosX + deltaX;
        }
        break;
      case 'bottom':
        newHeight = Math.max(minHeight, Math.min(maxHeight, resizeStart.value.height + deltaY));
        break;
      case 'top':
        newHeight = Math.max(minHeight, Math.min(maxHeight, resizeStart.value.height - deltaY));
        if (newHeight > minHeight) {
          newPosY = resizeStart.value.startPosY + deltaY;
        }
        break;
      case 'bottom-right':
        newWidth = Math.max(minWidth, Math.min(maxWidth, resizeStart.value.width + deltaX));
        newHeight = Math.max(minHeight, Math.min(maxHeight, resizeStart.value.height + deltaY));
        break;
      case 'bottom-left':
        newWidth = Math.max(minWidth, Math.min(maxWidth, resizeStart.value.width - deltaX));
        newHeight = Math.max(minHeight, Math.min(maxHeight, resizeStart.value.height + deltaY));
        if (newWidth > minWidth) {
          newPosX = resizeStart.value.startPosX + deltaX;
        }
        break;
      case 'top-right':
        newWidth = Math.max(minWidth, Math.min(maxWidth, resizeStart.value.width + deltaX));
        newHeight = Math.max(minHeight, Math.min(maxHeight, resizeStart.value.height - deltaY));
        if (newHeight > minHeight) {
          newPosY = resizeStart.value.startPosY + deltaY;
        }
        break;
      case 'top-left':
        newWidth = Math.max(minWidth, Math.min(maxWidth, resizeStart.value.width - deltaX));
        newHeight = Math.max(minHeight, Math.min(maxHeight, resizeStart.value.height - deltaY));
        if (newWidth > minWidth) {
          newPosX = resizeStart.value.startPosX + deltaX;
        }
        if (newHeight > minHeight) {
          newPosY = resizeStart.value.startPosY + deltaY;
        }
        break;
    }
    
    chatWindowSize.value = {
      width: newWidth,
      height: newHeight,
    };
    
    draggablePosition.value = {
      x: newPosX,
      y: newPosY,
    };
  };
  
  const handleUp = () => {
    isResizing.value = false;
    resizeDirection.value = 'bottom-right';
    document.removeEventListener('mousemove', handleMove);
    document.removeEventListener('mouseup', handleUp);
    document.removeEventListener('touchmove', handleMove);
    document.removeEventListener('touchend', handleUp);
  };
  
  document.addEventListener('mousemove', handleMove);
  document.addEventListener('mouseup', handleUp);
  document.addEventListener('touchmove', handleMove);
  document.addEventListener('touchend', handleUp);
};

watch(chatHistory, () => {
    nextTick(() => {
        if(messagesContainer.value) {
            messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
        }
    });
}, { deep: true });

</script>

<style scoped>
/* Custom scrollbar for logs */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Toast animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

/* Chat Markdown Styling */
.markdown-content {
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  color: #1f2937;
}

.markdown-content h1 {
  font-size: 1.5rem;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

.markdown-content h2 {
  font-size: 1.25rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.25rem;
}

.markdown-content h3 {
  font-size: 1.125rem;
}

.markdown-content h4 {
  font-size: 1rem;
}

.markdown-content p {
  margin-bottom: 1rem;
  color: #374151;
}

.markdown-content ul,
.markdown-content ol {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.markdown-content li {
  margin-bottom: 0.25rem;
  color: #374151;
}

.markdown-content strong {
  font-weight: 600;
  color: #1f2937;
}

.markdown-content em {
  font-style: italic;
  color: #4b5563;
}

.markdown-content code {
  background-color: #f3f4f6;
  color: #dc2626;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.875rem;
}

.markdown-content pre {
  background-color: #1f2937;
  color: #f9fafb;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin-bottom: 1rem;
}

.markdown-content pre code {
  background: none;
  color: inherit;
  padding: 0;
  font-size: 0.875rem;
}

.markdown-content blockquote {
  border-left: 4px solid #3b82f6;
  padding-left: 1rem;
  margin: 1rem 0;
  background-color: #f8fafc;
  color: #475569;
  font-style: italic;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 0;
  font-size: 0.825rem;
  background: white;
  min-width: max-content;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid #e5e7eb;
  padding: 0.4rem 0.5rem;
  text-align: left;
  vertical-align: top;
  line-height: 1.3;
  white-space: nowrap;
}

.markdown-content th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #1f2937;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.markdown-content td {
  background-color: #ffffff;
  color: #374151;
  font-size: 0.8rem;
}

.markdown-content tr:nth-child(even) td {
  background-color: #f9fafb;
}

.markdown-content a {
  color: #3b82f6;
  text-decoration: underline;
}

.markdown-content a:hover {
  color: #2563eb;
}

.markdown-content hr {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 1.5rem 0;
}

/* Streaming animation */
.streaming-message {
  position: relative;
}

.streaming-message::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
  animation: shimmer 2s infinite;
  border-radius: inherit;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Enhanced spacing for chat messages */
.ai-message-content {
  max-width: none;
}

.ai-message-content .markdown-wrapper {
  max-width: 100%;
}

.ai-message-content .markdown-content > *:first-child {
  margin-top: 0;
}

.ai-message-content .markdown-content > *:last-child {
  margin-bottom: 0;
}

/* Table scroll wrapper - isolated scrolling */
.table-scroll-wrapper {
  overflow-x: auto;
  margin: 1rem 0;
  border-radius: 0.375rem;
  border: 1px solid #e5e7eb;
  max-width: 100%;
}

.table-scroll-wrapper::-webkit-scrollbar {
  height: 6px;
}

.table-scroll-wrapper::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.table-scroll-wrapper::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.table-scroll-wrapper::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
