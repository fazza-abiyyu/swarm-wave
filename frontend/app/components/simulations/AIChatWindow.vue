<template>
  <div>
    <!-- Floating Chat Bubble -->
    <div v-if="!isOpen" @click="isOpen = true"
      class="fixed bottom-6 right-6 w-14 h-14 bg-blue-500 text-white rounded-full shadow-none hover:bg-blue-600 cursor-pointer flex items-center justify-center z-50 transition-all duration-200 hover:scale-110"
      title="Ask Swarm Wave AI">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
    </div>

    <!-- Chat Window -->
    <div v-if="isOpen" ref="chatWindow"
      class="fixed bottom-6 right-6 bg-white rounded-xl border border-gray-200 shadow-none z-50 flex flex-col transition-all duration-300"
      :style="{ transform: `translate(${position.x}px, ${position.y}px)`, width: `${size.width}px`, height: `${size.height}px`, minWidth: '320px', minHeight: '400px' }">
      
      <!-- Header -->
      <div class="flex items-center justify-between p-4 border-b border-gray-200 cursor-move" @mousedown="startDrag">
        <h3 class="text-lg font-semibold text-gray-900">Swarm Wave AI</h3>
        <div class="flex items-center space-x-2">
          <select v-model="aiLanguage" class="text-sm px-2 py-1 border border-gray-300 rounded-md focus:ring-1 focus:ring-blue-500 bg-white">
            <option value="English">EN</option>
            <option value="Indonesian">ID</option>
            <option value="Chinese">CN</option>
          </select>
          <button @click="isOpen = false" class="text-gray-500 hover:text-gray-700 p-1 rounded-md hover:bg-gray-100">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 bg-gray-50">
        <div v-if="chatHistory.length === 0" class="text-center text-gray-500 py-8">
          <svg class="w-12 h-12 mx-auto mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          <p class="text-sm">Ask me anything about your simulation results!</p>
        </div>
        <div v-else class="space-y-4">
          <div v-for="(message, index) in chatHistory" :key="index" :class="['flex', message.role === 'user' ? 'justify-end' : 'justify-start']">
            <div :class="['rounded-lg shadow-sm', message.role === 'user' ? 'bg-blue-500 text-white ml-8 px-4 py-3 max-w-[85%]' : 'bg-white border border-gray-200 text-gray-900 mr-4 max-w-[95%] overflow-hidden']">
              <div v-if="message.role === 'user'" class="text-sm font-medium">{{ message.content }}</div>
              <div v-else class="ai-message-content px-4 py-3">
                <div class="markdown-wrapper overflow-x-auto">
                  <div class="markdown-content text-sm leading-relaxed min-w-0" v-html="renderMarkdown(message.content)"></div>
                </div>
                <div v-if="message.isStreaming" class="flex items-center mt-3 text-xs text-gray-500">
                  <div class="flex space-x-1">
                    <div class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce"></div>
                    <div class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  </div>
                  <span class="ml-2">AI is typing...</span>
                </div>
                <div v-if="!message.isStreaming" class="mt-3 flex justify-end border-t border-gray-100 pt-2">
                  <button @click="copyToClipboard(message.content)" class="text-xs text-gray-500 hover:text-blue-600 flex items-center gap-1 px-2 py-1 rounded hover:bg-gray-50 transition-colors" title="Copy response">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    Copy
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div v-if="aiLoading && !isStreaming" class="flex justify-start">
            <div class="bg-white border border-gray-200 text-gray-900 px-3 py-2 rounded-lg">
              <div class="flex items-center space-x-1">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Error -->
      <div v-if="aiError" class="px-4 py-2 bg-red-50 border-t border-red-200">
        <div class="flex items-center">
          <svg class="w-4 h-4 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          <span class="text-xs text-red-600">{{ aiError }}</span>
        </div>
      </div>

      <!-- Input -->
      <div class="p-4 border-t border-gray-200 bg-white">
        <div class="flex gap-2">
          <textarea v-model="userMessage" @keydown.enter.prevent="handleSend" placeholder="Ask about your simulation..."
            class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:ring-1 focus:ring-blue-500 resize-none" rows="2" :disabled="aiLoading"></textarea>
          <div class="flex flex-col gap-1">
            <button @click="handleSend" :disabled="!userMessage.trim() || aiLoading"
              class="px-3 py-1 bg-blue-500 text-white text-sm rounded-md hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed">Send</button>
            <button @click="clearChat" class="px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded-md hover:bg-gray-300" title="Clear chat">Clear</button>
          </div>
        </div>
      </div>

      <!-- Resize Handle -->
      <div class="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize" @mousedown="startResize">
        <svg class="w-3 h-3 text-gray-400 absolute bottom-1 right-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7l10 10M17 7l-10 10" />
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import { marked } from 'marked';
import { useAiChatStream } from '~/composables/useAiChatStream';

const props = defineProps({
  simulationData: { type: Object, default: () => ({}) },
  selectedAlgorithms: { type: Array, default: () => [] }
});

const emit = defineEmits(['show-toast']);

const { chatHistory, aiLoading, aiError, aiLanguage, isStreaming, sendMessage, clearChat } = useAiChatStream();

const isOpen = ref(false);
const userMessage = ref('');
const position = ref({ x: 0, y: 0 });
const size = ref({ width: 480, height: 520 });
const chatWindow = ref(null);
const messagesContainer = ref(null);

const renderMarkdown = (text) => {
  const html = marked(text || '');
  return html.replace(/<table/g, '<div class="table-scroll-wrapper"><table').replace(/<\/table>/g, '</table></div>');
};

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => emit('show-toast', 'Copied to clipboard', 'success'));
};

const handleSend = async () => {
  if (!userMessage.value.trim() && chatHistory.value.length === 0) {
    userMessage.value = 'Explain these simulation results.';
  }
  if (!userMessage.value.trim()) return;
  await sendMessage(userMessage.value, props.simulationData, props.selectedAlgorithms.join('_'));
  userMessage.value = '';
};

const startDrag = (e) => {
  const startX = e.clientX - position.value.x;
  const startY = e.clientY - position.value.y;
  const onMove = (ev) => { position.value = { x: ev.clientX - startX, y: ev.clientY - startY }; };
  const onUp = () => { document.removeEventListener('mousemove', onMove); document.removeEventListener('mouseup', onUp); };
  document.addEventListener('mousemove', onMove);
  document.addEventListener('mouseup', onUp);
};

const startResize = (e) => {
  const startX = e.clientX;
  const startY = e.clientY;
  const startW = size.value.width;
  const startH = size.value.height;
  const onMove = (ev) => {
    size.value = { width: Math.max(320, startW + ev.clientX - startX), height: Math.max(400, startH + ev.clientY - startY) };
  };
  const onUp = () => { document.removeEventListener('mousemove', onMove); document.removeEventListener('mouseup', onUp); };
  document.addEventListener('mousemove', onMove);
  document.addEventListener('mouseup', onUp);
};

watch(chatHistory, () => { nextTick(() => { if (messagesContainer.value) messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight; }); }, { deep: true });
</script>

<style scoped>
.overflow-y-auto::-webkit-scrollbar { width: 6px; }
.overflow-y-auto::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 3px; }
.overflow-y-auto::-webkit-scrollbar-thumb { background: #c1c1c1; border-radius: 3px; }

.markdown-content { line-height: 1.6; }
.markdown-content h1, .markdown-content h2, .markdown-content h3 { font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem; color: #1f2937; }
.markdown-content p { margin-bottom: 0.75rem; color: #374151; }
.markdown-content ul, .markdown-content ol { margin-bottom: 0.75rem; padding-left: 1.5rem; }
.markdown-content li { margin-bottom: 0.25rem; color: #374151; }
.markdown-content strong { font-weight: 600; color: #1f2937; }
.markdown-content code { background-color: #f3f4f6; color: #dc2626; padding: 0.125rem 0.25rem; border-radius: 0.25rem; font-family: monospace; font-size: 0.875rem; }
.markdown-content pre { background-color: #1f2937; color: #f9fafb; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; margin-bottom: 0.75rem; }
.markdown-content pre code { background: none; color: inherit; padding: 0; }
.markdown-content table { width: 100%; border-collapse: collapse; font-size: 0.825rem; background: white; min-width: max-content; }
.markdown-content th, .markdown-content td { border: 1px solid #e5e7eb; padding: 0.4rem 0.5rem; text-align: left; white-space: nowrap; }
.markdown-content th { background-color: #f8fafc; font-weight: 600; color: #1f2937; font-size: 0.75rem; text-transform: uppercase; }
.table-scroll-wrapper { overflow-x: auto; margin: 0.75rem 0; border-radius: 0.375rem; border: 1px solid #e5e7eb; }
</style>
