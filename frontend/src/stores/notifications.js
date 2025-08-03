import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    notifications: [],
    unreadCount: 0,
    loading: false,
    error: null,
    
    // Notification preferences
    preferences: {
      dueDateReminders: true,
      dailySummary: false,
      emailNotifications: true,
      browserNotifications: false,
      reminderTime: '09:00' // Default reminder time
    }
  }),

  getters: {
    unreadNotifications: (state) => {
      return state.notifications.filter(n => !n.is_read)
    },
    
    notificationsByType: (state) => {
      return state.notifications.reduce((groups, notification) => {
        const type = notification.type
        if (!groups[type]) groups[type] = []
        groups[type].push(notification)
        return groups
      }, {})
    },
    
    recentNotifications: (state) => {
      return state.notifications.slice(0, 10)
    }
  },

  actions: {
    async fetchNotifications() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`${API_BASE_URL}/notifications/`)
        this.notifications = response.data.results || response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch notifications'
        console.error('Error fetching notifications:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchUnreadCount() {
      try {
        const response = await axios.get(`${API_BASE_URL}/notifications/unread_count/`)
        this.unreadCount = response.data.unread_count
      } catch (error) {
        console.error('Error fetching unread count:', error)
      }
    },

    async markAsRead(notificationId) {
      try {
        await axios.post(`${API_BASE_URL}/notifications/${notificationId}/mark_read/`)
        
        // Update local state
        const notification = this.notifications.find(n => n.id === notificationId)
        if (notification) {
          notification.is_read = true
          this.unreadCount = Math.max(0, this.unreadCount - 1)
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to mark notification as read'
        console.error('Error marking notification as read:', error)
      }
    },

    async markAllAsRead() {
      try {
        await axios.post(`${API_BASE_URL}/notifications/mark_all_read/`)
        
        // Update local state
        this.notifications.forEach(notification => {
          notification.is_read = true
        })
        this.unreadCount = 0
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to mark all notifications as read'
        console.error('Error marking all notifications as read:', error)
      }
    },

    async requestBrowserPermission() {
      if ('Notification' in window) {
        const permission = await Notification.requestPermission()
        this.preferences.browserNotifications = permission === 'granted'
        return permission === 'granted'
      }
      return false
    },

    showBrowserNotification(title, options = {}) {
      if (this.preferences.browserNotifications && 'Notification' in window && Notification.permission === 'granted') {
        const notification = new Notification(title, {
          icon: '/favicon.ico',
          badge: '/favicon.ico',
          ...options
        })
        
        // Auto close after 5 seconds
        setTimeout(() => {
          notification.close()
        }, 5000)
        
        return notification
      }
    },

    async updatePreferences(preferences) {
      try {
        // Update local preferences
        this.preferences = { ...this.preferences, ...preferences }
        
        // Save to backend (user profile)
        await axios.patch(`${API_BASE_URL}/auth/update_profile/`, {
          due_date_reminders: this.preferences.dueDateReminders,
          daily_summary: this.preferences.dailySummary,
          email_notifications: this.preferences.emailNotifications
        })
        
        // Store browser preferences locally
        localStorage.setItem('notificationPreferences', JSON.stringify(this.preferences))
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update preferences'
        console.error('Error updating notification preferences:', error)
        throw error
      }
    },

    loadPreferences() {
      const stored = localStorage.getItem('notificationPreferences')
      if (stored) {
        this.preferences = { ...this.preferences, ...JSON.parse(stored) }
      }
    },

    // Helper methods for different notification types
    createDueDateNotification(card) {
      const title = 'Task Due Soon'
      const message = `"${card.title}" is due ${this.formatDueDate(card.due_date)}`
      
      this.showBrowserNotification(title, {
        body: message,
        tag: `due-${card.id}`,
        data: { type: 'due_soon', cardId: card.id }
      })
    },

    createOverdueNotification(card) {
      const title = 'Task Overdue'
      const message = `"${card.title}" is overdue!`
      
      this.showBrowserNotification(title, {
        body: message,
        tag: `overdue-${card.id}`,
        data: { type: 'overdue', cardId: card.id },
        requireInteraction: true // Don't auto-dismiss
      })
    },

    createGoalProgressNotification(goal) {
      const title = 'Goal Progress Update'
      const message = `"${goal.title}" is ${goal.progress_percentage}% complete`
      
      this.showBrowserNotification(title, {
        body: message,
        tag: `goal-${goal.id}`,
        data: { type: 'goal_progress', goalId: goal.id }
      })
    },

    scheduleReminderNotifications() {
      // Check for due soon tasks every hour
      setInterval(() => {
        this.checkDueSoonTasks()
      }, 60 * 60 * 1000) // 1 hour

      // Daily reminder at specified time
      this.scheduleDailyReminder()
    },

    async checkDueSoonTasks() {
      if (!this.preferences.dueDateReminders) return

      try {
        // Get cards that are due within 24 hours
        const response = await axios.get(`${API_BASE_URL}/cards/?due_date=due_soon`)
        const dueSoonCards = response.data.results || response.data

        dueSoonCards.forEach(card => {
          if (!card.completed) {
            this.createDueDateNotification(card)
          }
        })
      } catch (error) {
        console.error('Error checking due soon tasks:', error)
      }
    },

    scheduleDailyReminder() {
      const now = new Date()
      const [hours, minutes] = this.preferences.reminderTime.split(':')
      const reminderTime = new Date()
      reminderTime.setHours(parseInt(hours), parseInt(minutes), 0, 0)

      // If reminder time has passed today, set for tomorrow
      if (reminderTime <= now) {
        reminderTime.setDate(reminderTime.getDate() + 1)
      }

      const msUntilReminder = reminderTime.getTime() - now.getTime()

      setTimeout(() => {
        this.sendDailyReminder()
        // Schedule for next day
        this.scheduleDailyReminder()
      }, msUntilReminder)
    },

    async sendDailyReminder() {
      if (!this.preferences.dailySummary) return

      try {
        // Get user's daily stats
        const response = await axios.get(`${API_BASE_URL}/dashboard/`)
        const stats = response.data.stats

        const title = 'Daily Task Summary'
        const message = `You have ${stats.total_cards - stats.completed_cards} pending tasks. Keep going! 💪`

        this.showBrowserNotification(title, {
          body: message,
          tag: 'daily-summary',
          data: { type: 'daily_summary' }
        })
      } catch (error) {
        console.error('Error sending daily reminder:', error)
      }
    },

    formatDueDate(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diff = date.getTime() - now.getTime()
      const hours = Math.floor(diff / (1000 * 60 * 60))

      if (hours < 0) {
        return 'overdue'
      } else if (hours < 1) {
        const minutes = Math.floor(diff / (1000 * 60))
        return `in ${minutes} minutes`
      } else if (hours < 24) {
        return `in ${hours} hours`
      } else {
        const days = Math.floor(hours / 24)
        return `in ${days} days`
      }
    }
  }
})