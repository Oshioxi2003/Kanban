<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
              <span class="text-xl font-bold text-gray-900">Timeline View</span>
            </router-link>
          </div>
          
          <div class="flex items-center space-x-4">
            <!-- Time filter -->
            <select 
              v-model="selectedPeriod"
              @change="fetchTimelineData"
              class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="7">Last 7 days</option>
              <option value="14">Last 14 days</option>
              <option value="30">Last 30 days</option>
            </select>
            
            <!-- View toggle -->
            <div class="flex bg-gray-100 rounded-md p-1">
              <button
                @click="viewMode = 'calendar'"
                :class="viewMode === 'calendar' ? 'bg-white shadow-sm' : ''"
                class="px-3 py-1 text-sm font-medium rounded-md transition-colors"
              >
                Calendar
              </button>
              <button
                @click="viewMode = 'list'"
                :class="viewMode === 'list' ? 'bg-white shadow-sm' : ''"
                class="px-3 py-1 text-sm font-medium rounded-md transition-colors"
              >
                List
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      
      <!-- Error state -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
        {{ error }}
      </div>
      
      <!-- Content -->
      <div v-else class="space-y-6">
        <!-- Due soon alerts -->
        <div v-if="dueSoonCards.length > 0 || overdueCards.length > 0" class="bg-white shadow rounded-lg p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Attention Required</h3>
          
          <!-- Overdue cards -->
          <div v-if="overdueCards.length > 0" class="mb-6">
            <div class="flex items-center mb-3">
              <svg class="h-5 w-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              <h4 class="text-sm font-medium text-red-800">Overdue ({{ overdueCards.length }})</h4>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              <TimelineCard 
                v-for="card in overdueCards" 
                :key="card.id"
                :card="card"
                type="overdue"
              />
            </div>
          </div>
          
          <!-- Due soon cards -->
          <div v-if="dueSoonCards.length > 0">
            <div class="flex items-center mb-3">
              <svg class="h-5 w-5 text-yellow-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
              <h4 class="text-sm font-medium text-yellow-800">Due Soon ({{ dueSoonCards.length }})</h4>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              <TimelineCard 
                v-for="card in dueSoonCards" 
                :key="card.id"
                :card="card"
                type="due-soon"
              />
            </div>
          </div>
        </div>

        <!-- Timeline view -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">
              Timeline - {{ selectedPeriod }} days
            </h3>
          </div>
          
          <!-- Calendar view -->
          <div v-if="viewMode === 'calendar'" class="p-6">
            <div class="grid grid-cols-7 gap-1 mb-4">
              <div v-for="day in weekDays" :key="day" class="p-2 text-center text-sm font-medium text-gray-500">
                {{ day }}
              </div>
            </div>
            
            <div class="grid grid-cols-7 gap-1">
              <div 
                v-for="date in calendarDates" 
                :key="date.dateStr"
                class="min-h-24 p-1 border border-gray-100 rounded"
                :class="date.isToday ? 'bg-blue-50 border-blue-200' : 'hover:bg-gray-50'"
              >
                <div class="text-sm font-medium text-gray-900 mb-1">
                  {{ date.day }}
                </div>
                <div class="space-y-1">
                  <div 
                    v-for="card in date.cards" 
                    :key="card.id"
                    class="text-xs p-1 rounded truncate"
                    :class="getCardClass(card)"
                    :title="card.title"
                  >
                    {{ card.title }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- List view -->
          <div v-else class="divide-y divide-gray-200">
            <div v-for="group in groupedCards" :key="group.date" class="p-6">
              <h4 class="text-sm font-medium text-gray-900 mb-3">{{ group.dateLabel }}</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                <TimelineCard 
                  v-for="card in group.cards" 
                  :key="card.id"
                  :card="card"
                />
              </div>
            </div>
            
            <div v-if="groupedCards.length === 0" class="p-6 text-center text-gray-500">
              No cards with due dates in the selected period.
            </div>
          </div>
        </div>

        <!-- Recent activity -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Recent Activity</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div v-for="activity in recentActivities" :key="activity.id" class="flex items-start">
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
import { ref, computed, onMounted } from 'vue'
import { useKanbanStore } from '../stores/kanban'
import TimelineCard from '../components/TimelineCard.vue'
import axios from 'axios'

export default {
  name: 'Timeline',
  components: {
    TimelineCard
  },
  setup() {
    const kanbanStore = useKanbanStore()
    const loading = ref(false)
    const error = ref(null)
    const selectedPeriod = ref(7)
    const viewMode = ref('calendar')
    
    const timelineData = ref({
      cards_timeline: [],
      recent_activities: [],
      period: { start: null, end: null }
    })
    
    const dueSoonCards = ref([])
    const overdueCards = ref([])
    
    const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    
    const recentActivities = computed(() => timelineData.value.recent_activities || [])
    
    const calendarDates = computed(() => {
      const dates = []
      const now = new Date()
      const startDate = new Date(now)
      startDate.setDate(now.getDate() - selectedPeriod.value)
      
      // Get start of week for calendar grid
      const calendarStart = new Date(startDate)
      calendarStart.setDate(startDate.getDate() - startDate.getDay())
      
      // Generate calendar grid
      for (let i = 0; i < 42; i++) { // 6 weeks
        const date = new Date(calendarStart)
        date.setDate(calendarStart.getDate() + i)
        
        const dateStr = date.toISOString().split('T')[0]
        const cards = timelineData.value.cards_timeline.filter(card => {
          if (!card.due_date) return false
          return card.due_date.split('T')[0] === dateStr
        })
        
        dates.push({
          date,
          dateStr,
          day: date.getDate(),
          isToday: dateStr === now.toISOString().split('T')[0],
          cards
        })
      }
      
      return dates
    })
    
    const groupedCards = computed(() => {
      const groups = {}
      
      timelineData.value.cards_timeline.forEach(card => {
        if (!card.due_date) return
        
        const date = new Date(card.due_date).toISOString().split('T')[0]
        if (!groups[date]) {
          groups[date] = {
            date,
            dateLabel: formatDateLabel(date),
            cards: []
          }
        }
        groups[date].cards.push(card)
      })
      
      return Object.values(groups).sort((a, b) => new Date(a.date) - new Date(b.date))
    })
    
    const fetchTimelineData = async () => {
      loading.value = true
      error.value = null
      
      try {
        // For now, we'll simulate the API call
        // In real implementation, this would call the backend API
        const boards = kanbanStore.boards
        if (boards.length > 0) {
          const board = boards[0] // Use first board for demo
          const response = await axios.get(`http://localhost:8000/api/boards/${board.id}/timeline/?days=${selectedPeriod.value}`)
          timelineData.value = response.data
        }
        
        // Fetch due soon and overdue cards
        const dueSoonResponse = await axios.get(`http://localhost:8000/api/boards/${board.id}/due_soon/`)
        dueSoonCards.value = dueSoonResponse.data.due_soon || []
        overdueCards.value = dueSoonResponse.data.overdue || []
        
      } catch (err) {
        error.value = 'Failed to load timeline data'
        console.error('Timeline fetch error:', err)
      } finally {
        loading.value = false
      }
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
    
    const formatDateLabel = (dateStr) => {
      const date = new Date(dateStr)
      const today = new Date()
      const yesterday = new Date(today)
      yesterday.setDate(today.getDate() - 1)
      const tomorrow = new Date(today)
      tomorrow.setDate(today.getDate() + 1)
      
      if (dateStr === today.toISOString().split('T')[0]) {
        return 'Today'
      } else if (dateStr === yesterday.toISOString().split('T')[0]) {
        return 'Yesterday'
      } else if (dateStr === tomorrow.toISOString().split('T')[0]) {
        return 'Tomorrow'
      } else {
        return date.toLocaleDateString()
      }
    }
    
    const getCardClass = (card) => {
      const now = new Date()
      const dueDate = new Date(card.due_date)
      
      if (card.completed) {
        return 'bg-green-100 text-green-800'
      } else if (dueDate < now) {
        return 'bg-red-100 text-red-800'
      } else if (dueDate - now < 24 * 60 * 60 * 1000) { // Due within 24 hours
        return 'bg-yellow-100 text-yellow-800'
      } else {
        return 'bg-blue-100 text-blue-800'
      }
    }
    
    onMounted(() => {
      kanbanStore.fetchBoards().then(() => {
        fetchTimelineData()
      })
    })
    
    return {
      loading,
      error,
      selectedPeriod,
      viewMode,
      weekDays,
      calendarDates,
      groupedCards,
      recentActivities,
      dueSoonCards,
      overdueCards,
      fetchTimelineData,
      formatDate,
      getCardClass
    }
  }
}
</script>