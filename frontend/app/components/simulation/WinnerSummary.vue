<template>
  <div 
    v-if="winner && winner !== 'Pending'"
    class="bg-gradient-to-r from-yellow-50 to-yellow-100 rounded-xl shadow-lg p-6 mb-6 border-2 border-yellow-400"
  >
    <div class="text-center">
      <h2 class="text-3xl font-bold mb-4 text-gray-800">
        🏆 Winner: <span :class="winner === 'ACO' ? 'text-blue-600' : 'text-red-600'">{{ winner }}</span>
      </h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <!-- ACO Stats -->
        <div 
          class="p-4 rounded-lg border-2 transition"
          :class="winner === 'ACO' ? 'bg-white border-blue-500 shadow-lg' : 'bg-gray-50 border-gray-300'"
        >
          <h3 class="text-xl font-semibold mb-3" :class="winner === 'ACO' ? 'text-blue-600' : 'text-gray-700'">
            ACO {{ winner === 'ACO' ? '👑' : '' }}
          </h3>
          <div class="space-y-2 text-left">
            <div class="flex justify-between">
              <span class="text-gray-600">Best Makespan:</span>
              <span class="font-bold">{{ acoStats.makespan }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Execution Time:</span>
              <span class="font-bold">{{ acoStats.executionTime }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Load Balance:</span>
              <span class="font-bold">{{ acoStats.loadBalance }}</span>
            </div>
          </div>
        </div>
        
        <!-- PSO Stats -->
        <div 
          class="p-4 rounded-lg border-2 transition"
          :class="winner === 'PSO' ? 'bg-white border-red-500 shadow-lg' : 'bg-gray-50 border-gray-300'"
        >
          <h3 class="text-xl font-semibold mb-3" :class="winner === 'PSO' ? 'text-red-600' : 'text-gray-700'">
            PSO {{ winner === 'PSO' ? '👑' : '' }}
          </h3>
          <div class="space-y-2 text-left">
            <div class="flex justify-between">
              <span class="text-gray-600">Best Makespan:</span>
              <span class="font-bold">{{ psoStats.makespan }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Execution Time:</span>
              <span class="font-bold">{{ psoStats.executionTime }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Load Balance:</span>
              <span class="font-bold">{{ psoStats.loadBalance }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="mt-6 text-sm text-gray-600">
        <p>💡 Winner determined by: Best Makespan → Execution Time → Load Balance Index</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  winner: { type: String, required: true },
  acoMakespan: { type: Number, default: null },
  acoExecutionTime: { type: Number, default: null },
  acoLoadBalance: { type: Number, default: null },
  psoMakespan: { type: Number, default: null },
  psoExecutionTime: { type: Number, default: null },
  psoLoadBalance: { type: Number, default: null }
});

const acoStats = computed(() => ({
  makespan: props.acoMakespan ? props.acoMakespan.toFixed(2) : '-',
  executionTime: props.acoExecutionTime ? props.acoExecutionTime.toFixed(3) + 's' : '-',
  loadBalance: props.acoLoadBalance ? props.acoLoadBalance.toFixed(2) : '-'
}));

const psoStats = computed(() => ({
  makespan: props.psoMakespan ? props.psoMakespan.toFixed(2) : '-',
  executionTime: props.psoExecutionTime ? props.psoExecutionTime.toFixed(3) + 's' : '-',
  loadBalance: props.psoLoadBalance ? props.psoLoadBalance.toFixed(2) : '-'
}));
</script>
