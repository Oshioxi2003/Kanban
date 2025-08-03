<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
              <span class="text-xl font-bold text-gray-900 dark:text-white">Eisenhower Matrix</span>
            </router-link>
          </div>
          
          <div class="flex items-center">
            <button 
              @click="refreshMatrix"
              :disabled="loading"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center disabled:opacity-50"
            >
              <svg class="w-4 h-4 mr-2" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              Refresh
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Introduction -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Priority Management with Eisenhower Matrix</h2>
        <p class="text-gray-600 dark:text-gray-300 mb-4">
          Organize your tasks based on urgency and importance to maximize productivity and focus on what truly matters.
        </p>
        
        <!-- Legend -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-red-500 rounded mr-2"></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">Urgent & Important</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-blue-500 rounded mr-2"></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">Important, Not Urgent</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-yellow-500 rounded mr-2"></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">Urgent, Not Important</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-gray-500 rounded mr-2"></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">Neither Urgent nor Important</span>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <!-- Matrix Grid -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Quadrant 1: Urgent & Important (Do First) -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow border-l-4 border-red-500">
          <div class="p-6">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center">
                <div class="w-3 h-3 bg-red-500 rounded-full mr-3"></div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ matrixData.quadrant_info?.urgent_important?.title || 'Do First' }}
                  </h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    {{ matrixData.quadrant_info?.urgent_important?.description }}
                  </p>
                </div>
              </div>
              <span class="bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 text-xs px-2 py-1 rounded-full">
                {{ matrixData.matrix?.urgent_important?.length || 0 }} tasks
              </span>
            </div>
            
            <div class="space-y-3 max-h-96 overflow-y-auto">
              <TaskCard
                v-for="task in matrixData.matrix?.urgent_important || []"
                :key="task.id"
                :task="task"
                :quadrant="'urgent_important'"
                @move="moveTask"
                class="border-l-2 border-red-500"
              />
              
              <div v-if="(matrixData.matrix?.urgent_important?.length || 0) === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
                <svg class="w-8 h-8 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <p class="text-sm">No urgent & important tasks</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Quadrant 2: Important, Not Urgent (Schedule) -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow border-l-4 border-blue-500">
          <div class="p-6">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center">
                <div class="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ matrixData.quadrant_info?.not_urgent_important?.title || 'Schedule' }}
                  </h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    {{ matrixData.quadrant_info?.not_urgent_important?.description }}
                  </p>
                </div>
              </div>
              <span class="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs px-2 py-1 rounded-full">
                {{ matrixData.matrix?.not_urgent_important?.length || 0 }} tasks
              </span>
            </div>
            
            <div class="space-y-3 max-h-96 overflow-y-auto">
              <TaskCard
                v-for="task in matrixData.matrix?.not_urgent_important || []"
                :key="task.id"
                :task="task"
                :quadrant="'not_urgent_important'"
                @move="moveTask"
                class="border-l-2 border-blue-500"
              />
              
              <div v-if="(matrixData.matrix?.not_urgent_important?.length || 0) === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
                <svg class="w-8 h-8 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                <p class="text-sm">No important tasks to schedule</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Quadrant 3: Urgent, Not Important (Delegate) -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow border-l-4 border-yellow-500">
          <div class="p-6">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center">
                <div class="w-3 h-3 bg-yellow-500 rounded-full mr-3"></div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ matrixData.quadrant_info?.urgent_not_important?.title || 'Delegate' }}
                  </h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    {{ matrixData.quadrant_info?.urgent_not_important?.description }}
                  </p>
                </div>
              </div>
              <span class="bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 text-xs px-2 py-1 rounded-full">
                {{ matrixData.matrix?.urgent_not_important?.length || 0 }} tasks
              </span>
            </div>
            
            <div class="space-y-3 max-h-96 overflow-y-auto">
              <TaskCard
                v-for="task in matrixData.matrix?.urgent_not_important || []"
                :key="task.id"
                :task="task"
                :quadrant="'urgent_not_important'"
                @move="moveTask"
                class="border-l-2 border-yellow-500"
              />
              
              <div v-if="(matrixData.matrix?.urgent_not_important?.length || 0) === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
                <svg class="w-8 h-8 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
                </svg>
                <p class="text-sm">No urgent tasks to delegate</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Quadrant 4: Not Urgent, Not Important (Eliminate) -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow border-l-4 border-gray-500">
          <div class="p-6">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center">
                <div class="w-3 h-3 bg-gray-500 rounded-full mr-3"></div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ matrixData.quadrant_info?.not_urgent_not_important?.title || 'Eliminate' }}
                  </h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    {{ matrixData.quadrant_info?.not_urgent_not_important?.description }}
                  </p>
                </div>
              </div>
              <span class="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 text-xs px-2 py-1 rounded-full">
                {{ matrixData.matrix?.not_urgent_not_important?.length || 0 }} tasks
              </span>
            </div>
            
            <div class="space-y-3 max-h-96 overflow-y-auto">
              <TaskCard
                v-for="task in matrixData.matrix?.not_urgent_not_important || []"
                :key="task.id"
                :task="task"
                :quadrant="'not_urgent_not_important'"
                @move="moveTask"
                class="border-l-2 border-gray-500"
              />
              
              <div v-if="(matrixData.matrix?.not_urgent_not_important?.length || 0) === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
                <svg class="w-8 h-8 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
                <p class="text-sm">No low-priority tasks</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Statistics -->
      <div class="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Task Distribution Analysis</h3>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="text-center">
            <div class="text-3xl font-bold text-red-500">
              {{ matrixData.matrix?.urgent_important?.length || 0 }}
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400">Crisis Management</div>
            <div class="text-xs text-gray-500 mt-1">
              {{ getPercentage('urgent_important') }}% of total
            </div>
          </div>
          
          <div class="text-center">
            <div class="text-3xl font-bold text-blue-500">
              {{ matrixData.matrix?.not_urgent_important?.length || 0 }}
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400">Strategic Work</div>
            <div class="text-xs text-gray-500 mt-1">
              {{ getPercentage('not_urgent_important') }}% of total
            </div>
          </div>
          
          <div class="text-center">
            <div class="text-3xl font-bold text-yellow-500">
              {{ matrixData.matrix?.urgent_not_important?.length || 0 }}
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400">Interruptions</div>
            <div class="text-xs text-gray-500 mt-1">
              {{ getPercentage('urgent_not_important') }}% of total
            </div>
          </div>
          
          <div class="text-center">
            <div class="text-3xl font-bold text-gray-500">
              {{ matrixData.matrix?.not_urgent_not_important?.length || 0 }}
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400">Time Wasters</div>
            <div class="text-xs text-gray-500 mt-1">
              {{ getPercentage('not_urgent_not_important') }}% of total
            </div>
          </div>
        </div>

        <!-- Recommendations -->
        <div class="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          <h4 class="font-medium text-blue-900 dark:text-blue-100 mb-2">💡 Productivity Recommendations</h4>
          <ul class="text-sm text-blue-800 dark:text-blue-200 space-y-1">
            <li v-if="getPercentage('urgent_important') > 25">
              • Too many crisis tasks ({{ getPercentage('urgent_important') }}%) - focus on prevention in Quadrant 2
            </li>
            <li v-if="getPercentage('not_urgent_important') < 40">
              • Increase strategic work time - aim for 40-60% in Quadrant 2
            </li>
            <li v-if="getPercentage('urgent_not_important') > 20">
              • Consider delegating or saying no to Quadrant 3 tasks
            </li>
            <li v-if="getPercentage('not_urgent_not_important') > 15">
              • Eliminate or minimize Quadrant 4 activities
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import TaskCard from '../components/TaskCard.vue'

const API_BASE_URL = 'http://localhost:8000/api'

export default {
  name: 'EisenhowerMatrix',
  components: {
    TaskCard
  },
  setup() {
    const matrixData = ref({
      matrix: {},
      quadrant_info: {}
    })
    const loading = ref(false)
    const error = ref(null)
    
    const totalTasks = computed(() => {
      const matrix = matrixData.value.matrix || {}
      return Object.values(matrix).reduce((total, quadrant) => total + (quadrant?.length || 0), 0)
    })
    
    const getPercentage = (quadrant) => {
      const count = matrixData.value.matrix?.[quadrant]?.length || 0
      if (totalTasks.value === 0) return 0
      return Math.round((count / totalTasks.value) * 100)
    }
    
    const fetchMatrix = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await axios.get(`${API_BASE_URL}/eisenhower/matrix/`)
        matrixData.value = response.data
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load matrix'
        console.error('Matrix fetch error:', err)
      } finally {
        loading.value = false
      }
    }
    
    const moveTask = async (taskId, targetQuadrant) => {
      try {
        await axios.post(`${API_BASE_URL}/eisenhower/move_card/`, {
          card_id: taskId,
          quadrant: targetQuadrant
        })
        
        // Refresh matrix after move
        await fetchMatrix()
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to move task'
        console.error('Task move error:', err)
      }
    }
    
    const refreshMatrix = () => {
      fetchMatrix()
    }
    
    onMounted(() => {
      fetchMatrix()
    })
    
    return {
      matrixData,
      loading,
      error,
      totalTasks,
      getPercentage,
      moveTask,
      refreshMatrix
    }
  }
}
</script>