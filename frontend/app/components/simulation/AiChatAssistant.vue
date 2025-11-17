<template>
  <div>
    <!-- Floating Chat Button -->
    <button
      v-if="!isChatOpen"
      @click="openChat"
      class="fixed bottom-6 right-6 w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full shadow-2xl hover:shadow-3xl transition-all duration-300 flex items-center justify-center z-40 hover:scale-110"
    >
      <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
    </button>

    <!-- Chat Window -->
    <div
      v-if="isChatOpen"
      ref="chatWindow"
      class="fixed bg-white rounded-2xl shadow-2xl flex flex-col z-50 border border-gray-200"
      :style="{
        left: `${draggablePosition.x}px`,
        top: `${draggablePosition.y}px`,
        width: `${chatWindowSize.width}px`,
        height: `${chatWindowSize.height}px`,
        bottom: 'auto',
        right: 'auto'
      }"
    >
      <!-- Header -->
      <div 
        @mousedown="startDrag"
        @touchstart="startDrag"
        class="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-3 rounded-t-2xl cursor-move flex items-center justify-between"
      >
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z" />
            <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z" />
          </svg>
          <span class="font-semibold">AI Assistant</span>
          <span v-if="isStreaming" class="text-xs bg-white/20 px-2 py-0.5 rounded-full">Streaming...</span>
        </div>
        <div class="flex items-center gap-2">
          <button @click="clearChat" class="hover:bg-white/20 p-1 rounded transition" title="Clear chat">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
          <button @click="closeChat" class="hover:bg-white/20 p-1 rounded transition" title="Close">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div 
        ref="messagesContainer"
        class="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50"
      >
        <div v-if="chatHistory.length === 0" class="text-center text-gray-400 mt-8">
          <svg class="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <p class="text-sm">Ask me anything about your simulation results!</p>
          <p class="text-xs mt-2 text-gray-400">
            Language: <span class="font-semibold">{{ aiLanguage.toUpperCase() }}</span>
          </p>
        </div>

        <div
          v-for="(msg, idx) in chatHistory"
          :key="idx"
          class="flex"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-[85%] rounded-2xl px-4 py-2 shadow-sm"
            :class="[
              msg.role === 'user' 
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white' 
                : 'bg-white text-gray-800 border border-gray-200',
              isStreaming && idx === chatHistory.length - 1 && msg.role === 'assistant' ? 'streaming-message' : ''
            ]"
          >
            <div 
              v-if="msg.role === 'assistant'"
              class="markdown-content text-sm ai-message-content"
              v-html="renderMarkdown(msg.content)"
            />
            <div v-else class="text-sm whitespace-pre-wrap">{{ msg.content }}</div>
            
            <button
              v-if="msg.role === 'assistant' && msg.content"
              @click="copyToClipboard(msg.content)"
              class="mt-2 text-xs opacity-70 hover:opacity-100 transition flex items-center gap-1"
              :class="msg.role === 'user' ? 'text-white' : 'text-gray-600'"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Copy
            </button>
          </div>
        </div>

        <div v-if="aiLoading && !isStreaming" class="flex justify-start">
          <div class="bg-white text-gray-800 rounded-2xl px-4 py-2 shadow-sm border border-gray-200">
            <div class="flex items-center gap-2">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
              <span class="text-sm">Thinking...</span>
            </div>
          </div>
        </div>

        <div v-if="aiError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-lg text-sm">
          ⚠️ {{ aiError }}
        </div>
      </div>

      <!-- Input -->
      <div class="border-t border-gray-200 p-3 bg-white rounded-b-2xl">
        <form @submit.prevent="sendUserMessage" class="flex gap-2">
          <input
            v-model="localUserMessage"
            type="text"
            placeholder="Ask about simulation results..."
            class="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            :disabled="aiLoading"
          />
          <button
            type="submit"
            :disabled="aiLoading || (!localUserMessage.trim() && chatHistory.length > 0)"
            class="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </form>
      </div>

      <!-- Resize Handles -->
      <div
        @mousedown="(e) => startResize(e, 'bottom-right')"
        @touchstart="(e) => startResize(e, 'bottom-right')"
        class="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize"
        style="background: linear-gradient(135deg, transparent 50%, rgba(156, 163, 175, 0.5) 50%)"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import { marked } from 'marked';

const props = defineProps({
  chatHistory: { type: Array, required: true },
  aiLoading: { type: Boolean, required: true },
  aiError: { type: String, default: '' },
  aiLanguage: { type: String, required: true },
  isStreaming: { type: Boolean, required: true }
});

const emit = defineEmits(['send-message', 'clear-chat', 'copy-to-clipboard']);

const isChatOpen = ref(false);
const localUserMessage = ref('');
const draggablePosition = ref({ x: window.innerWidth - 520, y: 80 });
const isDragging = ref(false);
const dragStart = ref({ x: 0, y: 0 });
const chatWindow = ref(null);
const chatWindowSize = ref({ width: 480, height: 520 });
const isResizing = ref(false);
const resizeDirection = ref('corner');
const resizeStart = ref({ x: 0, y: 0, width: 0, height: 0 });
const messagesContainer = ref(null);

const openChat = () => isChatOpen.value = true;
const closeChat = () => isChatOpen.value = false;

const renderMarkdown = (text) => {
  const html = marked(text || '');
  return html.replace(/<table/g, '<div class="table-scroll-wrapper"><table')
             .replace(/<\/table>/g, '</table></div>');
};

const copyToClipboard = (text) => {
  emit('copy-to-clipboard', text);
};

const clearChat = () => {
  emit('clear-chat');
};

const sendUserMessage = () => {
  if (!localUserMessage.value.trim() && props.chatHistory.length === 0) {
    localUserMessage.value = "Explain these simulation results.";
  }
  if (!localUserMessage.value.trim()) return;

  emit('send-message', localUserMessage.value);
  localUserMessage.value = '';
};

const startDrag = (event) => {
  isDragging.value = true;
  const clientX = event.clientX || event.touches[0].clientX;
  const clientY = event.clientY || event.touches[0].clientY;
  dragStart.value = { 
    x: clientX - draggablePosition.value.x, 
    y: clientY - draggablePosition.value.y 
  };
  
  const handleMove = (e) => {
    if (!isDragging.value) return;
    const moveX = e.clientX || e.touches[0].clientX;
    const moveY = e.clientY || e.touches[0].clientY;
    draggablePosition.value = { 
      x: moveX - dragStart.value.x, 
      y: moveY - dragStart.value.y 
    };
  };
  
  const handleUp = () => {
    isDragging.value = false;
    document.removeEventListener('mousemove', handleMove);
    document.removeEventListener('mouseup', handleUp);
    document.removeEventListener('touchmove', handleMove);
    document.removeEventListener('touchend', handleUp);
  };
  
  document.addEventListener('mousemove', handleMove);
  document.addEventListener('mouseup', handleUp);
  document.addEventListener('touchmove', handleMove);
  document.addEventListener('touchend', handleUp);
};

const startResize = (event, direction = 'bottom-right') => {
  isResizing.value = true;
  resizeDirection.value = direction;
  const clientX = event.clientX || event.touches[0].clientX;
  const clientY = event.clientY || event.touches[0].clientY;
  resizeStart.value = { 
    x: clientX, 
    y: clientY, 
    width: chatWindowSize.value.width, 
    height: chatWindowSize.value.height,
    startPosX: draggablePosition.value.x,
    startPosY: draggablePosition.value.y
  };
  
  const handleMove = (e) => {
    if (!isResizing.value) return;
    const moveX = e.clientX || e.touches[0].clientX;
    const moveY = e.clientY || e.touches[0].clientY;
    const deltaX = moveX - resizeStart.value.x;
    const deltaY = moveY - resizeStart.value.y;
    
    const minWidth = 320;
    const minHeight = 400;
    const maxWidth = window.innerWidth * 0.9;
    const maxHeight = window.innerHeight * 0.9;
    
    const newWidth = Math.max(minWidth, Math.min(maxWidth, resizeStart.value.width + deltaX));
    const newHeight = Math.max(minHeight, Math.min(maxHeight, resizeStart.value.height + deltaY));
    
    chatWindowSize.value = { width: newWidth, height: newHeight };
  };
  
  const handleUp = () => {
    isResizing.value = false;
    resizeDirection.value = 'bottom-right';
    document.removeEventListener('mousemove', handleMove);
    document.removeEventListener('mouseup', handleUp);
    document.removeEventListener('touchmove', handleMove);
    document.removeEventListener('touchend', handleUp);
  };
  
  document.addEventListener('mousemove', handleMove);
  document.addEventListener('mouseup', handleUp);
  document.addEventListener('touchmove', handleMove);
  document.addEventListener('touchend', handleUp);
};

watch(() => props.chatHistory, () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
}, { deep: true });
</script>

<style scoped>
/* Streaming animation */
.streaming-message {
  position: relative;
}

.streaming-message::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
  animation: shimmer 2s infinite;
  border-radius: inherit;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Markdown Styling */
.markdown-content {
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  color: #1f2937;
}

.markdown-content h1 {
  font-size: 1.5rem;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

.markdown-content h2 {
  font-size: 1.25rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.25rem;
}

.markdown-content h3 {
  font-size: 1.125rem;
}

.markdown-content h4 {
  font-size: 1rem;
}

.markdown-content p {
  margin-bottom: 1rem;
  color: #374151;
}

.markdown-content ul,
.markdown-content ol {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.markdown-content li {
  margin-bottom: 0.25rem;
  color: #374151;
}

.markdown-content strong {
  font-weight: 600;
  color: #1f2937;
}

.markdown-content em {
  font-style: italic;
  color: #4b5563;
}

.markdown-content code {
  background-color: #f3f4f6;
  color: #dc2626;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.875rem;
}

.markdown-content pre {
  background-color: #1f2937;
  color: #f9fafb;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin-bottom: 1rem;
}

.markdown-content pre code {
  background: none;
  color: inherit;
  padding: 0;
  font-size: 0.875rem;
}

.markdown-content blockquote {
  border-left: 4px solid #3b82f6;
  padding-left: 1rem;
  margin: 1rem 0;
  background-color: #f8fafc;
  color: #475569;
  font-style: italic;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 0;
  font-size: 0.825rem;
  background: white;
  min-width: max-content;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid #e5e7eb;
  padding: 0.4rem 0.5rem;
  text-align: left;
  vertical-align: top;
  line-height: 1.3;
  white-space: nowrap;
}

.markdown-content th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #1f2937;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.markdown-content td {
  background-color: #ffffff;
  color: #374151;
  font-size: 0.8rem;
}

.markdown-content tr:nth-child(even) td {
  background-color: #f9fafb;
}

.markdown-content a {
  color: #3b82f6;
  text-decoration: underline;
}

.markdown-content a:hover {
  color: #2563eb;
}

.markdown-content hr {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 1.5rem 0;
}

.ai-message-content {
  max-width: none;
}

.ai-message-content .markdown-wrapper {
  max-width: 100%;
}

.ai-message-content .markdown-content > *:first-child {
  margin-top: 0;
}

.ai-message-content .markdown-content > *:last-child {
  margin-bottom: 0;
}

.table-scroll-wrapper {
  overflow-x: auto;
  margin: 1rem 0;
  border-radius: 0.375rem;
  border: 1px solid #e5e7eb;
  max-width: 100%;
}

.table-scroll-wrapper::-webkit-scrollbar {
  height: 6px;
}

.table-scroll-wrapper::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.table-scroll-wrapper::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.table-scroll-wrapper::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
