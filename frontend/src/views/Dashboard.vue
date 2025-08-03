<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-bold text-gray-900">Kanban Dashboard</h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <!-- Notifications -->
            <div class="relative">
              <button 
                @click="showNotifications = !showNotifications"
                class="relative p-2 text-gray-400 hover:text-gray-500"
              >
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
                </svg>
                <span v-if="stats.overdue_cards > 0" class="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                  {{ stats.overdue_cards }}
                </span>
              </button>
              
              <!-- Notifications dropdown -->
              <div v-if="showNotifications" class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border z-50">
                <div class="p-4 border-b">
                  <h3 class="text-lg font-medium text-gray-900">Notifications</h3>
                </div>
                <div class="max-h-96 overflow-y-auto">
                  <div v-if="stats.overdue_cards > 0" class="p-4 border-b bg-red-50">
                    <div class="flex">
                      <svg class="h-5 w-5 text-red-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                      </svg>
                      <div class="ml-3">
                        <p class="text-sm font-medium text-red-800">
                          {{ stats.overdue_cards }} overdue tasks
                        </p>
                        <p class="text-sm text-red-600">
                          You have tasks that are past their due date
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div v-if="stats.due_soon_cards > 0" class="p-4 border-b bg-yellow-50">
                    <div class="flex">
                      <svg class="h-5 w-5 text-yellow-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
                      </svg>
                      <div class="ml-3">
                        <p class="text-sm font-medium text-yellow-800">
                          {{ stats.due_soon_cards }} tasks due soon
                        </p>
                        <p class="text-sm text-yellow-600">
                          Tasks due within the next 3 days
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div v-if="recentActivities.length === 0" class="p-4 text-center text-gray-500">
                    No recent activity
                  </div>
                  
                  <div v-for="activity in recentActivities.slice(0, 5)" :key="activity.id" class="p-4 border-b hover:bg-gray-50">
                    <div class="flex items-start">
                      <img 
                        :src="activity.user.profile?.avatar || `https://ui-avatars.com/api/?name=${activity.user.username}&background=3B82F6&color=fff`"
                        :alt="activity.user.username"
                        class="h-8 w-8 rounded-full"
                      />
                      <div class="ml-3 flex-1">
                        <p class="text-sm text-gray-900">
                          <span class="font-medium">{{ activity.user.username }}</span>
                          {{ activity.description }}
                        </p>
                        <p class="text-xs text-gray-500">{{ formatDate(activity.created_at) }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Profile dropdown -->
            <div class="relative">
              <button 
                @click="showProfileMenu = !showProfileMenu"
                class="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <img 
                  :src="authStore.userAvatar"
                  :alt="authStore.user?.username"
                  class="h-8 w-8 rounded-full"
                />
                <span class="ml-2 text-gray-700">{{ authStore.userFullName }}</span>
              </button>
              
              <!-- Profile dropdown menu -->
              <div v-if="showProfileMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border z-50">
                <router-link 
                  to="/profile" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Your Profile
                </router-link>
                <router-link 
                  to="/settings" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Settings
                </router-link>
                <button 
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Sign out
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Stats cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Boards</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.total_boards }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Tasks</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.total_cards }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Completed</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.completed_cards }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Completion Rate</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.completion_rate }}%</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick actions -->
      <div class="bg-white shadow rounded-lg mb-8">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Quick Actions</h3>
          <div class="flex flex-wrap gap-4">
            <router-link 
              to="/boards/new"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              New Board
            </router-link>
            
            <router-link 
              to="/timeline"
              class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              Timeline View
            </router-link>
            
            <router-link 
              to="/labels"
              class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
              </svg>
              Manage Labels
            </router-link>
          </div>
        </div>
      </div>

      <!-- Recent boards and activity -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Recent boards -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Recent Boards</h3>
            <div class="space-y-4">
              <router-link 
                v-for="board in kanbanStore.boards.slice(0, 5)" 
                :key="board.id"
                :to="`/board/${board.id}`"
                class="block p-4 border rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <h4 class="text-sm font-medium text-gray-900">{{ board.title }}</h4>
                    <p class="text-sm text-gray-500 mt-1">{{ board.description || 'No description' }}</p>
                    <div class="flex items-center mt-2 text-xs text-gray-400">
                      <span>{{ board.lists_count || 0 }} lists</span>
                      <span class="mx-2">•</span>
                      <span>{{ board.cards_count || 0 }} cards</span>
                      <span class="mx-2">•</span>
                      <span>{{ formatDate(board.updated_at) }}</span>
                    </div>
                  </div>
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                  </svg>
                </div>
              </router-link>
              
              <div v-if="kanbanStore.boards.length === 0" class="text-center py-4 text-gray-500">
                No boards yet. Create your first board to get started!
              </div>
            </div>
            
            <div v-if="kanbanStore.boards.length > 5" class="mt-4 text-center">
              <router-link 
                to="/boards"
                class="text-blue-600 hover:text-blue-500 text-sm font-medium"
              >
                View all boards →
              </router-link>
            </div>
          </div>
        </div>

        <!-- Recent activity -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Recent Activity</h3>
            <div class="space-y-4">
              <div v-for="activity in recentActivities.slice(0, 8)" :key="activity.id" class="flex items-start">
                <img 
                  :src="activity.user.profile?.avatar || `https://ui-avatars.com/api/?name=${activity.user.username}&background=3B82F6&color=fff`"
                  :alt="activity.user.username"
                  class="h-8 w-8 rounded-full mr-3"
                />
                <div class="flex-1">
                  <p class="text-sm text-gray-900">
                    <span class="font-medium">{{ activity.user.username }}</span>
                    {{ activity.description }}
                  </p>
                  <p class="text-xs text-gray-500">{{ formatDate(activity.created_at) }}</p>
                </div>
              </div>
              
              <div v-if="recentActivities.length === 0" class="text-center py-4 text-gray-500">
                No recent activity
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useKanbanStore } from '../stores/kanban'
import axios from 'axios'

export default {
  name: 'Dashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const kanbanStore = useKanbanStore()
    
    const showNotifications = ref(false)
    const showProfileMenu = ref(false)
    const stats = ref({
      total_boards: 0,
      total_cards: 0,
      completed_cards: 0,
      completion_rate: 0,
      due_soon_cards: 0,
      overdue_cards: 0
    })
    const recentActivities = ref([])
    
    const fetchDashboardStats = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/dashboard/')
        stats.value = response.data.stats
        recentActivities.value = response.data.recent_activities
      } catch (error) {
        console.error('Failed to fetch dashboard stats:', error)
      }
    }
    
    const handleLogout = async () => {
      await authStore.logout()
      router.push('/login')
    }
    
    const formatDate = (dateString) => {
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
    
    // Close dropdowns when clicking outside
    const handleClickOutside = (event) => {
      if (!event.target.closest('.relative')) {
        showNotifications.value = false
        showProfileMenu.value = false
      }
    }
    
    onMounted(() => {
      kanbanStore.fetchBoards()
      fetchDashboardStats()
      document.addEventListener('click', handleClickOutside)
    })
    
    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })
    
    return {
      authStore,
      kanbanStore,
      showNotifications,
      showProfileMenu,
      stats,
      recentActivities,
      handleLogout,
      formatDate
    }
  }
}
</script>