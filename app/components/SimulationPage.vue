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
          <h2 class="text-xl font-semibold text-gray-900 mb-4">
            Ant Colony Optimization (ACO) Results
          </h2>

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
            v-if="finalAssignment.ACO && finalAssignment.ACO.length > 0"
            class="mt-6"
          >
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              ACO Final Assignment (Best Makespan: {{ bestMakespan.ACO }})
            </h3>
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
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Total Time
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr
                    v-for="assignment in finalAssignment.ACO"
                    :key="assignment.agent"
                  >
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                    >
                      {{ assignment.agent }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                    >
                      {{ assignment.tasks.join(", ") }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                    >
                      {{ assignment.totalTime }}
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
          <h2 class="text-xl font-semibold text-gray-900 mb-4">
            Particle Swarm Optimization (PSO) Results
          </h2>

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
            v-if="finalAssignment.PSO && finalAssignment.PSO.length > 0"
            class="mt-6"
          >
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              PSO Final Assignment (Best Makespan: {{ bestMakespan.PSO }})
            </h3>
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
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Total Time
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr
                    v-for="assignment in finalAssignment.PSO"
                    :key="assignment.agent"
                  >
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                    >
                      {{ assignment.agent }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                    >
                      {{ assignment.tasks.join(", ") }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                    >
                      {{ assignment.totalTime }}
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
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, nextTick, onMounted } from "vue";
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
    chartACO.update();
  }

  if (chartPSO && chartData.value.PSO.labels.length > 0) {
    chartPSO.data.labels = chartData.value.PSO.labels;
    chartPSO.data.datasets[0].data = chartData.value.PSO.values;
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

  // Reset data for selected algorithms
  selectedAlgorithms.value.forEach((algo) => {
    logs.value[algo] = [];
    finalAssignment.value[algo] = [];
    bestMakespan.value[algo] = null;
    chartData.value[algo] = { labels: [], values: [] };
  });

  const numTasks = props.tasks.length;
  const numAgents = parameters.num_agents;

  // Run simulations for each selected algorithm
  const simulations = selectedAlgorithms.value.map(async (algorithm) => {
    // Generate different initial makespan for each algorithm
    let currentBest = 1800 + Math.random() * 200;
    if (algorithm === "PSO") {
      currentBest = 1750 + Math.random() * 150; // PSO typically starts slightly better
    }

    // Simulate iterations for this algorithm
    for (let i = 1; i <= parameters.num_iterations; i++) {
      // Simulate optimization (different rates for ACO vs PSO)
      let improvement = Math.random() * 20;
      if (algorithm === "ACO") {
        improvement = Math.random() * 15 + 5; // ACO has more consistent improvement
      } else {
        improvement = Math.random() * 25 + 2; // PSO has more variable improvement
      }

      currentBest = Math.max(currentBest - improvement, currentBest * 0.9);

      const log = `${algorithm} - Iteration ${i}: Best Makespan so far = ${currentBest.toFixed(
        2
      )}`;
      logs.value[algorithm].push(log);

      // Update chart data
      chartData.value[algorithm].labels.push(i);
      chartData.value[algorithm].values.push(currentBest);

      // Add small delay for visual effect
      await new Promise((resolve) => setTimeout(resolve, 50));

      // Update charts
      if (i % 3 === 0) {
        updateCharts();
      }
    }

    // Generate final assignment
    const tasksPerAgent = Math.floor(numTasks / numAgents);
    const remainingTasks = numTasks % numAgents;

    let taskIndex = 0;
    for (let agent = 1; agent <= numAgents; agent++) {
      const agentTasks = [];
      const tasksForThisAgent =
        tasksPerAgent + (agent <= remainingTasks ? 1 : 0);

      for (let j = 0; j < tasksForThisAgent; j++) {
        if (taskIndex < numTasks) {
          agentTasks.push(taskIndex + 1);
          taskIndex++;
        }
      }

      // Different performance characteristics for each algorithm
      let totalTime = 0;
      if (algorithm === "ACO") {
        totalTime = currentBest / numAgents + Math.random() * 30;
      } else {
        totalTime = currentBest / numAgents + Math.random() * 25;
      }

      finalAssignment.value[algorithm].push({
        agent: `${algorithm} Agent ${agent}`,
        tasks: agentTasks,
        totalTime: totalTime.toFixed(2),
      });
    }

    bestMakespan.value[algorithm] = currentBest.toFixed(2);
  });

  // Run all simulations in parallel
  await Promise.all(simulations);
  updateCharts();
  isRunning.value = false;
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

  validateData();
  initCharts();
});

// Expose for parent component
defineExpose({
  runSimulation,
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
