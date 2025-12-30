<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-none p-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold text-gray-900">Ant Colony Optimization (ACO) Results</h2>
      <span :class="['px-3 py-1 rounded-full text-xs font-medium', statusClass]">Status: {{ status }}</span>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Logs -->
      <div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">ACO Logs</h3>
        <div class="bg-gray-50 rounded-lg p-4 h-64 overflow-y-auto" ref="logsContainer">
          <div v-if="!logs || logs.length === 0" class="text-gray-500 text-center">Run simulation to see ACO logs</div>
          <div v-else class="space-y-1 text-sm font-mono">
            <div v-for="(log, index) in logs" :key="index" class="text-gray-700">{{ log }}</div>
          </div>
        </div>
      </div>
      <!-- Chart -->
      <div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">ACO Convergence Chart</h3>
        <div class="h-64"><canvas ref="chartCanvas" class="w-full h-full"></canvas></div>
      </div>
    </div>

    <!-- Assignment Table -->
    <div class="mt-6">
      <div class="flex justify-between items-center mb-2">
        <h3 class="text-lg font-medium text-gray-900">
          ACO Final Assignment <span v-if="bestMakespan">(Best Makespan: {{ parseFloat(bestMakespan).toFixed(2) }}s)</span>
        </h3>
        <div class="flex gap-2">
          <button @click="$emit('export-json')" class="px-3 py-1 text-xs bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">Export JSON</button>
          <button @click="$emit('export-csv')" class="px-3 py-1 text-xs bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors">Export CSV</button>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Agent</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Task List</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Total Time</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="finalAssignment.length === 0"><td colspan="3" class="px-6 py-4 text-center text-sm text-gray-500">No assignment data yet.</td></tr>
            <tr v-for="assignment in finalAssignment" :key="assignment.agent">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ assignment.agent }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">
                <div class="max-w-xs">
                  <div v-if="!expandedTasks[assignment.agent] && assignment.tasks && assignment.tasks.length > 10">
                    {{ assignment.tasks.slice(0, 10).join(", ") }}
                    <button @click="$emit('toggle-expansion', assignment.agent)" class="text-blue-600 hover:text-blue-800 ml-1">
                      ... (+{{ assignment.tasks.length - 10 }} more)
                    </button>
                  </div>
                  <div v-else>
                    <div class="max-h-32 overflow-y-auto">{{ Array.isArray(assignment.tasks) ? assignment.tasks.join(", ") : assignment.tasks }}</div>
                    <button v-if="assignment.tasks && assignment.tasks.length > 10 && expandedTasks[assignment.agent]" 
                      @click="$emit('toggle-expansion', assignment.agent)" class="text-blue-600 hover:text-blue-800 text-xs mt-1">Show less</button>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500 text-right font-mono">
                {{ typeof assignment.total_time === "number" ? assignment.total_time.toFixed(2) : assignment.total_time }}s
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps({
  status: { type: String, default: 'Idle' },
  logs: { type: Array, default: () => [] },
  bestMakespan: { type: [Number, String, null], default: null },
  finalAssignment: { type: Array, default: () => [] },
  expandedTasks: { type: Object, default: () => ({}) }
});

defineEmits(['export-json', 'export-csv', 'toggle-expansion']);

const chartCanvas = ref(null);
const logsContainer = ref(null);
let chart = null;

const statusClass = computed(() => ({
  'bg-gray-100 text-gray-800': props.status === 'Idle',
  'bg-blue-100 text-blue-800': props.status === 'Running...',
  'bg-green-100 text-green-800': props.status === 'Completed',
  'bg-red-100 text-red-800': props.status === 'Failed' || props.status === 'Stopped'
}));

const initChart = () => {
  if (!chartCanvas.value) return;
  if (chart) chart.destroy();
  chart = new Chart(chartCanvas.value.getContext('2d'), {
    type: 'line',
    data: { labels: [], datasets: [
      { label: 'ACO Best Makespan', data: [], borderColor: 'rgb(59, 130, 246)', backgroundColor: 'transparent', tension: 0.1 },
      { label: 'Best Point', data: [], backgroundColor: 'rgb(59, 130, 246)', pointRadius: 5, showLine: false }
    ]},
    options: { responsive: true, maintainAspectRatio: false, animation: { duration: 200 },
      scales: { y: { beginAtZero: false, title: { display: true, text: 'Makespan' }}, x: { title: { display: true, text: 'Iteration' }}}
    }
  });
};

const updateChart = (iteration, makespan) => {
  if (!chart) return;
  chart.data.labels.push(iteration);
  chart.data.datasets[0].data.push(makespan);
  const bestVal = Math.min(...chart.data.datasets[0].data);
  const bestIdx = chart.data.datasets[0].data.indexOf(bestVal);
  chart.data.datasets[1].data = chart.data.datasets[0].data.map((v, i) => i === bestIdx ? v : null);
  chart.update('none');
};

const resetChart = () => {
  if (!chart) return;
  chart.data.labels = [];
  chart.data.datasets[0].data = [];
  chart.data.datasets[1].data = [];
  chart.update();
};

onMounted(() => nextTick(initChart));

watch(() => props.logs, () => {
  nextTick(() => { if (logsContainer.value) logsContainer.value.scrollTop = logsContainer.value.scrollHeight; });
}, { deep: true });

defineExpose({ updateChart, resetChart, initChart });
</script>

<style scoped>
.overflow-y-auto::-webkit-scrollbar { width: 6px; }
.overflow-y-auto::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 3px; }
.overflow-y-auto::-webkit-scrollbar-thumb { background: #c1c1c1; border-radius: 3px; }
</style>
