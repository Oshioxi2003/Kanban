import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export const usePomodoroStore = defineStore('pomodoro', {
  state: () => ({
    currentSession: null,
    isActive: false,
    timeRemaining: 0,
    sessionType: 'work', // 'work', 'short_break', 'long_break'
    cycleCount: 0,
    
    // Session durations in minutes
    durations: {
      work: 25,
      short_break: 5,
      long_break: 15
    },
    
    // Settings
    settings: {
      autoStartBreaks: true,
      autoStartWork: false,
      longBreakInterval: 4, // After every 4 work sessions
      notifications: true,
      sounds: true
    },
    
    // Statistics
    todayStats: {
      total_sessions: 0,
      work_sessions: 0,
      total_minutes: 0
    },
    
    weekStats: {
      total_sessions: 0,
      work_sessions: 0,
      total_minutes: 0
    },
    
    // State
    loading: false,
    error: null
  }),

  getters: {
    isWorkSession: (state) => state.sessionType === 'work',
    isBreakSession: (state) => state.sessionType !== 'work',
    
    currentDuration: (state) => state.durations[state.sessionType],
    
    progressPercentage: (state) => {
      const totalTime = state.durations[state.sessionType] * 60 // Convert to seconds
      return ((totalTime - state.timeRemaining) / totalTime) * 100
    },
    
    formattedTime: (state) => {
      const minutes = Math.floor(state.timeRemaining / 60)
      const seconds = state.timeRemaining % 60
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
    },
    
    nextSessionType: (state) => {
      if (state.sessionType === 'work') {
        return (state.cycleCount + 1) % state.settings.longBreakInterval === 0 
          ? 'long_break' 
          : 'short_break'
      } else {
        return 'work'
      }
    }
  },

  actions: {
    async startSession(cardId = null, customDuration = null) {
      try {
        const duration = customDuration || this.durations[this.sessionType]
        
        const response = await axios.post(`${API_BASE_URL}/pomodoro/`, {
          card: cardId,
          session_type: this.sessionType,
          duration_minutes: duration
        })
        
        this.currentSession = response.data
        this.timeRemaining = duration * 60 // Convert to seconds
        this.isActive = true
        
        this.startTimer()
        
        if (this.settings.notifications) {
          this.showNotification(`${this.sessionType.replace('_', ' ')} session started!`, {
            body: `${duration} minutes of focused ${this.sessionType === 'work' ? 'work' : 'break'} time.`
          })
        }
        
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to start Pomodoro session'
        console.error('Pomodoro start error:', error)
      }
    },

    pauseSession() {
      this.isActive = false
      this.stopTimer()
    },

    resumeSession() {
      this.isActive = true
      this.startTimer()
    },

    async completeSession() {
      if (this.currentSession) {
        try {
          await axios.post(`${API_BASE_URL}/pomodoro/${this.currentSession.id}/complete_session/`)
          
          // Update cycle count
          if (this.sessionType === 'work') {
            this.cycleCount++
          }
          
          // Show completion notification
          if (this.settings.notifications) {
            this.showNotification('Session completed! 🎉', {
              body: `Great job on your ${this.sessionType.replace('_', ' ')} session!`,
              requireInteraction: true
            })
          }
          
          // Auto-start next session if enabled
          const nextType = this.nextSessionType
          if (
            (nextType !== 'work' && this.settings.autoStartBreaks) ||
            (nextType === 'work' && this.settings.autoStartWork)
          ) {
            this.sessionType = nextType
            setTimeout(() => {
              this.startSession()
            }, 2000)
          } else {
            this.sessionType = nextType
            this.isActive = false
          }
          
          // Refresh statistics
          this.fetchStats()
          
        } catch (error) {
          this.error = error.response?.data?.error || 'Failed to complete session'
          console.error('Pomodoro complete error:', error)
        }
      }
      
      this.currentSession = null
      this.timeRemaining = 0
      this.stopTimer()
    },

    stopSession() {
      this.isActive = false
      this.currentSession = null
      this.timeRemaining = 0
      this.stopTimer()
    },

    setSessionType(type) {
      if (!this.isActive) {
        this.sessionType = type
        this.timeRemaining = this.durations[type] * 60
      }
    },

    updateSettings(newSettings) {
      this.settings = { ...this.settings, ...newSettings }
      localStorage.setItem('pomodoroSettings', JSON.stringify(this.settings))
    },

    loadSettings() {
      const saved = localStorage.getItem('pomodoroSettings')
      if (saved) {
        this.settings = { ...this.settings, ...JSON.parse(saved) }
      }
    },

    async fetchStats() {
      try {
        const response = await axios.get(`${API_BASE_URL}/pomodoro/get_stats/`)
        this.todayStats = response.data.today
        this.weekStats = response.data.this_week
      } catch (error) {
        console.error('Failed to fetch Pomodoro stats:', error)
      }
    },

    // Timer management
    startTimer() {
      this.timer = setInterval(() => {
        if (this.timeRemaining > 0) {
          this.timeRemaining--
        } else {
          this.completeSession()
        }
      }, 1000)
    },

    stopTimer() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
    },

    // Notification helper
    showNotification(title, options = {}) {
      if ('Notification' in window && Notification.permission === 'granted') {
        const notification = new Notification(title, {
          icon: '/favicon.ico',
          badge: '/favicon.ico',
          ...options
        })
        
        if (!options.requireInteraction) {
          setTimeout(() => {
            notification.close()
          }, 5000)
        }
        
        return notification
      }
    },

    // Request notification permission
    async requestNotificationPermission() {
      if ('Notification' in window) {
        const permission = await Notification.requestPermission()
        this.settings.notifications = permission === 'granted'
        this.updateSettings({ notifications: this.settings.notifications })
        return permission === 'granted'
      }
      return false
    }
  }
})