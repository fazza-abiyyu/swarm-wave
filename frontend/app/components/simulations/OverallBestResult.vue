<template>
  <div v-if="bestMakespan.ACO && bestMakespan.PSO" class="bg-white rounded-xl border border-gray-200 shadow-none p-6 mt-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-4">Overall Best Result</h2>

    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Algorithm</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Best Makespan (s)</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Total Execution Time (ms)</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Load Balancing Index</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Computation Time (ms)</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr :class="[isWinner.ACO ? 'bg-blue-50 text-blue-700 font-bold' : 'text-gray-900']">
            <td class="px-6 py-4 whitespace-nowrap text-sm" :class="{ 'font-bold': isWinner.ACO }">ACO</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono" :class="{ 'font-bold': isWinner.ACO }">
              {{ bestMakespan.ACO ? parseFloat(bestMakespan.ACO).toFixed(2) : "N/A" }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono" :class="{ 'font-bold': isWinner.ACO }">
              {{ executionTime.ACO ? parseFloat(executionTime.ACO).toFixed(2) : "N/A" }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono" :class="{ 'font-bold': isWinner.ACO }">
              {{ loadBalanceIndex.ACO ? parseFloat(loadBalanceIndex.ACO).toFixed(4) : "N/A" }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono" :class="{ 'font-bold': isWinner.ACO }">
              {{ computationTime.ACO ? parseFloat(computationTime.ACO).toFixed(2) : "N/A" }}
            </td>
          </tr>
          <tr :class="[isWinner.PSO ? 'bg-blue-50 text-blue-700 font-bold' : 'text-gray-900']">
            <td class="px-6 py-4 whitespace-nowrap text-sm" :class="{ 'font-bold': isWinner.PSO }">PSO</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono" :class="{ 'font-bold': isWinner.PSO }">
              {{ bestMakespan.PSO ? parseFloat(bestMakespan.PSO).toFixed(2) : "N/A" }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono" :class="{ 'font-bold': isWinner.PSO }">
              {{ executionTime.PSO ? parseFloat(executionTime.PSO).toFixed(2) : "N/A" }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono" :class="{ 'font-bold': isWinner.PSO }">
              {{ loadBalanceIndex.PSO ? parseFloat(loadBalanceIndex.PSO).toFixed(4) : "N/A" }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono" :class="{ 'font-bold': isWinner.PSO }">
              {{ computationTime.PSO ? parseFloat(computationTime.PSO).toFixed(2) : "N/A" }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-6 pt-4 border-t border-gray-200 text-center">
      <span class="text-lg font-bold text-blue-600">Winner: {{ winner }}</span>
      <div v-if="winner !== 'Pending' && bestMakespan.ACO && bestMakespan.PSO" class="text-sm text-gray-600 mt-2">
        <span v-if="parseFloat(bestMakespan.ACO) === parseFloat(bestMakespan.PSO)">
          (Tied on makespan - {{ winner }} wins by execution time)
        </span>
        <span v-else>
          ({{ winner }} has better makespan: {{ winner === 'ACO' ? parseFloat(bestMakespan.ACO).toFixed(2) : parseFloat(bestMakespan.PSO).toFixed(2) }}s 
          vs {{ winner === 'ACO' ? parseFloat(bestMakespan.PSO).toFixed(2) : parseFloat(bestMakespan.ACO).toFixed(2) }}s)
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  bestMakespan: { type: Object, default: () => ({ ACO: null, PSO: null }) },
  executionTime: { type: Object, default: () => ({ ACO: null, PSO: null }) },
  loadBalanceIndex: { type: Object, default: () => ({ ACO: null, PSO: null }) },
  computationTime: { type: Object, default: () => ({ ACO: null, PSO: null }) },
  winner: { type: String, default: 'Pending' },
  isWinner: { type: Object, default: () => ({ ACO: false, PSO: false }) }
});
</script>
