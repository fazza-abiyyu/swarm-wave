<template>
  <div class="dynamic-table-container p-4">
    <!-- Error Message -->
    <div v-if="jsonError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
      <p class="text-red-600 text-sm">Invalid JSON format</p>
    </div>

    <!-- Controls -->
    <TableControls
      :showJsonEditor="showJsonEditor"
      @add-row="addRow"
      @add-column="addColumn"
      @import-json="importJson"
      @import-csv="importCsv"
      @export-json="exportJson"
      @export-csv="exportCsv"
      @toggle-json="toggleJsonEditor"
    />

    <!-- JSON Editor -->
    <JsonEditor
      v-model="jsonInput"
      :show="showJsonEditor"
      :error="jsonError"
      @update:modelValue="updateFromJson"
      @load-sample="loadSampleData"
    />

    <!-- Data Table -->
    <DataTable
      :headers="headers"
      :columnData="columnData"
      :cellErrors="cellErrors"
      @update-header="updateHeader"
      @remove-column="removeColumn"
      @remove-row="removeRow"
      @cell-input="handleCellInput"
      @cell-blur="validateAndUpdateCell"
    />

    <!-- Simulation Button -->
    <div class="simulation-section mt-6 text-center">
      <button ref="simulationButton" @click="openSimulationModal" :disabled="!isTableValid"
        class="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed"
        :class="{ 'opacity-50 cursor-not-allowed': !isTableValid }">
        {{ isTableValid ? 'Run Simulation' : 'Please Correct the Input' }}
      </button>
    </div>

    <!-- Floating Scroll Button -->
    <FloatingScrollButton :show="showFloatingButton" @click="scrollToSimulationButton" />

    <!-- Simulation Modal -->
    <SimulationModal
      :show="showSimulationModal"
      v-model="selectedAlgorithms"
      @close="closeSimulationModal"
      @run="runSimulation"
    />

    <!-- Delete Row Modal -->
    <ConfirmModal
      :show="showDeleteRowModal"
      title="Confirm Delete"
      message="Are you sure you want to delete this row? This action cannot be undone."
      @confirm="confirmDeleteRow"
      @cancel="showDeleteRowModal = false"
    />

    <!-- Delete Column Modal -->
    <ConfirmModal
      :show="showDeleteColumnModal"
      title="Confirm Delete"
      message="Are you sure you want to delete this column? This action cannot be undone."
      @confirm="confirmDeleteColumn"
      @cancel="showDeleteColumnModal = false"
    />

    <!-- Toast -->
    <TableToast :show="showToast" :message="toastMessage" @close="showToast = false" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import TableControls from './TableControls.vue';
import JsonEditor from './JsonEditor.vue';
import DataTable from './DataTable.vue';
import SimulationModal from './SimulationModal.vue';
import ConfirmModal from './ConfirmModal.vue';
import TableToast from './TableToast.vue';
import FloatingScrollButton from './FloatingScrollButton.vue';

const props = defineProps({ initialData: { type: Array, default: () => [] } });
const emit = defineEmits(['data-updated', 'run-simulation']);

// State
const headers = ref(['Task_ID', 'CPU_Usage', 'RAM_Usage', 'Priority', 'Execution_Time (s)', 'Depends_On_Task_ID']);
const columnData = ref([]);
const cellErrors = ref({});
const jsonInput = ref('');
const jsonError = ref(false);
const showJsonEditor = ref(false);
const showSimulationModal = ref(false);
const selectedAlgorithms = ref([]);
const toastMessage = ref('');
const showToast = ref(false);
const showDeleteRowModal = ref(false);
const showDeleteColumnModal = ref(false);
const pendingDeleteRowIndex = ref(null);
const pendingDeleteColumnIndex = ref(null);
const simulationButton = ref(null);
const showFloatingButton = ref(false);

// Default dataset
const defaultDataset = [
  {"Task_ID": "1", "CPU_Usage": "37", "RAM_Usage": "2612", "Priority": "2", "Execution_Time (s)": "1.27", "Depends_On_Task_ID": ""},
  {"Task_ID": "2", "CPU_Usage": "86", "RAM_Usage": "11761", "Priority": "3", "Execution_Time (s)": "3.71", "Depends_On_Task_ID": ""},
  {"Task_ID": "3", "CPU_Usage": "44", "RAM_Usage": "4610", "Priority": "2", "Execution_Time (s)": "8.53", "Depends_On_Task_ID": ""},
  {"Task_ID": "4", "CPU_Usage": "82", "RAM_Usage": "12604", "Priority": "3", "Execution_Time (s)": "7.31", "Depends_On_Task_ID": "3"},
  {"Task_ID": "5", "CPU_Usage": "59", "RAM_Usage": "15945", "Priority": "1", "Execution_Time (s)": "1.76", "Depends_On_Task_ID": ""}
];

// Computed
const validationErrors = computed(() => {
  const errors = [];
  headers.value.forEach((header, index) => {
    if (!header || header.trim() === '') errors.push(`Column ${index + 1} header is required`);
  });
  headers.value.forEach((header, colIndex) => {
    columnData.value[colIndex]?.forEach((value, rowIndex) => {
      if (colIndex === 0 && (!value || value.trim() === '')) errors.push(`Row ${rowIndex + 1}, Column "${header}" is empty`);
    });
  });
  headers.value.forEach((header, colIndex) => {
    if (colIndex === 0) return;
    columnData.value[colIndex]?.forEach((value, rowIndex) => {
      const trimmed = typeof value === 'string' ? value.trim() : String(value ?? '');
      if (!trimmed) return;
      const headerLower = header.toLowerCase();
      if (headerLower.includes('depend') || headerLower.includes('prerequisite')) {
        if (!/^(\d+([;,]\d+)*|none|null|0)$/i.test(trimmed)) errors.push(`Row ${rowIndex + 1}, Column "${header}" format error`);
      } else if (!/^-?(?:\d+(?:\.\d*)?|\.\d+)$/.test(trimmed)) {
        errors.push(`Row ${rowIndex + 1}, Column "${header}" must be a number`);
      }
    });
  });
  return errors;
});

const isTableValid = computed(() => validationErrors.value.length === 0 && (columnData.value[0]?.length || 0) > 0);

const getTableData = () => {
  return Array.from({ length: columnData.value[0]?.length || 0 }, (_, rowIndex) => {
    const row = {};
    headers.value.forEach((header, colIndex) => { row[header] = columnData.value[colIndex]?.[rowIndex] || ''; });
    return row;
  });
};

// Methods
const showToastMessage = (message) => {
  toastMessage.value = message;
  showToast.value = true;
  setTimeout(() => { showToast.value = false; }, 3000);
};

const validateCell = (value, header = '', colIndex = -1) => {
  if (value === null || value === undefined) return false;
  if (typeof value !== 'string') return false;
  if (value.trim() === '') return false;
  if (colIndex === 0) return true;
  const headerLower = header.toLowerCase();
  if (headerLower.includes('depend') || headerLower.includes('prerequisite')) {
    return /^(\d+([;,]\d+)*|none|null|0)$/i.test(value.trim());
  }
  return /^-?(?:\d+(?:\.\d*)?|\.\d+)$/.test(value.trim());
};

const validateAllCells = () => {
  cellErrors.value = {};
  headers.value.forEach((header, colIndex) => {
    columnData.value[colIndex]?.forEach((value, rowIndex) => {
      if (colIndex > 0 && (!value || value.trim() === '')) {
        columnData.value[colIndex][rowIndex] = '0';
        value = '0';
      }
      if (!validateCell(value, header, colIndex)) {
        cellErrors.value[`${rowIndex}-${header}`] = true;
      }
    });
  });
};

const handleCellInput = (rowIndex, colIndex, value) => {
  const header = headers.value[colIndex];
  let stringValue = String(value);
  const key = `${rowIndex}-${header}`;
  if (colIndex > 0 && (!stringValue || stringValue.trim() === '')) stringValue = '0';
  if (!validateCell(stringValue, header, colIndex)) cellErrors.value[key] = true;
  else delete cellErrors.value[key];
  if (colIndex >= 0 && columnData.value[colIndex]) columnData.value[colIndex][rowIndex] = stringValue;
};

const validateAndUpdateCell = (rowIndex, colIndex, value) => {
  const header = headers.value[colIndex];
  const key = `${rowIndex}-${header}`;
  let stringValue = String(value);
  if (!stringValue || stringValue.trim() === '') stringValue = colIndex === 0 ? '' : '0';
  if (!validateCell(stringValue, header, colIndex)) cellErrors.value[key] = true;
  else delete cellErrors.value[key];
  if (columnData.value[colIndex]) {
    columnData.value[colIndex][rowIndex] = stringValue;
    emit('data-updated', getTableData());
  }
};

const addRow = () => {
  headers.value.forEach((_, colIndex) => {
    if (!columnData.value[colIndex]) columnData.value[colIndex] = [];
    columnData.value[colIndex].push(colIndex === 0 ? '' : '0');
  });
  validateAllCells();
  emit('data-updated', getTableData());
  showToastMessage('Row added successfully');
};

const addColumn = () => {
  const newHeader = `Column${headers.value.length + 1}`;
  headers.value.push(newHeader);
  const isFirst = headers.value.length === 1;
  columnData.value.push(Array(columnData.value[0]?.length || 0).fill(isFirst ? '' : '0'));
  validateAllCells();
  emit('data-updated', getTableData());
  showToastMessage('Column added successfully');
};

const removeRow = (index) => { pendingDeleteRowIndex.value = index; showDeleteRowModal.value = true; };
const removeColumn = (index) => { pendingDeleteColumnIndex.value = index; showDeleteColumnModal.value = true; };

const confirmDeleteRow = () => {
  if (pendingDeleteRowIndex.value !== null) {
    headers.value.forEach((_, colIndex) => { columnData.value[colIndex].splice(pendingDeleteRowIndex.value, 1); });
    validateAllCells();
    emit('data-updated', getTableData());
    showToastMessage('Row deleted successfully');
  }
  showDeleteRowModal.value = false;
  pendingDeleteRowIndex.value = null;
};

const confirmDeleteColumn = () => {
  if (pendingDeleteColumnIndex.value !== null) {
    headers.value.splice(pendingDeleteColumnIndex.value, 1);
    columnData.value.splice(pendingDeleteColumnIndex.value, 1);
    validateAllCells();
    emit('data-updated', getTableData());
    showToastMessage('Column deleted successfully');
  }
  showDeleteColumnModal.value = false;
  pendingDeleteColumnIndex.value = null;
};

const updateHeader = (index, newHeader) => {
  const oldHeader = headers.value[index];
  if (typeof newHeader !== 'string') { showToastMessage('Column header must be a string'); headers.value[index] = oldHeader; return; }
  const trimmed = newHeader.trim();
  if (trimmed !== '' && headers.value.some((h, i) => i !== index && h.toLowerCase() === trimmed.toLowerCase())) {
    showToastMessage('Column header already exists');
    headers.value[index] = oldHeader;
    return;
  }
  if (oldHeader !== trimmed) {
    headers.value[index] = trimmed;
    validateAllCells();
    emit('data-updated', getTableData());
  }
};

const importJson = () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';
  input.onchange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          if (Array.isArray(data) && data.length > 0) {
            headers.value = Object.keys(data[0]);
            columnData.value = headers.value.map(header => data.map(row => String(row[header] || '')));
            jsonError.value = false;
            validateAllCells();
            emit('data-updated', getTableData());
            showToastMessage('JSON imported successfully');
          }
        } catch { jsonError.value = true; showToastMessage('Error parsing JSON file'); }
      };
      reader.readAsText(file);
    }
  };
  input.click();
};

const importCsv = () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.csv';
  input.onchange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const csv = e.target.result;
          const lines = csv.split('\n').filter(line => line.trim() !== '');
          if (lines.length > 1) {
            const headersRow = lines[0].split(',').map(h => h.trim());
            const dataRows = lines.slice(1);
            headers.value = headersRow;
            columnData.value = headersRow.map((_, colIndex) => dataRows.map(row => { const vals = row.split(',').map(v => v.trim()); return vals[colIndex] || ''; }));
            validateAllCells();
            emit('data-updated', getTableData());
            showToastMessage('CSV imported successfully');
          }
        } catch { showToastMessage('Error parsing CSV file'); }
      };
      reader.readAsText(file);
    }
  };
  input.click();
};

const exportJson = () => {
  if (!isTableValid.value) { showToastMessage('Please fix validation errors before exporting'); return; }
  const dataStr = JSON.stringify(getTableData(), null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'table-data.json';
  link.click();
  URL.revokeObjectURL(link.href);
  showToastMessage('JSON exported successfully');
};

const exportCsv = () => {
  if (!isTableValid.value) { showToastMessage('Please fix validation errors before exporting'); return; }
  if (headers.value.length === 0 || (columnData.value[0]?.length || 0) === 0) return;
  const tableData = getTableData();
  const csvContent = [headers.value.join(','), ...tableData.map(row => headers.value.map(h => row[h] || '').join(','))].join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'table-data.csv';
  link.click();
  URL.revokeObjectURL(link.href);
  showToastMessage('CSV exported successfully');
};

const updateFromJson = () => {
  if (!jsonInput.value.trim()) { jsonError.value = false; return; }
  try {
    const data = JSON.parse(jsonInput.value);
    if (Array.isArray(data) && data.length > 0) {
      headers.value = Object.keys(data[0]);
      columnData.value = headers.value.map(header => data.map(row => String(row[header] || '')));
      jsonError.value = false;
      validateAllCells();
      emit('data-updated', getTableData());
    } else jsonError.value = true;
  } catch { jsonError.value = true; }
};

const loadSampleData = () => {
  headers.value = Object.keys(defaultDataset[0]);
  columnData.value = headers.value.map(header => defaultDataset.map(row => String(row[header] || '')));
  validateAllCells();
  emit('data-updated', getTableData());
  showToastMessage('Loaded default dataset');
};

const toggleJsonEditor = () => {
  showJsonEditor.value = !showJsonEditor.value;
  if (showJsonEditor.value) { jsonInput.value = JSON.stringify(getTableData(), null, 2); jsonError.value = false; }
};

const openSimulationModal = () => {
  if (isTableValid.value) showSimulationModal.value = true;
  else showToastMessage('Please fix all validation errors before running simulation');
};

const closeSimulationModal = () => { showSimulationModal.value = false; selectedAlgorithms.value = []; };

const runSimulation = () => {
  if (selectedAlgorithms.value.length === 0) { showToastMessage('Please select at least one algorithm'); return; }
  emit('run-simulation', { tasks: getTableData(), algorithms: selectedAlgorithms.value });
  closeSimulationModal();
  showToastMessage('Simulation started');
};

const scrollToSimulationButton = () => {
  if (simulationButton.value) simulationButton.value.scrollIntoView({ behavior: 'smooth', block: 'center' });
};

const initializeData = () => {
  if (props.initialData && props.initialData.length > 0) {
    headers.value = Object.keys(props.initialData[0]);
    columnData.value = headers.value.map(header => props.initialData.map(row => String(row[header] || '')));
  } else {
    const defaultData = defaultDataset.slice(0, 5);
    headers.value = Object.keys(defaultData[0]);
    columnData.value = headers.value.map(header => defaultData.map(row => row[header] || ''));
  }
  validateAllCells();
};

watch(columnData, () => { jsonInput.value = JSON.stringify(getTableData(), null, 2); }, { deep: true });

onMounted(() => {
  if (simulationButton.value) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => { showFloatingButton.value = !entry.isIntersecting; });
    }, { threshold: 0.1 });
    observer.observe(simulationButton.value);
  }
});

initializeData();
jsonInput.value = JSON.stringify(getTableData(), null, 2);
</script>
