import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export const useAIStore = defineStore('ai', {
  state: () => ({
    suggestions: [],
    currentSuggestion: null,
    loading: false,
    error: null,
    
    // AI Chat state
    chatHistory: [],
    isTyping: false
  }),

  getters: {
    getSuggestionsByType: (state) => (type) => {
      return state.suggestions.filter(s => s.type === type)
    },
    
    recentSuggestions: (state) => {
      return state.suggestions.slice(0, 5)
    },
    
    appliedSuggestions: (state) => {
      return state.suggestions.filter(s => s.is_applied)
    }
  },

  actions: {
    async suggestTaskBreakdown(cardId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/ai-assistant/suggest_task_breakdown/`, {
          card_id: cardId
        })
        
        this.currentSuggestion = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to get AI suggestions'
        console.error('AI suggestion error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async suggestScheduleOptimization() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/ai-assistant/suggest_schedule/`)
        
        this.currentSuggestion = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to get schedule suggestions'
        console.error('Schedule suggestion error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async generateSummary(period = 'week') {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/ai-assistant/generate_summary/`, {
          period
        })
        
        this.currentSuggestion = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to generate summary'
        console.error('Summary generation error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async suggestPriorities() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/ai-assistant/suggest_priorities/`)
        
        return response.data.suggestions
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to get priority suggestions'
        console.error('Priority suggestion error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchSuggestions() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`${API_BASE_URL}/ai-assistant/get_suggestions/`)
        this.suggestions = response.data.suggestions
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to fetch suggestions'
        console.error('Fetch suggestions error:', error)
      } finally {
        this.loading = false
      }
    },

    async applySuggestion(suggestionId) {
      try {
        await axios.post(`${API_BASE_URL}/ai-assistant/${suggestionId}/apply_suggestion/`)
        
        // Update local state
        const suggestion = this.suggestions.find(s => s.id === suggestionId)
        if (suggestion) {
          suggestion.is_applied = true
        }
        
        return true
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to apply suggestion'
        console.error('Apply suggestion error:', error)
        throw error
      }
    },

    // Simulated AI Chat functionality
    async sendChatMessage(message) {
      this.isTyping = true
      
      // Add user message
      this.chatHistory.push({
        id: Date.now(),
        type: 'user',
        content: message,
        timestamp: new Date()
      })
      
      // Simulate AI thinking time
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Generate AI response
      const aiResponse = this.generateAIResponse(message)
      
      this.chatHistory.push({
        id: Date.now() + 1,
        type: 'ai',
        content: aiResponse,
        timestamp: new Date()
      })
      
      this.isTyping = false
    },

    generateAIResponse(userMessage) {
      const message = userMessage.toLowerCase()
      
      // Smart response generation based on keywords
      if (message.includes('break') || message.includes('split') || message.includes('divide')) {
        return `I can help you break down tasks! Try using the "🔬 Break Down Task" button on any card to get AI-powered suggestions for splitting it into smaller, manageable subtasks.`
      }
      
      if (message.includes('schedule') || message.includes('plan') || message.includes('time')) {
        return `For schedule optimization, I analyze your tasks and productivity patterns. I can suggest optimal time slots for different types of work, recommend breaks, and help you prioritize your day.`
      }
      
      if (message.includes('priority') || message.includes('urgent') || message.includes('important')) {
        return `I can analyze your tasks and suggest priority adjustments based on due dates, dependencies, and your goals. Would you like me to review your current task priorities?`
      }
      
      if (message.includes('summary') || message.includes('report') || message.includes('progress')) {
        return `I can generate natural language summaries of your work! I'll analyze your completed tasks, productivity patterns, and provide insights with encouraging feedback. Try the weekly or monthly summary features.`
      }
      
      if (message.includes('pomodoro') || message.includes('focus') || message.includes('productivity')) {
        return `The Pomodoro Technique is great for focus! I recommend 25-minute work sessions with 5-minute breaks. You can start a Pomodoro timer directly from any task card.`
      }
      
      if (message.includes('goal') || message.includes('objective')) {
        return `Goals help you stay focused on what matters most. I can help you break down large goals into smaller tasks and track your progress automatically.`
      }
      
      // Default responses
      const defaultResponses = [
        `I'm here to help optimize your productivity! I can break down tasks, suggest schedules, generate summaries, and provide insights about your work patterns.`,
        `Great question! I analyze your tasks and productivity data to provide personalized suggestions. What specific area would you like help with?`,
        `I'm designed to make your task management smarter. I can help with task breakdown, priority suggestions, schedule optimization, and progress summaries.`,
        `Think of me as your productivity coach! I learn from your work patterns and provide actionable insights to help you work more efficiently.`
      ]
      
      return defaultResponses[Math.floor(Math.random() * defaultResponses.length)]
    },

    clearChat() {
      this.chatHistory = []
    }
  }
})