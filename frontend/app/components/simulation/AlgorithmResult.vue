<template>
  <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-2xl font-bold text-gray-800">
        {{ algorithm }} Results
        <span v-if="isWinner" class="ml-2 text-yellow-500">🏆</span>
      </h2>
      <span 
        class="px-3 py-1 rounded-full text-sm font-semibold"
        :class="getStatusClass(status)"
      >
        {{ status }}
      </span>
    </div>
    
    <!-- Metrics -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-blue-50 p-4 rounded-lg">
        <div class="text-sm text-gray-600 mb-1">Best Makespan</div>
        <div class="text-2xl font-bold text-blue-600">
          {{ bestMakespan ? bestMakespan.toFixed(2) : '-' }}
        </div>
      </div>
      
      <div class="bg-green-50 p-4 rounded-lg">
        <div class="text-sm text-gray-600 mb-1">Execution Time</div>
        <div class="text-2xl font-bold text-green-600">
          {{ executionTime ? executionTime.toFixed(3) + 's' : '-' }}
        </div>
      </div>
      
      <div class="bg-purple-50 p-4 rounded-lg">
        <div class="text-sm text-gray-600 mb-1">Load Balance</div>
        <div class="text-2xl font-bold text-purple-600">
          {{ loadBalanceIndex ? loadBalanceIndex.toFixed(2) : '-' }}
        </div>
      </div>
      
      <div class="bg-orange-50 p-4 rounded-lg">
        <div class="text-sm text-gray-600 mb-1">Computation Time</div>
        <div class="text-2xl font-bold text-orange-600">
          {{ computationTime ? computationTime.toFixed(3) + 's' : '-' }}
        </div>
      </div>
    </div>
    
    <!-- Chart -->
    <div class="mb-6">
      <h3 class="text-lg font-semibold mb-3 text-gray-700">Convergence Chart</h3>
      <div class="bg-gray-50 p-4 rounded-lg">
        <canvas :ref="setChartRef" class="w-full" style="max-height: 300px;"></canvas>
      </div>
    </div>
    
    <!-- Logs -->
    <div class="mb-6">
      <h3 class="text-lg font-semibold mb-3 text-gray-700">Execution Logs</h3>
      <div 
        :ref="setLogsRef"
        class="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-y-auto"
        style="max-height: 200px;"
      >
        <div v-for="(log, idx) in logs" :key="idx" class="mb-1">
          {{ log }}
        </div>
        <div v-if="logs.length === 0" class="text-gray-500">
          No logs yet...
        </div>
      </div>
    </div>
    
    <!-- Assignment Table -->
    <div v-if="assignment && assignment.length > 0">
      <h3 class="text-lg font-semibold mb-3 text-gray-700">Task Assignment</h3>
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Agent</th>
              <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Tasks</th>
              <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Total Time</th>
              <th class="px-4 py-2 text-center text-sm font-semibold text-gray-700">Actions</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="(item, idx) in assignment" :key="idx">
              <tr class="border-t hover:bg-gray-50">
                <td class="px-4 py-2 font-medium">{{ item.agent }}</td>
                <td class="px-4 py-2">
                  <span v-if="!expandedTasks[item.agent]">
                    {{ item.tasks.slice(0, 3).join(', ') }}
                    <span v-if="item.tasks.length > 3" class="text-gray-500">
                      ... ({{ item.tasks.length - 3 }} more)
                    </span>
                  </span>
                  <span v-else>
                    {{ item.tasks.join(', ') }}
                  </span>
                </td>
                <td class="px-4 py-2">{{ item.total_time.toFixed(2) }}</td>
                <td class="px-4 py-2 text-center">
                  <button
                    v-if="item.tasks.length > 3"
                    @click="toggleExpansion(item.agent)"
                    class="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    {{ expandedTasks[item.agent] ? 'Show Less' : 'Show More' }}
                  </button>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Export Buttons -->
    <div class="mt-6 flex gap-3">
      <button
        @click="$emit('export-json')"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        📥 Export JSON
      </button>
      <button
        @click="$emit('export-csv')"
        class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
      >
        📊 Export CSV
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps({
  algorithm: { type: String, required: true },
  status: { type: String, required: true },
  bestMakespan: { type: Number, default: null },
  executionTime: { type: Number, default: null },
  loadBalanceIndex: { type: Number, default: null },
  computationTime: { type: Number, default: null },
  logs: { type: Array, default: () => [] },
  assignment: { type: Array, default: () => [] },
  isWinner: { type: Boolean, default: false }
});

const emit = defineEmits(['export-json', 'export-csv']);

const chartRef = ref(null);
const logsRef = ref(null);
const expandedTasks = ref({});
let chart = null;

const setChartRef = (el) => {
  chartRef.value = el;
};

const setLogsRef = (el) => {
  logsRef.value = el;
};

const getStatusClass = (status) => {
  const classes = {
    'Idle': 'bg-gray-200 text-gray-700',
    'Running...': 'bg-blue-200 text-blue-700',
    'Done': 'bg-green-200 text-green-700',
    'Error': 'bg-red-200 text-red-700',
    'Stopped': 'bg-yellow-200 text-yellow-700'
  };
  return classes[status] || 'bg-gray-200 text-gray-700';
};

const toggleExpansion = (agent) => {
  expandedTasks.value[agent] = !expandedTasks.value[agent];
};

const initChart = () => {
  if (!chartRef.value) return;
  
  const existingChart = Chart.getChart(chartRef.value);
  if (existingChart) {
    existingChart.destroy();
  }
  
  const ctx = chartRef.value.getContext('2d');
  const color = props.algorithm === 'ACO' ? 'rgb(59, 130, 246)' : 'rgb(239, 68, 68)';
  
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Best Makespan',
          data: [],
          borderColor: color,
          backgroundColor: color + '20',
          tension: 0.1
        },
        {
          label: 'Average Makespan',
          data: [],
          borderColor: color + '80',
          backgroundColor: color + '10',
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: false
        }
      }
    }
  });
};

onMounted(() => {
  initChart();
});

onBeforeUnmount(() => {
  if (chart) {
    chart.destroy();
  }
});

// Expose chart for parent component to update
defineExpose({
  chart,
  logsRef
});
</script>
