<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <!-- Toast Notification -->
    <ToastNotification 
      :show="toast.show" 
      :message="toast.message" 
      :type="toast.type" 
    />

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

      <!-- Data Preview Component -->
      <DataPreview
        v-if="filteredTasks && filteredTasks.length > 0"
        :tasks="props.tasks"
        :limit="dataLimit"
        :show-all="showAllData"
        @update:limit="dataLimit = $event"
        @update:show-all="showAllData = $event"
      />

      <!-- Empty State -->
      <div
        v-else
        class="bg-white rounded-xl shadow-lg p-6 mb-6"
      >
        <div class="text-center py-8 text-gray-500">
          <svg class="w-12 h-12 mx-auto mb-2 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
          </svg>
          <p>No data available</p>
        </div>
      </div>

      <!-- Algorithm Selector Component -->
      <AlgorithmSelector
        :selected-algorithms="selectedAlgorithms"
        @update:selected-algorithms="selectedAlgorithms = $event"
      />

      <!-- Parameters Form Component -->
      <ParametersForm
        :parameters="parameters"
        :headers="datasetHeaders"
        :selected-algorithms="selectedAlgorithms"
        @update:parameters="updateParameters"
      />

      <!-- Data Validation -->
      <div
        v-if="!dataValidation.isValid || dataValidation.warnings.length > 0"
        class="bg-white rounded-xl shadow-lg p-6 mb-6"
      >
        <h3 class="text-lg font-semibold mb-3 text-gray-800">⚠️ Data Validation</h3>
        
        <div v-if="dataValidation.errors.length > 0" class="mb-4">
          <p class="text-sm font-medium text-red-700 mb-2">Errors:</p>
          <ul class="list-disc list-inside space-y-1">
            <li v-for="(error, idx) in dataValidation.errors" :key="idx" class="text-red-600 text-sm">
              {{ error }}
            </li>
          </ul>
        </div>
        
        <div v-if="dataValidation.warnings.length > 0">
          <p class="text-sm font-medium text-yellow-700 mb-2">Warnings:</p>
          <ul class="list-disc list-inside space-y-1">
            <li v-for="(warning, idx) in dataValidation.warnings" :key="idx" class="text-yellow-600 text-sm">
              {{ warning }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Winner Summary Component -->
      <WinnerSummary
        v-if="selectedAlgorithms.length > 1"
        :winner="winner"
        :aco-makespan="bestMakespan.ACO"
        :aco-execution-time="executionTime.ACO"
        :aco-load-balance="loadBalanceIndex.ACO"
        :pso-makespan="bestMakespan.PSO"
        :pso-execution-time="executionTime.PSO"
        :pso-load-balance="loadBalanceIndex.PSO"
      />

      <!-- Algorithm Results -->
      <div v-if="selectedAlgorithms.length > 0" class="space-y-6">
        <AlgorithmResult
          v-for="algo in selectedAlgorithms"
          :key="algo"
          :ref="el => setResultRef(algo, el)"
          :algorithm="algo"
          :status="status[algo]"
          :best-makespan="bestMakespan[algo]"
          :execution-time="executionTime[algo]"
          :load-balance-index="loadBalanceIndex[algo]"
          :computation-time="computationTime[algo]"
          :logs="logs[algo]"
          :assignment="algo === 'ACO' ? acoFinalAssignment : psoFinalAssignment"
          :is-winner="isWinner[algo]"
          @export-json="() => exportJSON(algo)"
          @export-csv="() => exportCSV(algo)"
        />
      </div>

      <!-- AI Chat Assistant Component -->
      <AiChatAssistant
        :chat-history="chatHistory"
        :ai-loading="aiLoading"
        :ai-error="aiError"
        :ai-language="aiLanguage"
        :is-streaming="isStreaming"
        @send-message="handleSendMessage"
        @clear-chat="clearChat"
        @copy-to-clipboard="copyToClipboard"
      />

      <!-- Action Buttons -->
      <div class="mt-8 flex justify-center gap-4">
        <button
          @click="$emit('back-to-table')"
          class="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors font-medium"
        >
          ← Back to Table
        </button>
        <button
          v-if="!isRunning"
          @click="runSimulation"
          :disabled="selectedAlgorithms.length === 0 || !dataValidation.isValid"
          class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ▶ Run Simulation
        </button>
        <button
          v-else
          @click="stopSimulation"
          class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
        >
          ⏹ Stop Simulation
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, nextTick, onMounted, onUnmounted, computed } from "vue";
import { useAiChatStream } from "~/composables/useAiChatStream";

// Import child components
import ToastNotification from "./simulation/ToastNotification.vue";
import DataPreview from "./simulation/DataPreview.vue";
import AlgorithmSelector from "./simulation/AlgorithmSelector.vue";
import ParametersForm from "./simulation/ParametersForm.vue";
import AlgorithmResult from "./simulation/AlgorithmResult.vue";
import WinnerSummary from "./simulation/WinnerSummary.vue";
import AiChatAssistant from "./simulation/AiChatAssistant.vue";

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
const fullScheduleTable = ref({ aco: null, pso: null });
const fullResultData = ref({ aco: null, pso: null });
const agentInfoTable = ref({ aco: null, pso: null });
const toast = ref({ show: false, message: "", type: "error" });
const dataValidation = ref({ isValid: true, errors: [], warnings: [], summary: {} });
const dataLimit = ref(Math.max(1, Array.isArray(props.tasks) ? props.tasks.length : 1));
const showAllData = ref(false);
const abortControllers = ref(new Map());

// Refs for algorithm result components
const resultRefs = ref({});

const parameters = reactive({
  num_default_agents: 10,
  n_iterations: 100,
  task_id_col: '',
  agent_id_col: '',
  dependency_col: '',
  random_seed: 42,
  n_ants: 50,
  alpha: 0.9,
  beta: 2.0,
  evaporation_rate: 0.3,
  pheromone_deposit: 100,
  n_particles: 50,
  w: 0.3,
  c1: 0.3,
  c2: 0.4,
  enable_dependencies: false
});

// Helper function to set result component refs
const setResultRef = (algo, el) => {
  if (el) {
    resultRefs.value[algo] = el;
  }
};

// Computed property for determining winner
const winner = computed(() => {
  if (!bestMakespan.value.ACO || !bestMakespan.value.PSO) {
    return "Pending";
  }
  
  const acoMakespan = parseFloat(bestMakespan.value.ACO);
  const psoMakespan = parseFloat(bestMakespan.value.PSO);
  
  if (acoMakespan < psoMakespan) {
    return "ACO";
  } else if (psoMakespan < acoMakespan) {
    return "PSO";
  }
  
  if (executionTime.value.ACO && executionTime.value.PSO) {
    const acoTime = parseFloat(executionTime.value.ACO);
    const psoTime = parseFloat(executionTime.value.PSO);
    
    if (acoTime < psoTime) {
      return "ACO";
    } else if (psoTime < acoTime) {
      return "PSO";
    }
  }
  
  if (loadBalanceIndex.value.ACO && loadBalanceIndex.value.PSO) {
    const acoBalance = parseFloat(loadBalanceIndex.value.ACO);
    const psoBalance = parseFloat(loadBalanceIndex.value.PSO);
    
    if (acoBalance > psoBalance) {
      return "ACO";
    } else if (psoBalance > acoBalance) {
      return "PSO";
    }
  }
  
  return "ACO";
});

const isWinner = computed(() => ({
  ACO: winner.value === "ACO",
  PSO: winner.value === "PSO"
}));

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

const dependencyColumn = computed(() => {
  const headers = datasetHeaders.value;
  const dependencyFields = ['dependencies', 'depends_on', 'prerequisites', 'requires'];
  return headers.find(header => 
    dependencyFields.some(field => header.toLowerCase().includes(field.toLowerCase()))
  ) || '';
});

// --- SIMULATION LOGIC ---
const resetSimulationStateForAlgo = (algo) => {
  status.value[algo] = "Idle";
  logs.value[algo] = [];
  bestMakespan.value[algo] = null;
  executionTime.value[algo] = null;
  loadBalanceIndex.value[algo] = null;
  computationTime.value[algo] = null;
  if (algo === 'ACO') acoFinalAssignment.value = [];
  if (algo === 'PSO') psoFinalAssignment.value = [];

  const resultComponent = resultRefs.value[algo];
  if (resultComponent && resultComponent.chart) {
    resultComponent.chart.data.labels = [];
    resultComponent.chart.data.datasets[0].data = [];
    resultComponent.chart.data.datasets[1].data = [];
    resultComponent.chart.update();
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
  abortControllers.value.clear();

  const runningSims = selectedAlgorithms.value.map(async (algorithm) => {
    const requestBody = {
      algorithm: algorithm,
      tasks: filteredTasks.value,
      parameters: { ...parameters }
    };

    const controller = new AbortController();
    abortControllers.value.set(algorithm, controller);
    const config = useRuntimeConfig();

    try {
      const response = await fetch(`${config.public.API_URL}/stream_scheduling`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
        signal: controller.signal
      });

      if (!response.ok || !response.body) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      status.value[algorithm] = "Running...";
      const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        if (controller.signal.aborted) {
          break;
        }
        
        buffer += value;
        const messages = buffer.split('\n\n');
        buffer = messages.pop() || '';
        
        for (const message of messages) {
          if (message.startsWith('data:')) {
            const jsonData = message.substring(5).trim();
            if (jsonData && jsonData !== '') {
              try {
                const parsedData = JSON.parse(jsonData);
                handleStreamEvent(algorithm, parsedData);
              } catch (jsonError) {
                console.warn(`JSON parse error for ${algorithm}:`, jsonError.message);
                logs.value[algorithm].push(`⚠️ Data parsing warning: ${jsonError.message}`);
              }
            }
          }
        }
      }
      
      if (buffer.trim() && buffer.startsWith('data:')) {
        const jsonData = buffer.substring(5).trim();
        if (jsonData) {
          try {
            const parsedData = JSON.parse(jsonData);
            handleStreamEvent(algorithm, parsedData);
          } catch (jsonError) {
            logs.value[algorithm].push(`⚠️ Final data parsing warning: ${jsonError.message}`);
          }
        }
      }
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log(`${algorithm} simulation was aborted by user`);
      } else {
        console.error(`Error with ${algorithm} simulation:`, error);
        logs.value[algorithm].push(`❌ Simulation failed: ${error.message}`);
        status.value[algorithm] = "Failed";
      }
    } finally {
      abortControllers.value.delete(algorithm);
    }
  });

  await Promise.all(runningSims);
  abortControllers.value.clear();
  isRunning.value = false;
};

const handleStreamEvent = (algorithm, data) => {
  try {
    if (!data || typeof data !== 'object') {
      console.warn(`Invalid data received for ${algorithm}:`, data);
      return;
    }

    const resultComponent = resultRefs.value[algorithm];
    const chart = resultComponent?.chart;

    const processLog = (message) => {
      if (message && typeof message === 'string') {
        logs.value[algorithm].push(message);
        nextTick(() => {
          if (resultComponent?.logsRef) {
            resultComponent.logsRef.scrollTop = resultComponent.logsRef.scrollHeight;
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
            const bestVal = Math.min(...chart.data.datasets[0].data);
            const bestIndex = chart.data.datasets[0].data.indexOf(bestVal);
            chart.data.datasets[1].data = chart.data.datasets[0].data.map((val, idx) => idx === bestIndex ? val : null);
            chart.update('none');
          } catch (chartError) {
            console.warn(`Chart update error for ${algorithm}:`, chartError.message);
          }
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
        
        if (data.full_schedule_table) {
          fullScheduleTable.value[algorithm.toLowerCase()] = data.full_schedule_table;
          processLog(`Full schedule table received: ${data.full_schedule_table.total_rows} rows`);
        }
        
        if (data.full_result) {
          fullResultData.value[algorithm.toLowerCase()] = data.full_result;
          processLog(`Full result data saved for export`);
        }
        
        if (data.agent_info_table) {
          agentInfoTable.value[algorithm.toLowerCase()] = data.agent_info_table;
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
const validateData = () => {
  const errors = [];
  const warnings = [];
  
  if (!props.tasks || !Array.isArray(props.tasks)) {
    errors.push("Invalid tasks data format.");
  } else if (props.tasks.length === 0) {
    errors.push("No tasks available.");
  } else {
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
  ['ACO', 'PSO'].forEach(resetSimulationStateForAlgo);
  isRunning.value = false;
};

const stopSimulation = () => {
  abortControllers.value.forEach((controller, algorithm) => {
    controller.abort();
    logs.value[algorithm].push(`🛑 Simulation stopped by user`);
    status.value[algorithm] = "Stopped";
  });
  
  abortControllers.value.clear();
  isRunning.value = false;
  showToast("Simulation stopped", 'info');
};

const editData = () => {
  emit("edit-data", props.tasks);
};

const exportData = (algorithm, format) => {
  const algoKey = algorithm.toLowerCase();
  const fullResult = fullResultData.value[algoKey];
  const scheduleTable = fullScheduleTable.value[algoKey];
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
    content = JSON.stringify(fullResult || assignment, null, 2);
    mimeType = 'application/json';
    fileExtension = 'json';
  } else {
    if (scheduleTable && scheduleTable.data) {
      const csvLines = [];
      const agentInfo = agentInfoTable.value[algoKey];
      
      if (fullResult) {
        csvLines.push(`${fullResult.algorithm} Schedule Export`);
        csvLines.push(`Generated,${fullResult.timestamp || timestamp}`);
        csvLines.push(`Makespan,${fullResult.makespan || 'N/A'}`);
        csvLines.push(`Load Balance Index,${fullResult.load_balance_index || 'N/A'}`);
        csvLines.push(`Computation Time (ms),${fullResult.computation_time || 'N/A'}`);
        csvLines.push(`Total Tasks,${fullResult.total_tasks || scheduleTable.total_rows}`);
        csvLines.push(`Total Agents,${fullResult.total_agents || 'N/A'}`);
        csvLines.push('');
      }
      
      if (agentInfo && agentInfo.data) {
        csvLines.push('AGENT HETEROGENITAS');
        csvLines.push(agentInfo.columns.join(','));
        agentInfo.data.forEach(row => {
          csvLines.push(row.join(','));
        });
        csvLines.push('');
      }
      
      const agentGroups = {};
      const agentIdIndex = scheduleTable.columns.indexOf('agent_id');
      
      scheduleTable.data.forEach(row => {
        const agentId = row[agentIdIndex];
        if (!agentGroups[agentId]) {
          agentGroups[agentId] = [];
        }
        agentGroups[agentId].push(row);
      });
      
      const sortedAgents = Object.keys(agentGroups).sort((a, b) => {
        const numA = parseInt(a.match(/\d+/) || 0);
        const numB = parseInt(b.match(/\d+/) || 0);
        return numA - numB;
      });
      
      sortedAgents.forEach((agentId) => {
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
        
        agentGroups[agentId].forEach(row => {
          const formattedRow = row.map(cell => {
            if (typeof cell === 'string' && isNaN(cell)) {
              return cell;
            }
            return cell;
          }).join(',');
          csvLines.push(formattedRow);
        });
        
        const totalTasks = agentGroups[agentId].length;
        const finishTimeIndex = scheduleTable.columns.indexOf('finish_time');
        const maxFinishTime = Math.max(...agentGroups[agentId].map(r => r[finishTimeIndex]));
        csvLines.push(`${agentId} Total,${totalTasks} tasks,Total Time,${maxFinishTime.toFixed(2)}`);
        csvLines.push('');
      });
      
      content = csvLines.join('\n');
    } else {
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

const updateParameters = (newParams) => {
  Object.assign(parameters, newParams);
};

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => showToast('Copied to clipboard', 'success'));
};

const getDataTypes = () => {
  if (!filteredTasks.value.length || !datasetHeaders.value.length) return {};
  
  const types = {};
  const sampleSize = Math.min(10, filteredTasks.value.length);
  
  datasetHeaders.value.forEach(header => {
    const sampleValues = filteredTasks.value.slice(0, sampleSize)
      .map(task => task[header])
      .filter(val => val !== null && val !== undefined && val !== '');
    
    if (sampleValues.length === 0) {
      types[header] = 'empty';
      return;
    }
    
    const numericValues = sampleValues.filter(val => !isNaN(val) && isFinite(val));
    if (numericValues.length === sampleValues.length) {
      const hasDecimals = numericValues.some(val => val % 1 !== 0);
      types[header] = hasDecimals ? 'float' : 'integer';
    } else {
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

const handleSendMessage = async (message) => {
  const dataSpecification = {
    totalRows: filteredTasks.value.length,
    totalColumns: datasetHeaders.value.length,
    columns: datasetHeaders.value,
    sampleData: filteredTasks.value.slice(0, 3),
    dataTypes: getDataTypes(),
    dataLimitations: {
      originalRows: props.tasks.length,
      filteredRows: filteredTasks.value.length,
      showAllData: showAllData.value,
      dataLimit: dataLimit.value
    }
  };

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
  
  await sendMessage(message, simulationData, selectedAlgorithms.value.join('_'));
};

// --- LIFECYCLE HOOKS ---
onMounted(() => {
  if (props.algorithms && props.algorithms.length > 0) {
    selectedAlgorithms.value = [...props.algorithms];
  }
  validateData();
});

onUnmounted(() => {
  abortControllers.value.forEach((controller) => {
    controller.abort();
  });
  abortControllers.value.clear();
});

watch(() => props.tasks, () => {
  validateData();
  dataLimit.value = props.tasks.length;
}, { deep: true, immediate: true });

watch(dataLimit, (newValue) => {
  if (newValue <= 0) {
    dataLimit.value = 1;
  } else if (newValue > props.tasks.length) {
    dataLimit.value = props.tasks.length;
  }
}, { immediate: true });

watch(datasetHeaders, (newHeaders) => {
  if (newHeaders.length > 0 && (!parameters.task_id_col || parameters.task_id_col === '')) {
    parameters.task_id_col = newHeaders[0];
  }
}, { immediate: true });

watch([datasetHeaders, dependencyColumn], ([newHeaders, newDependencyCol]) => {
  if (newDependencyCol && (!parameters.dependency_col || parameters.dependency_col === '')) {
    parameters.dependency_col = newDependencyCol;
    parameters.enable_dependencies = true;
  } else if (!newDependencyCol && parameters.dependency_col) {
    parameters.dependency_col = '';
    parameters.enable_dependencies = false;
  }
}, { immediate: true });
</script>

<style scoped>
/* Custom scrollbar */
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
