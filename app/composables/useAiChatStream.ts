import { ref, type Ref } from 'vue'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  isStreaming?: boolean
}

interface StreamMessageOptions {
  message: string
  simulationResults?: SimulationResults
  swarmType?: string
  onChunk?: (chunk: string) => void
  onComplete?: (fullContent: string) => void
  onError?: (error: string) => void
}

interface SimulationResults {
  aco?: {
    bestMakespan?: string | number
    executionTime?: string | number
    loadBalanceIndex?: string | number
    computationTime?: string | number
    finalAssignment?: any[]
  }
  pso?: {
    bestMakespan?: string | number
    executionTime?: string | number
    loadBalanceIndex?: string | number
    computationTime?: string | number
    finalAssignment?: any[]
  }
}

export function useAiChatStream() {
  const chatHistory: Ref<ChatMessage[]> = ref([])
  const aiLoading: Ref<boolean> = ref(false)
  const aiError: Ref<string | null> = ref(null)
  const aiLanguage: Ref<string> = ref('English')
  const isStreaming: Ref<boolean> = ref(false)

  const sendMessage = async (userMessage: string, simulationResults: SimulationResults = {}, swarmType: string = 'both') => {
    if (!userMessage.trim()) return

    // Add user message to history
    chatHistory.value.push({ role: 'user', content: userMessage })
    
    // Add empty assistant message that will be populated via streaming
    const assistantMessageIndex = chatHistory.value.length
    chatHistory.value.push({ role: 'assistant', content: '', isStreaming: true })
    
    aiLoading.value = true
    aiError.value = null
    isStreaming.value = true

    try {
      // Create fetch request for streaming
      const response = await fetch('/api/chat-stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userMessage: userMessage || '',
          simulationResults: simulationResults || {},
          swarmType: swarmType || 'both',
          chatHistory: chatHistory.value.slice(0, -2) || [],
          language: aiLanguage.value || 'English'
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status} ${response.statusText}`)
      }

      if (!response.body) {
        throw new Error('No response body')
      }

      // Process streaming response
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      try {
        while (true) {
          const { value, done } = await reader.read()
          
          if (done) {
            // Ensure streaming state is cleaned up
            if (chatHistory.value[assistantMessageIndex]) {
              chatHistory.value[assistantMessageIndex].isStreaming = false
            }
            isStreaming.value = false
            console.log('Stream completed')
            break
          }

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop() || ''

          for (const line of lines) {
            if (line.trim() === '' || !line.startsWith('data: ')) continue
            
            try {
              const jsonStr = line.replace(/^data: /, '').trim()
              if (!jsonStr) continue
              
              const event = JSON.parse(jsonStr)
              
              switch (event.type) {
                case 'start':
                  console.log('Stream started:', event.data)
                  break
                  
                case 'chunk':
                  // Add chunk to the assistant message
                  if (chatHistory.value[assistantMessageIndex]) {
                    chatHistory.value[assistantMessageIndex].content += event.data
                  }
                  break
                  
                case 'done':
                  // Stream completed
                  if (chatHistory.value[assistantMessageIndex]) {
                    chatHistory.value[assistantMessageIndex].isStreaming = false
                  }
                  isStreaming.value = false
                  console.log('Stream completed')
                  return
                  
                case 'error':
                  throw new Error(event.data)
              }
            } catch (parseError) {
              console.error('Parse error:', parseError, 'for line:', line)
              // Continue processing instead of breaking
            }
          }
        }
      } catch (streamError) {
        console.error('Stream processing error:', streamError)
        throw streamError
      } finally {
        // Always ensure streaming state is reset
        if (chatHistory.value[assistantMessageIndex]) {
          chatHistory.value[assistantMessageIndex].isStreaming = false
        }
        isStreaming.value = false
      }

    } catch (error: any) {
      console.error('AI Chat Stream Error:', error)
      
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
      aiError.value = errorMessage
      
      // Update the assistant message with error
      if (chatHistory.value[assistantMessageIndex]) {
        chatHistory.value[assistantMessageIndex].content = `Sorry, an error occurred: ${errorMessage}`
        chatHistory.value[assistantMessageIndex].isStreaming = false
      }
      
    } finally {
      aiLoading.value = false
      isStreaming.value = false
    }
  }

  // Improved streaming function with better error handling
  const streamMessage = async (input: string, simulationResults: SimulationResults = {}, swarmType: string = 'both') => {
    if (!input.trim()) return ''

    // Add user message to history
    chatHistory.value.push({ role: 'user', content: input })
    
    // Add empty assistant message that will be populated via streaming
    const assistantMessageIndex = chatHistory.value.length
    chatHistory.value.push({ role: 'assistant', content: '', isStreaming: true })
    
    aiLoading.value = true
    aiError.value = null
    isStreaming.value = true

    try {
      const response = await fetch('/api/chat-stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userMessage: input,
          simulationResults,
          swarmType,
          chatHistory: chatHistory.value.slice(0, -2),
          language: aiLanguage.value
        })
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`HTTP ${response.status}: ${errorText}`)
      }

      if (!response.body) {
        throw new Error('No response body')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let fullContent = ''

      while (true) {
        const { value, done } = await reader.read()
        
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.trim() === '' || !line.startsWith('data: ')) continue
          
          try {
            const jsonStr = line.replace(/^data: /, '').trim()
            if (!jsonStr) continue
            
            const event = JSON.parse(jsonStr)
            
            switch (event.type) {
              case 'start':
                console.log('Stream started')
                break
                
              case 'chunk':
                const chunk = event.data || ''
                fullContent += chunk
                
                // Update the assistant message
                if (chatHistory.value[assistantMessageIndex]) {
                  chatHistory.value[assistantMessageIndex].content = fullContent
                }
                
                // Auto-scroll saat streaming update - trigger multiple times for long messages
                if (typeof window !== 'undefined') {
                  setTimeout(() => {
                    const event = new CustomEvent('chat-scroll');
                    window.dispatchEvent(event);
                  }, 50);
                  
                  // Scroll lagi setelah sedikit delay untuk memastikan pesan panjang ter-scroll
                  setTimeout(() => {
                    const event = new CustomEvent('chat-scroll');
                    window.dispatchEvent(event);
                  }, 200);
                }
                break
                
              case 'done':
                // Stream completed
                if (chatHistory.value[assistantMessageIndex]) {
                  chatHistory.value[assistantMessageIndex].isStreaming = false
                }
                isStreaming.value = false
                return fullContent
                
              case 'error':
                throw new Error(event.data)
            }
          } catch (parseError) {
            console.warn('Parse error:', parseError, 'for line:', line)
            // Continue processing instead of failing completely
          }
        }
      }

      // Ensure streaming state is cleaned up
      if (chatHistory.value[assistantMessageIndex]) {
        chatHistory.value[assistantMessageIndex].isStreaming = false
      }
      
      return fullContent

    } catch (error: any) {
      console.error('Stream Message Error:', error)
      
      const errorMessage = error instanceof Error ? error.message : 'Unknown streaming error'
      aiError.value = errorMessage
      
      // Update the assistant message with error
      if (chatHistory.value[assistantMessageIndex]) {
        chatHistory.value[assistantMessageIndex].content = `Error: ${errorMessage}`
        chatHistory.value[assistantMessageIndex].isStreaming = false
      }
      
      throw error
    } finally {
      aiLoading.value = false
      isStreaming.value = false
    }
  }

  const clearChat = () => {
    chatHistory.value = []
    aiError.value = null
    aiLoading.value = false
    isStreaming.value = false
  }

  // Function to test streaming connection
  const testStreamConnection = async (): Promise<{ success: boolean; message: string }> => {
    try {
      const result = await streamMessage('Hello, test streaming connection', {}, 'both')
      return { 
        success: true, 
        message: 'Streaming connection works! Response: ' + (result.substring(0, 100) + (result.length > 100 ? '...' : ''))
      }
    } catch (error: any) {
      return { 
        success: false, 
        message: `Streaming test failed: ${error.message || 'Unknown error'}` 
      }
    }
  }

  // Alternative method for non-streaming fallback
  const sendMessageFallback = async (userMessage: string, simulationResults: SimulationResults = {}, swarmType: string = 'both') => {
    if (!userMessage.trim()) return

    // Add user message to history
    chatHistory.value.push({ role: 'user', content: userMessage })
    
    aiLoading.value = true
    aiError.value = null

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userMessage,
          simulationResults,
          swarmType,
          chatHistory: chatHistory.value.slice(0, -1),
          language: aiLanguage.value
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`)
      }

      const data = await response.json()
      
      // Add assistant response to history
      chatHistory.value.push({ role: 'assistant', content: data.response })

    } catch (error: any) {
      console.error('AI Chat Fallback Error:', error)
      aiError.value = error.message
      
      // Add error message to chat
      chatHistory.value.push({ 
        role: 'assistant', 
        content: `Error: ${error.message}` 
      })
    } finally {
      aiLoading.value = false
    }
  }

  return {
    chatHistory,
    aiLoading,
    aiError,
    aiLanguage,
    isStreaming,
    sendMessage,
    clearChat,
    testStreamConnection,
    streamMessage,
    sendMessageFallback
  }
}