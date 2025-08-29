<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <!-- Toast Notification -->
    <div 
      v-if="toast.show"
      class="fixed top-4 right-4 z-50 px-4 py-3 rounded-lg shadow-lg flex items-center animate-fade-in"
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
      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">Data Preview</h3>
          <button @click="editData"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
            Edit
          </button>
        </div>
        <div
          v-if="filteredTasks.length === 0"
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
                  v-for="header in Object.keys(filteredTasks[0] || {})"
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
                  v-for="header in Object.keys(filteredTasks[0] || {})"
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
              />
              <p class="text-xs text-gray-500 mt-1">
                Showing {{ Math.min(dataLimit, props.tasks.length) }} of {{ props.tasks.length }} rows
              </p>
            </div>
            
            <div>
              <label class="flex items-center cursor-pointer">
                <input
                  v-model="showAllData"
                  type="checkbox"
                  class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                />
                <span class="ml-2 text-sm text-gray-700">Show all data</span>
              </label>
            </div>

            <div class="text-sm text-gray-600">
              <p>Preview: {{ filteredTasks.length }} rows</p>
              <p class="text-xs">This affects simulation input only</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Algorithm Selection -->
      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
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
      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">
          Common Parameters
        </h2>

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
              <span
                class="relative group cursor-pointer text-gray-400 text-xs font-bold"
              >
                ?
                <div
                  class="absolute hidden group-hover:block bg-gray-800 text-white text-xs rounded-md shadow-lg p-2 left-4 top-0 w-64 z-10"
                >
                  Column name for task IDs in your dataset.
                  Default: 'id'
                </div>
              </span>
            </div>
            <select
              v-model="parameters.task_id_col"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option v-for="header in datasetHeaders" :key="header" :value="header">
                {{ header }}
              </option>
            </select>
          </div>

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
          </div>

          <!-- ACO Specific Parameters -->
          <template v-if="selectedAlgorithms.includes('ACO')">
            <div class="col-span-1">
              <h3 class="text-md font-semibold text-gray-900 mb-3">
                ACO Parameters
              </h3>
              <div class="space-y-4">
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
            <div class="col-span-1">
              <h3 class="text-md font-semibold text-gray-900 mb-3">
                PSO Parameters
              </h3>
              <div class="space-y-4">
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

        <div class="mt-6">
          <button
          @click="runSimulation"
          :disabled="
            isRunning ||
            selectedAlgorithms.length === 0 ||
            !dataValidation.isValid ||
            filteredTasks.length === 0
          "
          class="w-full md:w-auto px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          <span v-if="isRunning">Running...</span>
          <span v-else-if="filteredTasks.length === 0">No Data Available</span>
          <span v-else-if="!dataValidation.isValid">Invalid Data</span>
          <span v-else>{{
            `Run ${selectedAlgorithms.join(" & ")} Simulation`
          }}</span>
        </button>
        </div>
      </div>

      <!-- Algorithm Results -->
      <div v-if="selectedAlgorithms.length > 0" class="space-y-6">
        <!-- ACO Results -->
        <div
          v-if="selectedAlgorithms.includes('ACO')"
          class="bg-white rounded-xl shadow-lg p-6"
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
          class="bg-white rounded-xl shadow-lg p-6"
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
        class="bg-white rounded-xl shadow-lg p-6 mb-6"
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
        v-if="bestMakespan.ACO && bestMakespan.PSO"
        class="bg-white rounded-xl shadow-sm p-6 mt-6"
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
                  Total Execution Time (s)
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
                  bestMakespan.ACO <= bestMakespan.PSO
                    ? 'bg-blue-50 text-blue-700 font-bold'
                    : 'text-gray-900',
                ]"
              >
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm"
                  :class="{
                    'font-bold':
                      bestMakespan.ACO &&
                      bestMakespan.PSO &&
                      bestMakespan.ACO <= bestMakespan.PSO,
                  }"
                >
                  ACO
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{
                    'font-bold':
                      bestMakespan.ACO &&
                      bestMakespan.PSO &&
                      bestMakespan.ACO <= bestMakespan.PSO,
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
                    'font-bold':
                      bestMakespan.ACO &&
                      bestMakespan.PSO &&
                      bestMakespan.ACO <= bestMakespan.PSO,
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
                    'font-bold':
                      bestMakespan.ACO &&
                      bestMakespan.PSO &&
                      bestMakespan.ACO <= bestMakespan.PSO,
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
                    'font-bold':
                      bestMakespan.ACO &&
                      bestMakespan.PSO &&
                      bestMakespan.ACO <= bestMakespan.PSO,
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
                  bestMakespan.ACO &&
                  bestMakespan.PSO &&
                  bestMakespan.PSO < bestMakespan.ACO
                    ? 'bg-blue-50 text-blue-700 font-bold'
                    : 'text-gray-900',
                ]"
              >
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm"
                  :class="{
                    'font-bold':
                      bestMakespan.ACO &&
                      bestMakespan.PSO &&
                      bestMakespan.PSO < bestMakespan.ACO,
                  }"
                >
                  PSO
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{
                    'font-bold':
                      bestMakespan.ACO &&
                      bestMakespan.PSO &&
                      bestMakespan.PSO < bestMakespan.ACO,
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
                    'font-bold':
                      bestMakespan.ACO &&
                      bestMakespan.PSO &&
                      bestMakespan.PSO < bestMakespan.ACO,
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
                    'font-bold':
                      bestMakespan.ACO &&
                      bestMakespan.PSO &&
                      bestMakespan.PSO < bestMakespan.ACO,
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
                    'font-bold':
                      bestMakespan.ACO &&
                      bestMakespan.PSO &&
                      bestMakespan.PSO < bestMakespan.ACO,
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
            Winner:
            {{
              bestMakespan.ACO && bestMakespan.PSO
                ? bestMakespan.ACO <= bestMakespan.PSO
                  ? "ACO"
                  : "PSO"
                : "Pending"
            }}
          </span>
        </div>
      </div>

      <!-- AI Chat Assistant - Floating Design -->
      <div>
        <!-- Floating Chat Bubble -->
        <div
          v-if="!isChatOpen"
          @click="openChat"
          class="fixed bottom-6 right-6 w-14 h-14 bg-blue-500 text-white rounded-full shadow-lg hover:bg-blue-600 cursor-pointer flex items-center justify-center z-50 transition-all duration-200 hover:scale-110"
          title="Ask Swarm Lab AI"
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
          class="fixed bottom-6 right-6 bg-white rounded-xl shadow-2xl z-50 flex flex-col transition-all duration-300 ease-in-out"
          :class="{
            'translate-y-0 opacity-100': isChatOpen,
            'translate-y-full opacity-0': !isChatOpen,
            'cursor-move': isDragging,
            'cursor-se-resize': isResizing,
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
            <h3 class="text-lg font-semibold text-gray-900">Swarm Lab AI</h3>
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

            <div v-else class="space-y-3">
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
                      'max-w-[90%] px-3 py-2 rounded-lg text-sm whitespace-normal',
                      message.role === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-white border border-gray-200 text-gray-900',
                    ]"
                  >
                    <div
                      class="prose prose-sm max-w-none break-words overflow-wrap-break-word overflow-x-auto"
                      v-html="renderMarkdown(message.content)"
                    ></div>

                    <!-- Copy Button for AI responses -->
                    <div
                      v-if="message.role === 'assistant'"
                      class="mt-2 flex justify-end"
                    >
                      <button
                        @click="copyToClipboard(message.content)"
                        class="text-xs text-gray-500 hover:text-gray-700 flex items-center gap-1 px-2 py-1 rounded hover:bg-gray-100 transition-colors"
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

          <!-- Resize Handle -->
          <div 
            class="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize"
            @mousedown="startResize"
            @touchstart="startResize"
          >
            <svg class="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd" />
            </svg>
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
          Run Again
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
const chartCanvasACO = ref(null);
const chartCanvasPSO = ref(null);
const acoLogsContainer = ref(null);
const psoLogsContainer = ref(null);
let chartACO = null;
let chartPSO = null;
const toast = ref({ show: false, message: "", type: "error" });
const dataValidation = ref({ isValid: true, errors: [], warnings: [], summary: {} });
const dataLimit = ref(Math.max(1, props.tasks.length));
const showAllData = ref(false);
const parameters = reactive({
  num_default_agents: 3, n_iterations: 100, task_id_col: 'id', agent_id_col: '',
  n_ants: 10, alpha: 1.0, beta: 2.0, evaporation_rate: 0.5, pheromone_deposit: 100.0,
  n_particles: 30, w: 0.5, c1: 1.5, c2: 1.5,
});
const expandedTasks = ref({ ACO: {}, PSO: {} });

// --- COMPUTED PROPERTIES ---
const filteredTasks = computed(() => {
  if (!props.tasks || props.tasks.length === 0) return [];
  if (showAllData.value) return props.tasks;
  const actualLimit = Math.max(1, Math.min(dataLimit.value, props.tasks.length));
  return props.tasks.slice(0, actualLimit);
});

const datasetHeaders = computed(() => {
  if (props.tasks.length === 0) return [];
  return Object.keys(props.tasks[0]);
});

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
  }
};

const runSimulation = async () => {
  validateData();
  if (filteredTasks.value.length === 0) {
    showToast("Please add at least one task to the data.", 'error');
    return;
  }
  if (!dataValidation.value.isValid || selectedAlgorithms.value.length === 0) {
    showToast("Please select an algorithm and ensure data is valid.", 'error');
    return;
  }

  isRunning.value = true;
  selectedAlgorithms.value.forEach(resetSimulationStateForAlgo);

  const runningSims = selectedAlgorithms.value.map(async (algorithm) => {
    const requestBody = {
      algorithm: algorithm,
      tasks: filteredTasks.value,
      parameters: { ...parameters }
    };

    try {
      const response = await fetch('http://127.0.0.1:5001/stream_scheduling', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok || !response.body) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      status.value[algorithm] = "Running...";
      const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const lines = value.split('\n\n').filter(line => line.startsWith('data:'));
        for (const line of lines) {
          const jsonData = line.substring(5);
          if (jsonData) {
            handleStreamEvent(algorithm, JSON.parse(jsonData));
          }
        }
      }
    } catch (error) {
      console.error(`Error with ${algorithm} simulation:`, error);
      logs.value[algorithm].push(`❌ Simulation failed: ${error.message}`);
      status.value[algorithm] = "Failed";
    }
  });

  await Promise.all(runningSims);
  isRunning.value = false;
};

const handleStreamEvent = (algorithm, data) => {
  const chart = algorithm === 'ACO' ? chartACO : chartPSO;
  const logsContainer = algorithm === 'ACO' ? acoLogsContainer.value : psoLogsContainer.value;

  const processLog = (message) => {
      logs.value[algorithm].push(message);
      nextTick(() => {
          if (logsContainer) {
              logsContainer.scrollTop = logsContainer.scrollHeight;
          }
      });
  };

  switch (data.type) {
    case 'log':
    case 'start':
      processLog(data.message);
      break;
    
    case 'iteration':
      processLog(data.log_message);
      bestMakespan.value[algorithm] = data.makespan;
      if (chart) {
        chart.data.labels.push(data.iteration);
        chart.data.datasets[0].data.push(data.makespan);
        // Only show the best point marker
        const bestVal = Math.min(...chart.data.datasets[0].data);
        const bestIndex = chart.data.datasets[0].data.indexOf(bestVal);
        chart.data.datasets[1].data = chart.data.datasets[0].data.map((val, idx) => idx === bestIndex ? val : null);

        chart.update('none'); // Use 'none' for smoother updates
      }
      break;

    case 'done':
      processLog(data.log_message);
      bestMakespan.value[algorithm] = data.makespan;
      const finalAssignments = transformAssignmentData(data.schedule);
      if (algorithm === 'ACO') acoFinalAssignment.value = finalAssignments;
      if (algorithm === 'PSO') psoFinalAssignment.value = finalAssignments;
      break;

    case 'final_metrics':
      executionTime.value[algorithm] = data.execution_time;
      computationTime.value[algorithm] = data.execution_time;
      loadBalanceIndex.value[algorithm] = data.load_balance_index;
      status.value[algorithm] = "Completed";
      break;

    case 'error':
      processLog(`❌ ERROR: ${data.message}`);
      status.value[algorithm] = "Failed";
      break;
  }
};

const transformAssignmentData = (schedule) => {
  if (!schedule || schedule.length === 0) return [];
  const agentMap = new Map();

  schedule.forEach(task => {
    const agentId = task.agent_id;
    if (!agentMap.has(agentId)) {
      agentMap.set(agentId, { tasks: [], finish_time: 0 });
    }
    const agentData = agentMap.get(agentId);
    agentData.tasks.push(task.task_id);
    agentData.finish_time = Math.max(agentData.finish_time, task.finish_time);
  });

  return Array.from(agentMap.entries()).map(([agent, data]) => ({
    agent: agent,
    tasks: data.tasks,
    total_time: data.finish_time
  }));
};

// --- UI & HELPER FUNCTIONS ---

const initCharts = () => {
    const createChart = (canvasRef, label, color) => {
        if (!canvasRef.value) return null;
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
    if (chartACO) chartACO.destroy();
    if (chartPSO) chartPSO.destroy();
    nextTick(() => {
        chartACO = createChart(chartCanvasACO, 'ACO', 'rgb(59, 130, 246)');
        chartPSO = createChart(chartCanvasPSO, 'PSO', 'rgb(239, 68, 68)');
    });
};

const validateData = () => {
  const errors = [];
  if (props.tasks.length === 0) {
    errors.push("No tasks available.");
  }
  // Add more comprehensive validation if needed
  dataValidation.value = {
    isValid: errors.length === 0,
    errors,
    warnings: [],
  };
};

const resetSimulation = () => {
  selectedAlgorithms.value.forEach(resetSimulationStateForAlgo);
  isRunning.value = false;
};

const editData = () => emit("edit-data");

const exportData = (algorithm, format) => {
    const assignment = algorithm === 'ACO' ? acoFinalAssignment.value : psoFinalAssignment.value;
    if (!assignment || assignment.length === 0) {
        showToast(`No data to export for ${algorithm}`, 'info');
        return;
    }

    let content = '';
    let mimeType = '';
    let fileExtension = '';

    if (format === 'json') {
        content = JSON.stringify(assignment, null, 2);
        mimeType = 'application/json';
        fileExtension = 'json';
    } else { // csv
        const headers = ["Agent", "Tasks", "Total Time"];
        const rows = assignment.map(row => [
            `"${row.agent}"`,
            `"${Array.isArray(row.tasks) ? row.tasks.join(";") : row.tasks}"`,
            `"${row.total_time}"`
        ]);
        content = [headers.join(","), ...rows.map(row => row.join(","))].join("\n");
        mimeType = 'text/csv;charset=utf-8;';
        fileExtension = 'csv';
    }

    const blob = new Blob([content], { type: mimeType });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${algorithm}_final_assignment.${fileExtension}`;
    link.click();
    URL.revokeObjectURL(link.href);
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

watch(props.tasks, () => {
    validateData();
    dataLimit.value = props.tasks.length;
}, { deep: true, immediate: true });

// --- AI & CHAT WINDOW (UNCHANGED) ---
const userMessage = ref("");
const isChatOpen = ref(false);
const draggablePosition = ref({ x: 0, y: 0 });
const isDragging = ref(false);
const dragStart = ref({ x: 0, y: 0 });
const chatWindow = ref(null);
const chatWindowSize = ref({ width: 384, height: 500 });
const isResizing = ref(false);
const resizeStart = ref({ x: 0, y: 0, width: 0, height: 0 });
const messagesContainer = ref(null);

const openChat = () => isChatOpen.value = true;
const closeChat = () => isChatOpen.value = false;
const renderMarkdown = (text) => marked(text || '');
const copyToClipboard = (text) => navigator.clipboard.writeText(text).then(() => showToast('Copied to clipboard', 'success'));

const sendUserMessage = async () => {
    if (!userMessage.value.trim() && chatHistory.value.length === 0) {
        userMessage.value = "Explain these simulation results.";
    }
    if (!userMessage.value.trim()) return;

    const simulationData = {
        aco: selectedAlgorithms.value.includes('ACO') ? {
            bestMakespan: bestMakespan.value.ACO,
            executionTime: executionTime.value.ACO,
            loadBalanceIndex: loadBalanceIndex.value.ACO,
            finalAssignment: acoFinalAssignment.value,
        } : null,
        pso: selectedAlgorithms.value.includes('PSO') ? {
            bestMakespan: bestMakespan.value.PSO,
            executionTime: executionTime.value.PSO,
            loadBalanceIndex: loadBalanceIndex.value.PSO,
            finalAssignment: psoFinalAssignment.value,
        } : null,
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

const startResize = (event) => {
  isResizing.value = true;
  const clientX = event.clientX || event.touches[0].clientX;
  const clientY = event.clientY || event.touches[0].clientY;
  resizeStart.value = { x: clientX, y: clientY, width: chatWindowSize.value.width, height: chatWindowSize.value.height };
  
  const handleMove = (e) => {
    if (!isResizing.value) return;
    const moveX = e.clientX || e.touches[0].clientX;
    const moveY = e.clientY || e.touches[0].clientY;
    const deltaX = moveX - resizeStart.value.x;
    const deltaY = moveY - resizeStart.value.y;
    chatWindowSize.value = {
      width: Math.max(320, resizeStart.value.width + deltaX),
      height: Math.max(400, resizeStart.value.height + deltaY),
    };
  };
  const handleUp = () => {
    isResizing.value = false;
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
</style>
