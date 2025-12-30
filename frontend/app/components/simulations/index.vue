<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <!-- Toast Notification -->
    <ToastNotification :show="toast.show" :message="toast.message" :type="toast.type" />

    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Swarm Intelligence Simulation</h1>
        <p class="text-gray-600">Run ACO or PSO algorithms on your experimental data</p>
      </div>

      <!-- Data Preview -->
      <DataPreview
        :tasks="props.tasks"
        :datasetHeaders="datasetHeaders"
        :dataLimit="dataLimit"
        :showAllData="showAllData"
        @edit-data="editData"
        @update:dataLimit="dataLimit = $event"
        @update:showAllData="showAllData = $event"
      />

      <!-- Algorithm Selection -->
      <AlgorithmSelection v-model="selectedAlgorithms" />

      <!-- Parameter Config -->
      <ParameterConfig
        :parameters="parameters"
        :selectedAlgorithms="selectedAlgorithms"
        :datasetHeaders="datasetHeaders"
        :isRunning="isRunning"
        :dataValidation="dataValidation"
        :filteredTasksLength="filteredTasks.length"
        @update:parameters="Object.assign(parameters, $event)"
        @run-simulation="runSimulation"
        @stop-simulation="stopSimulation"
      />

      <!-- Algorithm Results -->
      <div v-if="selectedAlgorithms.length > 0" class="space-y-6">
        <ACOResults v-if="selectedAlgorithms.includes('ACO')" ref="acoResultsRef"
          :status="status.ACO" :logs="logs.ACO" :bestMakespan="bestMakespan.ACO"
          :finalAssignment="acoFinalAssignment" :expandedTasks="expandedTasks.ACO"
          @export-json="exportJSON('ACO')" @export-csv="exportCSV('ACO')"
          @toggle-expansion="toggleTaskExpansion('ACO', $event)" />

        <PSOResults v-if="selectedAlgorithms.includes('PSO')" ref="psoResultsRef"
          :status="status.PSO" :logs="logs.PSO" :bestMakespan="bestMakespan.PSO"
          :finalAssignment="psoFinalAssignment" :expandedTasks="expandedTasks.PSO"
          @export-json="exportJSON('PSO')" @export-csv="exportCSV('PSO')"
          @toggle-expansion="toggleTaskExpansion('PSO', $event)" />
      </div>

      <!-- Data Validation -->
      <DataValidation :errors="dataValidation.errors" :warnings="dataValidation.warnings" />

      <!-- No Data State -->
      <div v-if="props.tasks.length === 0" class="bg-white rounded-xl border border-gray-200 shadow-none p-6">
        <div class="text-center py-12">
          <div class="text-gray-400 mb-4">
            <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No Data Available</h3>
          <p class="text-gray-500 mb-4">Please add some tasks to the data table before running simulations.</p>
          <button @click="$emit('back-to-table')" class="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Go to Data Table
          </button>
        </div>
      </div>

      <!-- Overall Best Result -->
      <OverallBestResult v-if="selectedAlgorithms.includes('ACO') && selectedAlgorithms.includes('PSO')"
        :bestMakespan="bestMakespan" :executionTime="executionTime" :loadBalanceIndex="loadBalanceIndex"
        :computationTime="computationTime" :winner="winner" :isWinner="isWinner" />

      <!-- AI Chat -->
      <AIChatWindow :simulationData="simulationData" :selectedAlgorithms="selectedAlgorithms" @show-toast="showToast" />

      <!-- Empty State -->
      <div v-if="selectedAlgorithms.length === 0" class="bg-white rounded-xl shadow-lg p-6">
        <div class="text-center py-12">
          <div class="text-gray-400 mb-4">
            <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Select Algorithms to Compare</h3>
          <p class="text-gray-500">Choose ACO, PSO, or both to run parallel simulations and compare their performance.</p>
          <div class="mt-4 text-sm text-orange-600 bg-orange-50 border border-orange-200 rounded-md p-3">
            <svg class="w-5 h-5 inline mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span class="font-medium">Warning:</span> No algorithms selected. Please choose at least one algorithm above to begin simulation.
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="mt-8 flex justify-center gap-4">
        <button @click="resetSimulation" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition duration-200">Reset Result</button>
        <button @click="$emit('back-to-table')" class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg transition duration-200">Back to Dashboard</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted, nextTick } from 'vue';
import ToastNotification from './ToastNotification.vue';
import DataPreview from './DataPreview.vue';
import AlgorithmSelection from './AlgorithmSelection.vue';
import ParameterConfig from './ParameterConfig.vue';
import ACOResults from './ACOResults.vue';
import PSOResults from './PSOResults.vue';
import OverallBestResult from './OverallBestResult.vue';
import DataValidation from './DataValidation.vue';
import AIChatWindow from './AIChatWindow.vue';

const props = defineProps({
  tasks: { type: Array, required: true },
  algorithms: { type: Array, default: () => [] }
});
const emit = defineEmits(['back-to-table', 'edit-data']);

// Component refs
const acoResultsRef = ref(null);
const psoResultsRef = ref(null);

// State
const selectedAlgorithms = ref([]);
const isRunning = ref(false);
const logs = ref({ ACO: [], PSO: [] });
const bestMakespan = ref({ ACO: null, PSO: null });
const executionTime = ref({ ACO: null, PSO: null });
const loadBalanceIndex = ref({ ACO: null, PSO: null });
const computationTime = ref({ ACO: null, PSO: null });
const status = ref({ ACO: 'Idle', PSO: 'Idle' });
const acoFinalAssignment = ref([]);
const psoFinalAssignment = ref([]);
const fullScheduleTable = ref({ aco: null, pso: null });
const fullResultData = ref({ aco: null, pso: null });
const agentInfoTable = ref({ aco: null, pso: null });
const toast = ref({ show: false, message: '', type: 'error' });
const dataValidation = ref({ isValid: true, errors: [], warnings: [] });
const dataLimit = ref(Math.max(1, Array.isArray(props.tasks) ? props.tasks.length : 1));
const showAllData = ref(false);
const expandedTasks = ref({ ACO: {}, PSO: {} });
const abortControllers = ref(new Map());

const parameters = reactive({
  num_default_agents: 10, n_iterations: 100, task_id_col: '', agent_id_col: '', dependency_col: '',
  random_seed: 42, n_ants: 50, alpha: 0.9, beta: 2.0, evaporation_rate: 0.3, pheromone_deposit: 100,
  n_particles: 50, w: 0.3, c1: 0.3, c2: 0.4, enable_dependencies: false
});

// Computed
const winner = computed(() => {
  if (!bestMakespan.value.ACO || !bestMakespan.value.PSO) return 'Pending';
  const acoMs = parseFloat(bestMakespan.value.ACO);
  const psoMs = parseFloat(bestMakespan.value.PSO);
  if (acoMs < psoMs) return 'ACO';
  if (psoMs < acoMs) return 'PSO';
  if (executionTime.value.ACO && executionTime.value.PSO) {
    if (parseFloat(executionTime.value.ACO) < parseFloat(executionTime.value.PSO)) return 'ACO';
    if (parseFloat(executionTime.value.PSO) < parseFloat(executionTime.value.ACO)) return 'PSO';
  }
  return 'ACO';
});

const isWinner = computed(() => ({ ACO: winner.value === 'ACO', PSO: winner.value === 'PSO' }));

const filteredTasks = computed(() => {
  if (!props.tasks || !Array.isArray(props.tasks) || props.tasks.length === 0) return [];
  if (showAllData.value) return props.tasks;
  return props.tasks.slice(0, Math.min(Math.max(1, dataLimit.value), props.tasks.length));
});

const datasetHeaders = computed(() => {
  if (!props.tasks || !Array.isArray(props.tasks) || props.tasks.length === 0) return [];
  const firstTask = props.tasks[0];
  return firstTask && typeof firstTask === 'object' ? Object.keys(firstTask) : [];
});

const dependencyColumn = computed(() => {
  const headers = datasetHeaders.value;
  const depFields = ['dependencies', 'depends_on', 'prerequisites', 'requires'];
  return headers.find(h => depFields.some(f => h.toLowerCase().includes(f.toLowerCase()))) || '';
});

const simulationData = computed(() => ({
  aco: selectedAlgorithms.value.includes('ACO') ? {
    bestMakespan: bestMakespan.value.ACO, executionTime: executionTime.value.ACO,
    loadBalanceIndex: loadBalanceIndex.value.ACO, finalAssignment: acoFinalAssignment.value,
    totalAgents: parameters.num_default_agents, totalTasks: filteredTasks.value.length
  } : null,
  pso: selectedAlgorithms.value.includes('PSO') ? {
    bestMakespan: bestMakespan.value.PSO, executionTime: executionTime.value.PSO,
    loadBalanceIndex: loadBalanceIndex.value.PSO, finalAssignment: psoFinalAssignment.value,
    totalAgents: parameters.num_default_agents, totalTasks: filteredTasks.value.length
  } : null
}));

// Functions
const showToast = (message, type = 'error') => {
  toast.value = { show: true, message, type };
  setTimeout(() => { toast.value.show = false; }, 3000);
};

const validateData = () => {
  const errors = [];
  const warnings = [];
  if (!props.tasks || !Array.isArray(props.tasks)) errors.push('Invalid tasks data format.');
  else if (props.tasks.length === 0) errors.push('No tasks available.');
  dataValidation.value = { isValid: errors.length === 0, errors, warnings };
};

const editData = () => emit('edit-data', props.tasks);

const resetSimulationStateForAlgo = (algo) => {
  status.value[algo] = 'Idle';
  logs.value[algo] = [];
  bestMakespan.value[algo] = null;
  executionTime.value[algo] = null;
  loadBalanceIndex.value[algo] = null;
  computationTime.value[algo] = null;
  if (algo === 'ACO') { acoFinalAssignment.value = []; if (acoResultsRef.value) acoResultsRef.value.resetChart(); }
  if (algo === 'PSO') { psoFinalAssignment.value = []; if (psoResultsRef.value) psoResultsRef.value.resetChart(); }
};

const resetSimulation = async () => {
  ['ACO', 'PSO'].forEach(resetSimulationStateForAlgo);
  isRunning.value = false;
};

const stopSimulation = () => {
  abortControllers.value.forEach((controller, algo) => {
    controller.abort();
    logs.value[algo].push('🛑 Simulation stopped by user');
    status.value[algo] = 'Stopped';
  });
  abortControllers.value.clear();
  isRunning.value = false;
  showToast('Simulation stopped', 'info');
};

const runSimulation = async () => {
  validateData();
  if (!filteredTasks.value.length) { showToast('Please add at least one task.', 'error'); return; }
  if (!dataValidation.value.isValid || !selectedAlgorithms.value.length) { showToast('Please select an algorithm and ensure data is valid.', 'error'); return; }

  await resetSimulation();
  isRunning.value = true;
  await nextTick();
  if (acoResultsRef.value) acoResultsRef.value.initChart();
  if (psoResultsRef.value) psoResultsRef.value.initChart();
  abortControllers.value.clear();

  const config = useRuntimeConfig();
  const runningSims = selectedAlgorithms.value.map(async (algorithm) => {
    const controller = new AbortController();
    abortControllers.value.set(algorithm, controller);
    try {
      const response = await fetch(`${config.public.API_URL}/stream_scheduling`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ algorithm, tasks: filteredTasks.value, parameters: { ...parameters } }),
        signal: controller.signal
      });
      if (!response.ok) throw new Error(response.statusText);
      if (!response.body) throw new Error('No response body');

      status.value[algorithm] = 'Running...';
      const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done || controller.signal.aborted) break;
        buffer += value;
        const messages = buffer.split('\n\n');
        buffer = messages.pop() || '';
        for (const msg of messages) {
          if (msg.startsWith('data:')) {
            try {
              const data = JSON.parse(msg.substring(5).trim());
              handleStreamEvent(algorithm, data);
            } catch (e) { console.warn('JSON parse error:', e.message); }
          }
        }
      }
    } catch (error) {
      if (error.name !== 'AbortError') {
        logs.value[algorithm].push(`❌ Simulation failed: ${error.message}`);
        status.value[algorithm] = 'Failed';
      }
    } finally { abortControllers.value.delete(algorithm); }
  });

  await Promise.all(runningSims);
  abortControllers.value.clear();
  isRunning.value = false;
};

const handleStreamEvent = (algorithm, data) => {
  if (!data || typeof data !== 'object') return;
  const resultsRef = algorithm === 'ACO' ? acoResultsRef.value : psoResultsRef.value;

  switch (data.type) {
    case 'log': case 'start':
      if (data.message) logs.value[algorithm].push(data.message);
      break;
    case 'iteration':
      if (data.log_message) logs.value[algorithm].push(data.log_message);
      if (typeof data.makespan === 'number') bestMakespan.value[algorithm] = data.makespan;
      if (resultsRef && typeof data.iteration === 'number' && typeof data.makespan === 'number') {
        resultsRef.updateChart(data.iteration, data.makespan);
      }
      break;
    case 'done':
      if (data.log_message) logs.value[algorithm].push(data.log_message);
      if (typeof data.makespan === 'number') bestMakespan.value[algorithm] = data.makespan;
      if (typeof data.computation_time === 'number') computationTime.value[algorithm] = data.computation_time;
      if (data.schedule && Array.isArray(data.schedule)) {
        const assignments = transformAssignmentData(data.schedule);
        if (algorithm === 'ACO') acoFinalAssignment.value = assignments;
        if (algorithm === 'PSO') psoFinalAssignment.value = assignments;
      }
      break;
    case 'final_metrics':
      if (typeof data.total_execution_time === 'number') executionTime.value[algorithm] = data.total_execution_time;
      if (typeof data.computation_time === 'number') computationTime.value[algorithm] = data.computation_time;
      if (typeof data.load_balance_index === 'number') loadBalanceIndex.value[algorithm] = data.load_balance_index;
      if (data.full_schedule_table) fullScheduleTable.value[algorithm.toLowerCase()] = data.full_schedule_table;
      if (data.full_result) fullResultData.value[algorithm.toLowerCase()] = data.full_result;
      if (data.agent_info_table) agentInfoTable.value[algorithm.toLowerCase()] = data.agent_info_table;
      status.value[algorithm] = 'Completed';
      break;
    case 'error':
      logs.value[algorithm].push(`❌ ERROR: ${data.message || 'Unknown error'}`);
      status.value[algorithm] = 'Failed';
      break;
  }
};

const transformAssignmentData = (schedule) => {
  if (!schedule || !Array.isArray(schedule)) return [];
  const agentMap = new Map();
  schedule.forEach(task => {
    if (!task?.agent_id || !task?.task_id) return;
    if (!agentMap.has(task.agent_id)) agentMap.set(task.agent_id, { tasks: [], finish_time: 0 });
    const data = agentMap.get(task.agent_id);
    data.tasks.push(task.task_id);
    data.finish_time = Math.max(data.finish_time, task.finish_time || 0);
  });
  return Array.from(agentMap.entries()).map(([agent, data]) => ({ agent, tasks: data.tasks, total_time: data.finish_time }));
};

const toggleTaskExpansion = (algorithm, agentId) => {
  if (!expandedTasks.value[algorithm]) expandedTasks.value[algorithm] = {};
  expandedTasks.value[algorithm][agentId] = !expandedTasks.value[algorithm][agentId];
};

const exportData = (algorithm, format) => {
  const algoKey = algorithm.toLowerCase();
  const fullResult = fullResultData.value[algoKey];
  const scheduleTable = fullScheduleTable.value[algoKey];
  const assignment = algorithm === 'ACO' ? acoFinalAssignment.value : psoFinalAssignment.value;
  if (!fullResult && (!assignment || !assignment.length)) { showToast(`No data to export for ${algorithm}`, 'info'); return; }

  let content = '', mimeType = '', ext = '';
  const timestamp = new Date().toISOString().replace(/:/g, '-').split('.')[0];

  if (format === 'json') {
    content = JSON.stringify(fullResult || assignment, null, 2);
    mimeType = 'application/json'; ext = 'json';
  } else {
    if (scheduleTable?.data) {
      const lines = [`${algorithm} Schedule Export`, `Generated,${timestamp}`, `Makespan,${fullResult?.makespan || 'N/A'}`, ''];
      lines.push(scheduleTable.columns.join(','));
      scheduleTable.data.forEach(row => lines.push(row.join(',')));
      content = lines.join('\n');
    } else {
      const headers = ['Agent', 'Tasks', 'Total Time'];
      const rows = assignment.map(r => [`"${r.agent}"`, `"${Array.isArray(r.tasks) ? r.tasks.join(';') : r.tasks}"`, `"${r.total_time}"`]);
      content = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    }
    mimeType = 'text/csv;charset=utf-8;'; ext = 'csv';
  }

  const blob = new Blob([content], { type: mimeType });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${algorithm.toLowerCase()}_schedule_${timestamp}.${ext}`;
  link.click();
  URL.revokeObjectURL(link.href);
  showToast(`${algorithm} data exported successfully`, 'success');
};

const exportJSON = (algo) => exportData(algo, 'json');
const exportCSV = (algo) => exportData(algo, 'csv');

// Watchers
watch(datasetHeaders, (newHeaders) => {
  if (newHeaders.length > 0 && !parameters.task_id_col) parameters.task_id_col = newHeaders[0];
}, { immediate: true });

watch([datasetHeaders, dependencyColumn], ([, depCol]) => {
  if (depCol && !parameters.dependency_col) { parameters.dependency_col = depCol; parameters.enable_dependencies = true; }
}, { immediate: true });

watch(() => props.tasks, () => { validateData(); dataLimit.value = props.tasks.length; }, { deep: true, immediate: true });

// Lifecycle
onMounted(() => {
  if (props.algorithms?.length) selectedAlgorithms.value = [...props.algorithms];
  validateData();
});

onUnmounted(() => {
  abortControllers.value.forEach(c => c.abort());
  abortControllers.value.clear();
});
</script>
