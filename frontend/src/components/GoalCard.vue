<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
    <!-- Header -->
    <div class="flex items-start justify-between mb-4">
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ goal.title }}</h3>
        <p v-if="goal.description" class="text-sm text-gray-600 line-clamp-2">
          {{ goal.description }}
        </p>
      </div>
      
      <!-- Menu -->
      <div class="relative">
        <button 
          @click="showMenu = !showMenu"
          class="p-1 text-gray-400 hover:text-gray-600 rounded"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
          </svg>
        </button>
        
        <!-- Dropdown menu -->
        <div v-if="showMenu" class="absolute right-0 mt-1 w-32 bg-white shadow-lg rounded-md py-1 z-20 border">
          <button 
            @click="viewDetails"
            class="block px-3 py-1 text-xs text-gray-700 hover:bg-gray-50 w-full text-left"
          >
            View Details
          </button>
          <button 
            @click="editGoal"
            class="block px-3 py-1 text-xs text-gray-700 hover:bg-gray-50 w-full text-left"
          >
            Edit
          </button>
          <button 
            v-if="!goal.is_completed"
            @click="completeGoal"
            class="block px-3 py-1 text-xs text-green-600 hover:bg-green-50 w-full text-left"
          >
            Mark Complete
          </button>
          <button 
            v-else
            @click="reopenGoal"
            class="block px-3 py-1 text-xs text-blue-600 hover:bg-blue-50 w-full text-left"
          >
            Reopen
          </button>
          <button 
            @click="deleteGoal"
            class="block px-3 py-1 text-xs text-red-600 hover:bg-red-50 w-full text-left"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
    
    <!-- Progress bar -->
    <div class="mb-4">
      <div class="flex justify-between text-sm text-gray-600 mb-2">
        <span>Progress</span>
        <span>{{ goal.progress_percentage }}%</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          class="h-2 rounded-full transition-all duration-300"
          :class="progressBarClass"
          :style="{ width: `${goal.progress_percentage}%` }"
        ></div>
      </div>
    </div>
    
    <!-- Stats -->
    <div class="flex items-center justify-between text-sm text-gray-500 mb-4">
      <div class="flex items-center space-x-4">
        <span class="flex items-center">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          {{ goal.completed_cards_count }}/{{ goal.cards_count }} tasks
        </span>
        
        <span v-if="goal.target_date" class="flex items-center" :class="dueDateClass">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          {{ formatDate(goal.target_date) }}
        </span>
      </div>
    </div>
    
    <!-- Status badges -->
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <span 
          v-if="goal.is_completed"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
        >
          <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
          </svg>
          Completed
        </span>
        
        <span 
          v-else-if="goal.is_overdue"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"
        >
          <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
          </svg>
          Overdue
        </span>
        
        <span 
          v-else-if="goal.progress_percentage === 0"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
        >
          Not Started
        </span>
        
        <span 
          v-else-if="goal.progress_percentage < 100"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
        >
          In Progress
        </span>
      </div>
      
      <!-- Action button -->
      <button
        @click="viewDetails"
        class="text-sm text-blue-600 hover:text-blue-500 font-medium"
      >
        View Details →
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'GoalCard',
  props: {
    goal: {
      type: Object,
      required: true
    }
  },
  emits: ['edit', 'complete', 'reopen', 'delete', 'view-details'],
  setup(props, { emit }) {
    const showMenu = ref(false)
    
    const progressBarClass = computed(() => {
      if (props.goal.is_completed) {
        return 'bg-green-500'
      } else if (props.goal.progress_percentage >= 75) {
        return 'bg-blue-500'
      } else if (props.goal.progress_percentage >= 50) {
        return 'bg-yellow-500'
      } else if (props.goal.progress_percentage > 0) {
        return 'bg-orange-500'
      } else {
        return 'bg-gray-400'
      }
    })
    
    const dueDateClass = computed(() => {
      if (!props.goal.target_date) return ''
      
      if (props.goal.is_overdue && !props.goal.is_completed) {
        return 'text-red-600'
      } else {
        return 'text-gray-500'
      }
    })
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const today = new Date()
      const tomorrow = new Date(today)
      tomorrow.setDate(today.getDate() + 1)
      
      const dateStr = date.toDateString()
      const todayStr = today.toDateString()
      const tomorrowStr = tomorrow.toDateString()
      
      if (dateStr === todayStr) {
        return 'Today'
      } else if (dateStr === tomorrowStr) {
        return 'Tomorrow'
      } else {
        return date.toLocaleDateString('en-US', { 
          month: 'short', 
          day: 'numeric',
          year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined
        })
      }
    }
    
    const viewDetails = () => {
      showMenu.value = false
      emit('view-details', props.goal)
    }
    
    const editGoal = () => {
      showMenu.value = false
      emit('edit', props.goal)
    }
    
    const completeGoal = () => {
      showMenu.value = false
      emit('complete', props.goal)
    }
    
    const reopenGoal = () => {
      showMenu.value = false
      emit('reopen', props.goal)
    }
    
    const deleteGoal = () => {
      showMenu.value = false
      emit('delete', props.goal)
    }
    
    return {
      showMenu,
      progressBarClass,
      dueDateClass,
      formatDate,
      viewDetails,
      editGoal,
      completeGoal,
      reopenGoal,
      deleteGoal
    }
  }
}
</script>