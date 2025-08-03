<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
    <!-- Header -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mr-3">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">AI Assistant</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">Your productivity companion</p>
          </div>
        </div>
        
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Content -->
    <div class="p-4">
      <!-- Quick Actions -->
      <div class="grid grid-cols-2 gap-3 mb-6">
        <button
          @click="showTaskBreakdown = true"
          class="p-3 text-left border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <div class="flex items-center mb-2">
            <svg class="w-5 h-5 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
            </svg>
            <span class="font-medium text-gray-900 dark:text-white">Break Down Task</span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400">Split complex tasks into smaller ones</p>
        </button>

        <button
          @click="generateSchedule"
          class="p-3 text-left border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <div class="flex items-center mb-2">
            <svg class="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            <span class="font-medium text-gray-900 dark:text-white">Optimize Schedule</span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400">Get personalized schedule suggestions</p>
        </button>

        <button
          @click="generateSummary('week')"
          class="p-3 text-left border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <div class="flex items-center mb-2">
            <svg class="w-5 h-5 text-purple-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v4"/>
            </svg>
            <span class="font-medium text-gray-900 dark:text-white">Weekly Summary</span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400">AI-generated progress report</p>
        </button>

        <button
          @click="suggestPriorities"
          class="p-3 text-left border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <div class="flex items-center mb-2">
            <svg class="w-5 h-5 text-orange-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
            </svg>
            <span class="font-medium text-gray-900 dark:text-white">Priority Suggestions</span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400">Smart priority recommendations</p>
        </button>
      </div>

      <!-- AI Chat Interface -->
      <div class="border border-gray-200 dark:border-gray-600 rounded-lg">
        <div class="p-3 border-b border-gray-200 dark:border-gray-600">
          <h4 class="font-medium text-gray-900 dark:text-white">AI Chat</h4>
        </div>
        
        <!-- Chat Messages -->
        <div class="h-64 overflow-y-auto p-3 space-y-3">
          <div v-if="aiStore.chatHistory.length === 0" class="text-center text-gray-500 dark:text-gray-400 py-8">
            <svg class="w-8 h-8 mx-auto mb-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
            <p class="text-sm">Ask me anything about productivity!</p>
            <p class="text-xs mt-1">Try: "How can I break down this task?" or "What should I prioritize today?"</p>
          </div>
          
          <div 
            v-for="message in aiStore.chatHistory" 
            :key="message.id"
            class="flex"
            :class="message.type === 'user' ? 'justify-end' : 'justify-start'"
          >
            <div 
              class="max-w-xs px-3 py-2 rounded-lg text-sm"
              :class="message.type === 'user' 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'"
            >
              {{ message.content }}
            </div>
          </div>
          
          <!-- Typing indicator -->
          <div v-if="aiStore.isTyping" class="flex justify-start">
            <div class="bg-gray-100 dark:bg-gray-700 px-3 py-2 rounded-lg">
              <div class="flex space-x-1">
                <div class="w-1 h-1 bg-gray-500 rounded-full animate-bounce"></div>
                <div class="w-1 h-1 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-1 h-1 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Chat Input -->
        <div class="p-3 border-t border-gray-200 dark:border-gray-600">
          <form @submit.prevent="sendMessage" class="flex space-x-2">
            <input
              v-model="chatMessage"
              type="text"
              placeholder="Ask AI for help..."
              class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              :disabled="aiStore.isTyping"
            />
            <button
              type="submit"
              :disabled="!chatMessage.trim() || aiStore.isTyping"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
            </button>
          </form>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="aiStore.loading" class="mt-4 text-center">
        <div class="inline-flex items-center px-4 py-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          <svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="text-blue-600 text-sm">AI is thinking...</span>
        </div>
      </div>

      <!-- Error State -->
      <div v-if="aiStore.error" class="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
        <p class="text-red-700 dark:text-red-300 text-sm">{{ aiStore.error }}</p>
      </div>
    </div>

    <!-- Task Breakdown Modal -->
    <TaskBreakdownModal
      v-if="showTaskBreakdown"
      @close="showTaskBreakdown = false"
      @select-task="handleTaskBreakdown"
    />

    <!-- Suggestion Result Modal -->
    <SuggestionModal
      v-if="showSuggestion"
      :suggestion="currentSuggestion"
      @close="showSuggestion = false"
      @apply="applySuggestion"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAIStore } from '../stores/ai'
import TaskBreakdownModal from './TaskBreakdownModal.vue'
import SuggestionModal from './SuggestionModal.vue'

export default {
  name: 'AIAssistant',
  components: {
    TaskBreakdownModal,
    SuggestionModal
  },
  emits: ['close'],
  setup() {
    const aiStore = useAIStore()
    
    const chatMessage = ref('')
    const showTaskBreakdown = ref(false)
    const showSuggestion = ref(false)
    const currentSuggestion = ref(null)
    
    const sendMessage = async () => {
      if (!chatMessage.value.trim()) return
      
      const message = chatMessage.value
      chatMessage.value = ''
      
      await aiStore.sendChatMessage(message)
    }
    
    const handleTaskBreakdown = async (cardId) => {
      showTaskBreakdown.value = false
      
      try {
        const suggestion = await aiStore.suggestTaskBreakdown(cardId)
        currentSuggestion.value = suggestion
        showSuggestion.value = true
      } catch (error) {
        console.error('Task breakdown error:', error)
      }
    }
    
    const generateSchedule = async () => {
      try {
        const suggestion = await aiStore.suggestScheduleOptimization()
        currentSuggestion.value = suggestion
        showSuggestion.value = true
      } catch (error) {
        console.error('Schedule generation error:', error)
      }
    }
    
    const generateSummary = async (period) => {
      try {
        const suggestion = await aiStore.generateSummary(period)
        currentSuggestion.value = suggestion
        showSuggestion.value = true
      } catch (error) {
        console.error('Summary generation error:', error)
      }
    }
    
    const suggestPriorities = async () => {
      try {
        const suggestions = await aiStore.suggestPriorities()
        currentSuggestion.value = { suggestions }
        showSuggestion.value = true
      } catch (error) {
        console.error('Priority suggestion error:', error)
      }
    }
    
    const applySuggestion = async (suggestionId) => {
      try {
        await aiStore.applySuggestion(suggestionId)
        showSuggestion.value = false
      } catch (error) {
        console.error('Apply suggestion error:', error)
      }
    }
    
    onMounted(() => {
      aiStore.fetchSuggestions()
    })
    
    return {
      aiStore,
      chatMessage,
      showTaskBreakdown,
      showSuggestion,
      currentSuggestion,
      sendMessage,
      handleTaskBreakdown,
      generateSchedule,
      generateSummary,
      suggestPriorities,
      applySuggestion
    }
  }
}
</script>