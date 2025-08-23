<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
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
        <h3 class="text-lg font-medium text-gray-900 mb-4">Data Preview</h3>
        <div
          v-if="props.tasks.length === 0"
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
                  v-for="header in Object.keys(props.tasks[0] || {})"
                  :key="header"
                  class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="(task, index) in props.tasks.slice(0, 5)"
                :key="index"
                class="hover:bg-gray-50"
              >
                <td
                  v-for="header in Object.keys(props.tasks[0] || {})"
                  :key="header"
                  class="px-4 py-2 whitespace-nowrap text-sm text-gray-900"
                >
                  {{ task[header] }}
                </td>
              </tr>
            </tbody>
          </table>
          <div
            v-if="props.tasks.length > 5"
            class="text-center py-2 text-sm text-gray-500"
          >
            Showing first 5 of {{ props.tasks.length }} rows
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
              v-model.number="parameters.num_agents"
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
              v-model.number="parameters.num_iterations"
              type="number"
              min="1"
              max="100"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
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
                    v-model.number="parameters.num_particles"
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
                    v-model.number="parameters.inertia"
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
              !dataValidation.isValid
            "
            class="w-full md:w-auto px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <span v-if="isRunning">Running...</span>
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
                  status.ACO === 'Idle' ? 'bg-gray-100 text-gray-800' :
                  status.ACO === 'Running...' ? 'bg-blue-100 text-blue-800' :
                  'bg-green-100 text-green-800'
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
              <div class="bg-gray-50 rounded-lg p-4 h-64 overflow-y-auto">
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
          <div
            v-if="selectedAlgorithms.includes('ACO')"
            class="mt-6"
          >
            <div class="flex justify-between items-center mb-2">
              <h3 class="text-lg font-medium text-gray-900">
                ACO Final Assignment 
                <span v-if="bestMakespan.ACO">(Best Makespan: {{ bestMakespan.ACO }}s)</span>
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
                  <!-- Preview Mode -->
                  <tr v-if="simulationStatus !== 'completed' && (!finalAssignment.ACO || finalAssignment.ACO.length === 0)">
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                    >
                      Agent 1
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500">
                      Preview...
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500 text-right font-mono">
                      Preview...
                    </td>
                  </tr>
                  <!-- Actual Data -->
                  <tr
                    v-for="assignment in (simulationStatus === 'completed' ? acoFinalAssignment : finalAssignment.ACO)"
                    :key="assignment.agent"
                  >
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                    >
                      {{ assignment.agent }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500">
                      <div class="max-w-xs">
                        <div v-if="!expandedTasks.ACO[assignment.agent] && assignment.tasks.length > 10">
                          {{ assignment.tasks.slice(0, 10).join(', ') }}
                          <button
                            @click="toggleTaskExpansion('ACO', assignment.agent)"
                            class="text-blue-600 hover:text-blue-800 ml-1"
                          >
                            ... (+{{ assignment.tasks.length - 10 }} more)
                          </button>
                        </div>
                        <div v-else-if="expandedTasks.ACO[assignment.agent] || assignment.tasks.length <= 10">
                          <div class="max-h-32 overflow-y-auto">
                            {{ Array.isArray(assignment.tasks) ? assignment.tasks.join(', ') : assignment.tasks }}
                          </div>
                          <button
                            v-if="assignment.tasks.length > 10 && expandedTasks.ACO[assignment.agent]"
                            @click="toggleTaskExpansion('ACO', assignment.agent)"
                            class="text-blue-600 hover:text-blue-800 text-xs mt-1"
                          >
                            Show less
                          </button>
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500 text-right font-mono">
                      <span v-if="assignment.total_time === 'Preview...'" class="text-gray-500">
                        {{ assignment.total_time }}
                      </span>
                      <span v-else>
                        {{ typeof assignment.total_time === 'number' ? assignment.total_time.toFixed(2) : assignment.total_time }}s
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
                  status.PSO === 'Idle' ? 'bg-gray-100 text-gray-800' :
                  status.PSO === 'Running...' ? 'bg-blue-100 text-blue-800' :
                  'bg-green-100 text-green-800'
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
              <div class="bg-gray-50 rounded-lg p-4 h-64 overflow-y-auto">
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
          <div
            v-if="selectedAlgorithms.includes('PSO')"
            class="mt-6"
          >
            <div class="flex justify-between items-center mb-2">
              <h3 class="text-lg font-medium text-gray-900">
                PSO Final Assignment 
                <span v-if="bestMakespan.PSO">(Best Makespan: {{ bestMakespan.PSO }}s)</span>
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
                  <!-- Preview Mode -->
                  <tr v-if="simulationStatus !== 'completed' && (!finalAssignment.PSO || finalAssignment.PSO.length === 0)">
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                    >
                      Agent 1
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500">
                      Preview...
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500 text-right font-mono">
                      Preview...
                    </td>
                  </tr>
                  <!-- Actual Data -->
                  <tr
                    v-for="assignment in (simulationStatus === 'completed' ? psoFinalAssignment : finalAssignment.PSO)"
                    :key="assignment.agent"
                  >
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                    >
                      {{ assignment.agent }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500">
                      <div class="max-w-xs">
                        <div v-if="!expandedTasks.PSO[assignment.agent] && assignment.tasks.length > 10">
                          {{ assignment.tasks.slice(0, 10).join(', ') }}
                          <button
                            @click="toggleTaskExpansion('PSO', assignment.agent)"
                            class="text-blue-600 hover:text-blue-800 ml-1"
                          >
                            ... (+{{ assignment.tasks.length - 10 }} more)
                          </button>
                        </div>
                        <div v-else-if="expandedTasks.PSO[assignment.agent] || assignment.tasks.length <= 10">
                          <div class="max-h-32 overflow-y-auto">
                            {{ Array.isArray(assignment.tasks) ? assignment.tasks.join(', ') : assignment.tasks }}
                          </div>
                          <button
                            v-if="assignment.tasks.length > 10 && expandedTasks.PSO[assignment.agent]"
                            @click="toggleTaskExpansion('PSO', assignment.agent)"
                            class="text-blue-600 hover:text-blue-800 text-xs mt-1"
                          >
                            Show less
                          </button>
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500 text-right font-mono">
                      <span v-if="assignment.total_time === 'Preview...'" class="text-gray-500">
                        {{ assignment.total_time }}
                      </span>
                      <span v-else>
                        {{ typeof assignment.total_time === 'number' ? assignment.total_time.toFixed(2) : assignment.total_time }}s
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
      <div v-if="bestMakespan.ACO && bestMakespan.PSO" class="bg-white rounded-xl shadow-sm p-6 mt-6">
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
                    : 'text-gray-900'
                ]"
              >
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm"
                  :class="{ 'font-bold': bestMakespan.ACO && bestMakespan.PSO && bestMakespan.ACO <= bestMakespan.PSO }"
                >
                  ACO
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{ 'font-bold': bestMakespan.ACO && bestMakespan.PSO && bestMakespan.ACO <= bestMakespan.PSO }"
                >
                  {{ bestMakespan.ACO ? parseFloat(bestMakespan.ACO).toFixed(2) : 'N/A' }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{ 'font-bold': bestMakespan.ACO && bestMakespan.PSO && bestMakespan.ACO <= bestMakespan.PSO }"
                >
                  {{ executionTime.ACO ? parseFloat(executionTime.ACO).toFixed(2) : 'N/A' }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{ 'font-bold': bestMakespan.ACO && bestMakespan.PSO && bestMakespan.ACO <= bestMakespan.PSO }"
                >
                  {{ loadBalanceIndex.ACO ? parseFloat(loadBalanceIndex.ACO).toFixed(4) : 'N/A' }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{ 'font-bold': bestMakespan.ACO && bestMakespan.PSO && bestMakespan.ACO <= bestMakespan.PSO }"
                >
                  {{ computationTime.ACO ? parseFloat(computationTime.ACO).toFixed(2) : 'N/A' }}
                </td>
              </tr>
              <tr
                :class="[
                  bestMakespan.ACO && bestMakespan.PSO && bestMakespan.PSO < bestMakespan.ACO 
                    ? 'bg-blue-50 text-blue-700 font-bold' 
                    : 'text-gray-900'
                ]"
              >
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm"
                  :class="{ 'font-bold': bestMakespan.ACO && bestMakespan.PSO && bestMakespan.PSO < bestMakespan.ACO }"
                >
                  PSO
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{ 'font-bold': bestMakespan.ACO && bestMakespan.PSO && bestMakespan.PSO < bestMakespan.ACO }"
                >
                  {{ bestMakespan.PSO ? parseFloat(bestMakespan.PSO).toFixed(2) : 'N/A' }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{ 'font-bold': bestMakespan.ACO && bestMakespan.PSO && bestMakespan.PSO < bestMakespan.ACO }"
                >
                  {{ executionTime.PSO ? parseFloat(executionTime.PSO).toFixed(2) : 'N/A' }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{ 'font-bold': bestMakespan.ACO && bestMakespan.PSO && bestMakespan.PSO < bestMakespan.ACO }"
                >
                  {{ loadBalanceIndex.PSO ? parseFloat(loadBalanceIndex.PSO).toFixed(4) : 'N/A' }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono"
                  :class="{ 'font-bold': bestMakespan.ACO && bestMakespan.PSO && bestMakespan.PSO < bestMakespan.ACO }"
                >
                  {{ computationTime.PSO ? parseFloat(computationTime.PSO).toFixed(2) : 'N/A' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="mt-6 pt-4 border-t border-gray-200 text-center">
          <span class="text-lg font-bold text-blue-600">
            Winner: {{ bestMakespan.ACO && bestMakespan.PSO ? (bestMakespan.ACO <= bestMakespan.PSO ? 'ACO' : 'PSO') : 'Pending' }}
          </span>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="selectedAlgorithms.length === 0"
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
import { ref, reactive, watch, nextTick, onMounted, computed } from "vue";
import Chart from "chart.js/auto";

// Props
const props = defineProps({
  tasks: {
    type: Array,
    required: true,
  },
  algorithms: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["back-to-table"]);

// State
const selectedAlgorithms = ref([]);
const isRunning = ref(false);
const logs = ref({});
const finalAssignment = ref({});
const bestMakespan = ref({});
const executionTime = ref({});
const loadBalanceIndex = ref({});
const computationTime = ref({});
const chartData = ref({});
const dataValidation = ref({
  isValid: true,
  errors: [],
  warnings: [],
  summary: {},
});
const chartCanvasACO = ref(null);
const chartCanvasPSO = ref(null);
let chartACO = null;
let chartPSO = null;
const dummyFinalAssignment = ref(null);
const showTaskModal = ref(false);
const modalData = ref({ agent: '', tasks: [] });
const status = ref({ ACO: 'Idle', PSO: 'Idle' });
const expandedTasks = ref({ ACO: {}, PSO: {} });

// Reactive state for backend results
const acoFinalAssignment = ref([]);
const psoFinalAssignment = ref([]);
const simulationStatus = ref('idle'); // idle, running, completed

// Dummy data generators
const generateDummyACOAssignments = () => {
  const dummy = [];
  for (let i = 1; i <= parameters.num_agents; i++) {
    dummy.push({
      agent: `ACO Agent ${i}`,
      tasks: ["Preview..."],
      total_time: "Preview..."
    });
  }
  acoFinalAssignment.value = dummy;
};

const generateDummyPSOAssignments = () => {
  const dummy = [];
  for (let i = 1; i <= parameters.num_agents; i++) {
    dummy.push({
      agent: `PSO Agent ${i}`,
      tasks: ["Preview..."],
      total_time: "Preview..."
    });
  }
  psoFinalAssignment.value = dummy;
};



// Parameters
const parameters = reactive({
  // Common
  num_agents: 3,
  num_iterations: 50,

  // ACO specific
  alpha: 0.7,
  beta: 3.0,
  evaporation_rate: 0.5,

  // PSO specific
  num_particles: 30,
  inertia: 0.7,
  c1: 1.5,
  c2: 1.5,
});

// Chart data already declared above

// Initialize charts
  const initCharts = () => {
    // ACO Chart
    if (chartCanvasACO.value) {
      const ctx = chartCanvasACO.value.getContext("2d");
      chartACO = new Chart(ctx, {
        type: "line",
        data: {
          labels: [],
          datasets: [
            {
              label: "ACO Best Makespan",
              data: [],
              borderColor: "rgb(59, 130, 246)",
              backgroundColor: "rgba(59, 130, 246, 0.1)",
              tension: 0.4,
              fill: true,
            },
            {
              label: "Best Makespan",
              data: [],
              backgroundColor: "rgb(59, 130, 246)",
              borderColor: "rgb(59, 130, 246)",
              pointRadius: 6,
              pointHoverRadius: 8,
              showLine: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
            },
          },
          scales: {
            y: {
              beginAtZero: false,
              title: {
                display: true,
                text: "Makespan",
              },
            },
            x: {
              title: {
                display: true,
                text: "Iteration",
              },
            },
          },
        },
      });
    }

    // PSO Chart
    if (chartCanvasPSO.value) {
      const ctx = chartCanvasPSO.value.getContext("2d");
      chartPSO = new Chart(ctx, {
        type: "line",
        data: {
          labels: [],
          datasets: [
            {
              label: "PSO Best Makespan",
              data: [],
              borderColor: "rgb(239, 68, 68)",
              backgroundColor: "rgba(239, 68, 68, 0.1)",
              tension: 0.4,
              fill: true,
            },
            {
              label: "Best Makespan",
              data: [],
              backgroundColor: "rgb(239, 68, 68)",
              borderColor: "rgb(239, 68, 68)",
              pointRadius: 6,
              pointHoverRadius: 8,
              showLine: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
            },
          },
          scales: {
            y: {
              beginAtZero: false,
              title: {
                display: true,
                text: "Makespan",
              },
            },
            x: {
              title: {
                display: true,
                text: "Iteration",
              },
            },
          },
        },
      });
    }
  };

// Data validation and preview
const validateData = () => {
  const errors = [];
  const warnings = [];
  const summary = {
    totalRows: props.tasks.length,
    emptyCells: 0,
    validRows: 0,
    numericColumns: [],
    textColumns: [],
  };

  if (props.tasks.length === 0) {
    errors.push("No tasks available. Please add tasks to the data table.");
    dataValidation.value = { isValid: false, errors, warnings, summary };
    return;
  }

  // Analyze each task for valid data
  props.tasks.forEach((task, index) => {
    const taskKeys = Object.keys(task);
    let hasValidData = false;
    let rowHasValidNumeric = false;

    taskKeys.forEach((key) => {
      const value = task[key];
      const strValue = String(value).trim();

      if (
        value === null ||
        value === undefined ||
        value === "" ||
        strValue === ""
      ) {
        summary.emptyCells++;
        // Treat empty as 0 for validation purposes
        if (!summary.numericColumns.includes(key))
          summary.numericColumns.push(key);
        rowHasValidNumeric = true;
      } else {
        hasValidData = true;

        // Validate all non-empty values must be numeric
        const numValue = Number(strValue);

        if (!isNaN(numValue) && isFinite(numValue)) {
          if (!summary.numericColumns.includes(key))
            summary.numericColumns.push(key);
          rowHasValidNumeric = true;
        } else {
          errors.push(
            `Row ${index + 1}: ${key} must be numeric (found: "${strValue}")`
          );
          return;
        }
      }
    });

    if (rowHasValidNumeric) summary.validRows++;
  });

  // Validation rules - allow empty values as 0
  if (summary.validRows === 0 && props.tasks.length === 0) {
    errors.push("No tasks available. Please add tasks to the data table.");
  }

  if (summary.emptyCells > 0) {
    warnings.push(
      `${summary.emptyCells} empty cells detected. These will be treated as 0 during simulation.`
    );
  }

  dataValidation.value = {
    isValid: errors.length === 0,
    errors,
    warnings,
    summary,
  };
};

// Update charts
  const updateCharts = () => {
    if (chartACO && chartData.value.ACO.labels.length > 0) {
      chartACO.data.labels = chartData.value.ACO.labels;
      chartACO.data.datasets[0].data = chartData.value.ACO.values;
      
      // Add best makespan marker
      const minValue = Math.min(...chartData.value.ACO.values);
      const minIndex = chartData.value.ACO.values.indexOf(minValue);
      
      chartACO.data.datasets[1] = {
        label: 'Best Makespan',
        data: chartData.value.ACO.values.map((value, index) => 
          index === minIndex ? value : null
        ),
        backgroundColor: 'rgb(59, 130, 246)',
        borderColor: 'rgb(59, 130, 246)',
        pointRadius: 6,
        pointHoverRadius: 8,
        showLine: false,
      };
      
      chartACO.update();
    }

    if (chartPSO && chartData.value.PSO.labels.length > 0) {
      chartPSO.data.labels = chartData.value.PSO.labels;
      chartPSO.data.datasets[0].data = chartData.value.PSO.values;
      
      // Add best makespan marker
      const minValue = Math.min(...chartData.value.PSO.values);
      const minIndex = chartData.value.PSO.values.indexOf(minValue);
      
      chartPSO.data.datasets[1] = {
        label: 'Best Makespan',
        data: chartData.value.PSO.values.map((value, index) => 
          index === minIndex ? value : null
        ),
        backgroundColor: 'rgb(239, 68, 68)',
        borderColor: 'rgb(239, 68, 68)',
        pointRadius: 6,
        pointHoverRadius: 8,
        showLine: false,
      };
      
      chartPSO.update();
    }
  };

// Mock simulation function for multiple algorithms
const runSimulation = async () => {
  validateData();

  if (!dataValidation.value.isValid) {
    console.error(
      "SimulationPage - Data validation failed:",
      dataValidation.value.errors
    );
    return;
  }

  if (selectedAlgorithms.value.length === 0) {
    console.error(
      "SimulationPage - Cannot run simulation: No algorithms selected"
    );
    return;
  }

  isRunning.value = true;
  dummyFinalAssignment.value = null; // Reset dummy data

  // Reset data for selected algorithms and set status to Running
  simulationStatus.value = 'running';
  selectedAlgorithms.value.forEach((algo) => {
    status.value[algo] = 'Running...';
    logs.value[algo] = [];
    finalAssignment.value[algo] = [];
    bestMakespan.value[algo] = null;
    executionTime.value[algo] = null;
    loadBalanceIndex.value[algo] = null;
    computationTime.value[algo] = null;
    chartData.value[algo] = { labels: [], values: [] };
  });
  
  // Reset backend result arrays and generate dummy assignments
  generateDummyACOAssignments();
  generateDummyPSOAssignments();
  
  // Reset and clear charts - destroy and recreate to ensure proper re-rendering
  if (chartACO) {
    chartACO.destroy();
    chartACO = null;
  }
  if (chartPSO) {
    chartPSO.destroy();
    chartPSO = null;
  }
  
  // Re-initialize charts after data reset
  await nextTick();
  initCharts();

  // Simple simulation with dummy data - prevent stack overflow
  const numTasks = props.tasks.length;
  const numAgents = parameters.num_agents;

  // Add minimal logs for each algorithm
  selectedAlgorithms.value.forEach((algorithm) => {
    logs.value[algorithm].push(`${algorithm} - Starting simulation...`);
    
    // Add a few dummy iterations
    for (let i = 1; i <= Math.min(5, parameters.num_iterations); i++) {
      const currentBest = 1800 + Math.random() * 200 - (i * 10);
      logs.value[algorithm].push(`${algorithm} - Iteration ${i}: Best Makespan so far = ${currentBest.toFixed(2)}`);
      
      chartData.value[algorithm].labels.push(i);
      chartData.value[algorithm].values.push(currentBest);
    }
    
    logs.value[algorithm].push(`${algorithm} - Simulation completed!`);
  });

  // After 2 seconds, complete the simulation and show dummy final assignment
    setTimeout(() => {
      isRunning.value = false;
      
      // Set status to Completed for all algorithms
      selectedAlgorithms.value.forEach((algo) => {
        status.value[algo] = 'Completed';
      });
      
      dummyFinalAssignment.value = {
      agents: [
        { id: 1, tasks: [1, 3, 5, 7, 9, 11], time: 1826.21 },
        { id: 2, tasks: [2, 4, 6, 8, 10, 12], time: 1825.90 },
        { id: 3, tasks: [13, 14, 15, 16], time: 1824.89 }
      ],
      bestMakespan: 1826.21
    };
    
    // Add final assignment data for each algorithm
    selectedAlgorithms.value.forEach((algorithm) => {
      const tasksPerAgent = Math.floor(numTasks / numAgents);
      const remainingTasks = numTasks % numAgents;
      
      let taskIndex = 0;
      const assignmentData = [];
      
      for (let agent = 1; agent <= numAgents; agent++) {
        const agentTasks = [];
        const tasksForThisAgent = tasksPerAgent + (agent <= remainingTasks ? 1 : 0);
        
        for (let j = 0; j < tasksForThisAgent; j++) {
          if (taskIndex < numTasks) {
            agentTasks.push(taskIndex + 1);
            taskIndex++;
          }
        }
        
        const totalTime = (algorithm === "ACO" ? 1825 : 1826) + Math.random() * 10;
        
        const assignment = {
          agent: `${algorithm} Agent ${agent}`,
          tasks: agentTasks,
          total_time: Array.isArray(totalTime) ? totalTime[0] : totalTime,
        };
        
        finalAssignment.value[algorithm].push(assignment);
        assignmentData.push(assignment);
      }
      
      // Replace dummy data with actual backend results
      if (algorithm === 'ACO') {
        acoFinalAssignment.value = assignmentData.map(item => ({
          agent: item.agent,
          tasks: item.tasks,
          total_time: parseFloat(item.total_time.toFixed(2))
        }));
      } else if (algorithm === 'PSO') {
        psoFinalAssignment.value = assignmentData.map(item => ({
          agent: item.agent,
          tasks: item.tasks,
          total_time: parseFloat(item.total_time.toFixed(2))
        }));
      }
      
      bestMakespan.value[algorithm] = (algorithm === "ACO" ? 1825.50 : 1826.21).toFixed(2);
      executionTime.value[algorithm] = (algorithm === "ACO" ? 45.2 : 38.7).toFixed(1);
      loadBalanceIndex.value[algorithm] = (algorithm === "ACO" ? 0.15 : 0.18).toFixed(3);
      computationTime.value[algorithm] = (algorithm === "ACO" ? 245 : 189).toFixed(0);
    });
    
    simulationStatus.value = 'completed';
    
    updateCharts();
  }, 2000);
};

// Watch for algorithms prop changes
watch(
  () => props.algorithms,
  (newAlgorithms) => {
    console.log("SimulationPage - Algorithms prop changed:", newAlgorithms);
    if (newAlgorithms && newAlgorithms.length > 0) {
      selectedAlgorithms.value = [...newAlgorithms];
      console.log(
        "SimulationPage - Updated selected algorithms:",
        selectedAlgorithms.value
      );
    }
  },
  { immediate: true }
);

// Watch for simulation completion to update tables
watch(
  simulationStatus,
  (newStatus) => {
    if (newStatus === 'completed') {
      console.log('Simulation completed - tables updated with backend data');
    }
  }
);

// Watch for num_agents changes to regenerate dummy assignments
watch(
  () => parameters.num_agents,
  (newNumAgents) => {
    if (simulationStatus.value === 'idle') {
      generateDummyACOAssignments();
      generateDummyPSOAssignments();
    }
  }
);

// Watch for tasks changes to re-validate
watch(
  () => props.tasks,
  (newTasks) => {
    console.log("SimulationPage - Tasks changed:", newTasks?.length);
    validateData();
  },
  { immediate: true, deep: true }
);

// Lifecycle
onMounted(() => {
  console.log("SimulationPage - Mounted with props:", {
    tasks: props.tasks?.length,
    algorithms: props.algorithms,
  });

  // Initialize with provided algorithms
  if (props.algorithms && props.algorithms.length > 0) {
    selectedAlgorithms.value = [...props.algorithms];
    console.log(
      "SimulationPage - Initialized with algorithms:",
      selectedAlgorithms.value
    );
  }

  // Initialize dummy assignments
  generateDummyACOAssignments();
  generateDummyPSOAssignments();
  
  validateData();
  initCharts();
});

// Modal functions
const openTaskModal = (assignment) => {
  modalData.value = { agent: assignment.agent, tasks: assignment.tasks };
  showTaskModal.value = true;
};

const closeTaskModal = () => {
  showTaskModal.value = false;
  modalData.value = { agent: '', tasks: [] };
};

// Reset simulation function
const resetSimulation = () => {
  // Reset all state
  logs.value = {};
  finalAssignment.value = {};
  bestMakespan.value = {};
  executionTime.value = {};
  loadBalanceIndex.value = {};
  computationTime.value = {};
  chartData.value = {};
  status.value = { ACO: 'Idle', PSO: 'Idle' };
  expandedTasks.value = { ACO: {}, PSO: {} };
  dummyFinalAssignment.value = null;
  
  // Reset backend result arrays and regenerate dummy assignments
  generateDummyACOAssignments();
  generateDummyPSOAssignments();
  simulationStatus.value = 'idle';
  
  // Reset charts
  if (chartACO) {
    chartACO.destroy();
    chartACO = null;
  }
  if (chartPSO) {
    chartPSO.destroy();
    chartPSO = null;
  }
  
  // Re-initialize charts
  nextTick(() => {
    initCharts();
  });
};

// Export functions
const exportJSON = (algorithm) => {
  const data = algorithm === 'ACO' ? acoFinalAssignment.value : psoFinalAssignment.value;
  
  if (!data || data.length === 0) return;
  
  // Filter out dummy preview data
  const exportData = data.filter(item => item.total_time !== "Preview...");
  if (exportData.length === 0) return;
  
  const jsonString = JSON.stringify(exportData, null, 2);
  const blob = new Blob([jsonString], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `${algorithm}_final_assignment.json`;
  link.click();
  
  URL.revokeObjectURL(url);
};

const exportCSV = (algorithm) => {
  const data = algorithm === 'ACO' ? acoFinalAssignment.value : psoFinalAssignment.value;
  
  if (!data || data.length === 0) return;
  
  // Filter out dummy preview data
  const exportData = data.filter(item => item.total_time !== "Preview...");
  if (exportData.length === 0) return;
  
  const headers = ['Agent', 'Tasks', 'Total Time'];
  const rows = exportData.map(row => [
    `"${row.agent}"`,
    `"${Array.isArray(row.tasks) ? row.tasks.join('; ') : row.tasks}"`,
    `"${row.total_time}"`
  ]);
  
  const csvContent = [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `${algorithm}_final_assignment.csv`;
  link.click();
  
  URL.revokeObjectURL(url);
};

// Toggle task expansion
const toggleTaskExpansion = (algorithm, index) => {
  expandedTasks.value[algorithm][index] = !expandedTasks.value[algorithm][index];
};

// Expose for parent component
defineExpose({
  runSimulation,
  resetSimulation,
});
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
</style>
