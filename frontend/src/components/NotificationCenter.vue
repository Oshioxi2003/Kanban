<template>
  <div class="relative">
    <!-- Notification bell button -->
    <button 
      @click="showNotifications = !showNotifications"
      class="relative p-2 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded-full"
    >
      <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
      </svg>
      
      <!-- Unread count badge -->
      <span 
        v-if="notificationsStore.unreadCount > 0" 
        class="absolute -top-1 -right-1 h-5 w-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center font-medium"
      >
        {{ notificationsStore.unreadCount > 99 ? '99+' : notificationsStore.unreadCount }}
      </span>
    </button>
    
    <!-- Notifications dropdown -->
    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div 
        v-if="showNotifications"
        class="absolute right-0 mt-2 w-96 bg-white rounded-lg shadow-lg border z-50 max-h-96 overflow-hidden"
      >
        <!-- Header -->
        <div class="p-4 border-b border-gray-200 flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900">Notifications</h3>
          <div class="flex items-center space-x-2">
            <button
              v-if="notificationsStore.unreadCount > 0"
              @click="markAllAsRead"
              class="text-sm text-blue-600 hover:text-blue-500"
            >
              Mark all read
            </button>
            <button
              @click="showSettings = !showSettings"
              class="p-1 text-gray-400 hover:text-gray-600 rounded"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Settings panel -->
        <div v-if="showSettings" class="p-4 border-b border-gray-200 bg-gray-50">
          <h4 class="text-sm font-medium text-gray-900 mb-3">Notification Settings</h4>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm text-gray-700">Due date reminders</label>
              <input
                v-model="localPreferences.dueDateReminders"
                @change="updatePreferences"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
            <div class="flex items-center justify-between">
              <label class="text-sm text-gray-700">Daily summary</label>
              <input
                v-model="localPreferences.dailySummary"
                @change="updatePreferences"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
            <div class="flex items-center justify-between">
              <label class="text-sm text-gray-700">Browser notifications</label>
              <input
                v-model="localPreferences.browserNotifications"
                @change="handleBrowserNotificationToggle"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
            <div v-if="localPreferences.dailySummary" class="flex items-center justify-between">
              <label class="text-sm text-gray-700">Reminder time</label>
              <input
                v-model="localPreferences.reminderTime"
                @change="updatePreferences"
                type="time"
                class="text-sm border border-gray-300 rounded px-2 py-1"
              />
            </div>
          </div>
        </div>
        
        <!-- Loading state -->
        <div v-if="notificationsStore.loading" class="p-4 text-center">
          <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto"></div>
        </div>
        
        <!-- Notifications list -->
        <div v-else-if="notificationsStore.notifications.length > 0" class="max-h-64 overflow-y-auto">
          <div 
            v-for="notification in notificationsStore.recentNotifications" 
            :key="notification.id"
            class="p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer"
            :class="{ 'bg-blue-50': !notification.is_read }"
            @click="handleNotificationClick(notification)"
          >
            <div class="flex items-start">
              <!-- Icon based on type -->
              <div class="flex-shrink-0 mr-3 mt-1">
                <div 
                  class="w-2 h-2 rounded-full"
                  :class="getNotificationIconClass(notification.type)"
                ></div>
              </div>
              
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900" :class="{ 'font-semibold': !notification.is_read }">
                  {{ notification.title }}
                </p>
                <p class="text-sm text-gray-600 mt-1">
                  {{ notification.message }}
                </p>
                <p class="text-xs text-gray-400 mt-1">
                  {{ formatTime(notification.created_at) }}
                </p>
              </div>
              
              <!-- Mark as read button -->
              <button
                v-if="!notification.is_read"
                @click.stop="markAsRead(notification.id)"
                class="ml-2 text-xs text-blue-600 hover:text-blue-500"
              >
                Mark read
              </button>
            </div>
          </div>
        </div>
        
        <!-- Empty state -->
        <div v-else class="p-8 text-center text-gray-500">
          <svg class="mx-auto h-8 w-8 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
          </svg>
          <p class="text-sm">No notifications yet</p>
        </div>
        
        <!-- View all link -->
        <div v-if="notificationsStore.notifications.length > 10" class="p-3 text-center border-t">
          <router-link 
            to="/notifications"
            class="text-sm text-blue-600 hover:text-blue-500"
            @click="showNotifications = false"
          >
            View all notifications
          </router-link>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationsStore } from '../stores/notifications'

export default {
  name: 'NotificationCenter',
  setup() {
    const router = useRouter()
    const notificationsStore = useNotificationsStore()
    
    const showNotifications = ref(false)
    const showSettings = ref(false)
    
    const localPreferences = reactive({
      dueDateReminders: true,
      dailySummary: false,
      browserNotifications: false,
      emailNotifications: true,
      reminderTime: '09:00'
    })
    
    const getNotificationIconClass = (type) => {
      const classes = {
        due_soon: 'bg-yellow-400',
        overdue: 'bg-red-400',
        assigned: 'bg-blue-400',
        mentioned: 'bg-purple-400',
        goal_progress: 'bg-green-400',
        daily_summary: 'bg-gray-400'
      }
      return classes[type] || 'bg-gray-400'
    }
    
    const formatTime = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffInMinutes = Math.floor((now - date) / (1000 * 60))
      
      if (diffInMinutes < 1) {
        return 'Just now'
      } else if (diffInMinutes < 60) {
        return `${diffInMinutes}m ago`
      } else if (diffInMinutes < 1440) {
        return `${Math.floor(diffInMinutes / 60)}h ago`
      } else {
        return date.toLocaleDateString()
      }
    }
    
    const markAsRead = async (notificationId) => {
      await notificationsStore.markAsRead(notificationId)
    }
    
    const markAllAsRead = async () => {
      await notificationsStore.markAllAsRead()
    }
    
    const handleNotificationClick = (notification) => {
      // Mark as read
      if (!notification.is_read) {
        markAsRead(notification.id)
      }
      
      // Navigate based on notification type
      if (notification.card) {
        router.push(`/board/${notification.card.list.board.id}`)
      } else if (notification.goal) {
        router.push('/goals')
      }
      
      showNotifications.value = false
    }
    
    const updatePreferences = async () => {
      try {
        await notificationsStore.updatePreferences(localPreferences)
      } catch (error) {
        console.error('Failed to update preferences:', error)
      }
    }
    
    const handleBrowserNotificationToggle = async () => {
      if (localPreferences.browserNotifications) {
        const granted = await notificationsStore.requestBrowserPermission()
        if (!granted) {
          localPreferences.browserNotifications = false
        }
      }
      updatePreferences()
    }
    
    // Close dropdown when clicking outside
    const handleClickOutside = (event) => {
      if (!event.target.closest('.relative')) {
        showNotifications.value = false
        showSettings.value = false
      }
    }
    
    // Sync local preferences with store
    watch(() => notificationsStore.preferences, (newPrefs) => {
      Object.assign(localPreferences, newPrefs)
    }, { deep: true })
    
    onMounted(() => {
      notificationsStore.loadPreferences()
      notificationsStore.fetchNotifications()
      notificationsStore.fetchUnreadCount()
      
      // Setup automatic updates
      const interval = setInterval(() => {
        notificationsStore.fetchUnreadCount()
      }, 30000) // Check every 30 seconds
      
      // Setup reminder notifications
      notificationsStore.scheduleReminderNotifications()
      
      document.addEventListener('click', handleClickOutside)
      
      // Cleanup interval on unmount
      onUnmounted(() => {
        clearInterval(interval)
        document.removeEventListener('click', handleClickOutside)
      })
    })
    
    return {
      notificationsStore,
      showNotifications,
      showSettings,
      localPreferences,
      getNotificationIconClass,
      formatTime,
      markAsRead,
      markAllAsRead,
      handleNotificationClick,
      updatePreferences,
      handleBrowserNotificationToggle
    }
  }
}
</script>