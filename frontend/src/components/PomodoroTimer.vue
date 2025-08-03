<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center">
        <div class="w-8 h-8 bg-gradient-to-r from-red-500 to-pink-500 rounded-full flex items-center justify-center mr-3">
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Pomodoro Timer</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">Focus with the Pomodoro Technique</p>
        </div>
      </div>
      
      <button
        @click="showSettings = !showSettings"
        class="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
        </svg>
      </button>
    </div>

    <!-- Timer Display -->
    <div class="text-center mb-8">
      <!-- Session Type -->
      <div class="mb-4">
        <div class="flex justify-center space-x-2">
          <button
            v-for="type in sessionTypes"
            :key="type.value"
            @click="pomodoroStore.setSessionType(type.value)"
            class="px-3 py-1 text-sm rounded-full transition-colors"
            :class="pomodoroStore.sessionType === type.value
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'"
          >
            {{ type.label }}
          </button>
        </div>
      </div>

      <!-- Circular Progress -->
      <div class="relative w-48 h-48 mx-auto mb-6">
        <svg class="w-48 h-48 transform -rotate-90" viewBox="0 0 100 100">
          <!-- Background circle -->
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke="currentColor"
            stroke-width="2"
            fill="none"
            class="text-gray-200 dark:text-gray-700"
          />
          <!-- Progress circle -->
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke="currentColor"
            stroke-width="4"
            fill="none"
            stroke-linecap="round"
            :stroke-dasharray="circumference"
            :stroke-dashoffset="strokeDashoffset"
            :class="progressColor"
            class="transition-all duration-1000 ease-in-out"
          />
        </svg>
        
        <!-- Timer Text -->
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <div class="text-4xl font-bold text-gray-900 dark:text-white">
            {{ pomodoroStore.formattedTime }}
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {{ sessionTypeLabel }}
          </div>
          <div v-if="pomodoroStore.cycleCount > 0" class="text-xs text-gray-400 mt-1">
            Cycle {{ pomodoroStore.cycleCount }}
          </div>
        </div>
      </div>

      <!-- Controls -->
      <div class="flex justify-center space-x-4">
        <button
          v-if="!pomodoroStore.isActive && !pomodoroStore.currentSession"
          @click="startSession"
          class="px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition-colors"
        >
          Start
        </button>
        
        <button
          v-if="pomodoroStore.isActive"
          @click="pomodoroStore.pauseSession()"
          class="px-6 py-3 bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg font-medium transition-colors"
        >
          Pause
        </button>
        
        <button
          v-if="!pomodoroStore.isActive && pomodoroStore.currentSession"
          @click="pomodoroStore.resumeSession()"
          class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
        >
          Resume
        </button>
        
        <button
          v-if="pomodoroStore.currentSession"
          @click="pomodoroStore.stopSession()"
          class="px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-lg font-medium transition-colors"
        >
          Stop
        </button>
      </div>
    </div>

    <!-- Statistics -->
    <div class="grid grid-cols-2 gap-4 mb-6">
      <div class="text-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <div class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ pomodoroStore.todayStats.work_sessions }}
        </div>
        <div class="text-sm text-gray-600 dark:text-gray-400">Today</div>
      </div>
      
      <div class="text-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <div class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ pomodoroStore.weekStats.work_sessions }}
        </div>
        <div class="text-sm text-gray-600 dark:text-gray-400">This Week</div>
      </div>
    </div>

    <!-- Settings Panel -->
    <div v-if="showSettings" class="border-t border-gray-200 dark:border-gray-700 pt-6">
      <h4 class="font-medium text-gray-900 dark:text-white mb-4">Timer Settings</h4>
      
      <div class="space-y-4">
        <!-- Duration Settings -->
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Work (min)
            </label>
            <input
              v-model.number="localSettings.durations.work"
              type="number"
              min="1"
              max="60"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Short Break (min)
            </label>
            <input
              v-model.number="localSettings.durations.short_break"
              type="number"
              min="1"
              max="30"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Long Break (min)
            </label>
            <input
              v-model.number="localSettings.durations.long_break"
              type="number"
              min="1"
              max="60"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
          </div>
        </div>

        <!-- Auto-start Settings -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <label class="text-sm text-gray-700 dark:text-gray-300">Auto-start breaks</label>
            <input
              v-model="localSettings.settings.autoStartBreaks"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>
          
          <div class="flex items-center justify-between">
            <label class="text-sm text-gray-700 dark:text-gray-300">Auto-start work sessions</label>
            <input
              v-model="localSettings.settings.autoStartWork"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>
          
          <div class="flex items-center justify-between">
            <label class="text-sm text-gray-700 dark:text-gray-300">Enable notifications</label>
            <input
              v-model="localSettings.settings.notifications"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>
        </div>

        <!-- Save Settings -->
        <button
          @click="saveSettings"
          class="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          Save Settings
        </button>
      </div>
    </div>

    <!-- Task Selection Modal -->
    <TaskSelectionModal
      v-if="showTaskSelection"
      @close="showTaskSelection = false"
      @select="startSessionWithTask"
    />
  </div>
</template>

<script>
import { ref, computed, reactive, onMounted, onUnmounted } from 'vue'
import { usePomodoroStore } from '../stores/pomodoro'
import TaskSelectionModal from './TaskSelectionModal.vue'

export default {
  name: 'PomodoroTimer',
  components: {
    TaskSelectionModal
  },
  setup() {
    const pomodoroStore = usePomodoroStore()
    
    const showSettings = ref(false)
    const showTaskSelection = ref(false)
    
    const sessionTypes = [
      { value: 'work', label: 'Work' },
      { value: 'short_break', label: 'Short Break' },
      { value: 'long_break', label: 'Long Break' }
    ]
    
    const localSettings = reactive({
      durations: { ...pomodoroStore.durations },
      settings: { ...pomodoroStore.settings }
    })
    
    // Computed properties
    const circumference = 2 * Math.PI * 45 // radius = 45
    
    const strokeDashoffset = computed(() => {
      const progress = pomodoroStore.progressPercentage
      return circumference - (progress / 100) * circumference
    })
    
    const progressColor = computed(() => {
      if (pomodoroStore.sessionType === 'work') {
        return 'text-red-500'
      } else {
        return 'text-green-500'
      }
    })
    
    const sessionTypeLabel = computed(() => {
      const labels = {
        work: 'Focus Time',
        short_break: 'Short Break',
        long_break: 'Long Break'
      }
      return labels[pomodoroStore.sessionType] || 'Work'
    })
    
    // Methods
    const startSession = () => {
      if (pomodoroStore.sessionType === 'work') {
        showTaskSelection.value = true
      } else {
        pomodoroStore.startSession()
      }
    }
    
    const startSessionWithTask = (taskId) => {
      showTaskSelection.value = false
      pomodoroStore.startSession(taskId)
    }
    
    const saveSettings = () => {
      pomodoroStore.durations = { ...localSettings.durations }
      pomodoroStore.updateSettings(localSettings.settings)
      
      // Request notification permission if enabled
      if (localSettings.settings.notifications) {
        pomodoroStore.requestNotificationPermission()
      }
      
      showSettings.value = false
    }
    
    // Lifecycle
    onMounted(() => {
      pomodoroStore.loadSettings()
      pomodoroStore.fetchStats()
      
      // Sync local settings with store
      Object.assign(localSettings.durations, pomodoroStore.durations)
      Object.assign(localSettings.settings, pomodoroStore.settings)
    })
    
    onUnmounted(() => {
      pomodoroStore.stopTimer()
    })
    
    return {
      pomodoroStore,
      showSettings,
      showTaskSelection,
      sessionTypes,
      localSettings,
      circumference,
      strokeDashoffset,
      progressColor,
      sessionTypeLabel,
      startSession,
      startSessionWithTask,
      saveSettings
    }
  }
}
</script>