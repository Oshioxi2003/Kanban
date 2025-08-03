<template>
  <div 
    class="p-3 border rounded-lg hover:shadow-md transition-shadow cursor-pointer"
    :class="cardClass"
    @click="$emit('cardClick', card)"
  >
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <h4 class="text-sm font-medium text-gray-900 mb-1">{{ card.title }}</h4>
        <p v-if="card.description" class="text-xs text-gray-600 mb-2 line-clamp-2">
          {{ card.description }}
        </p>
        
        <!-- Labels -->
        <div v-if="card.labels && card.labels.length > 0" class="flex flex-wrap gap-1 mb-2">
          <span 
            v-for="label in card.labels" 
            :key="label.id"
            class="px-2 py-0.5 text-xs font-medium rounded-full"
            :style="{ backgroundColor: label.color + '20', color: label.color }"
          >
            {{ label.name }}
          </span>
        </div>
        
        <!-- Meta info -->
        <div class="flex items-center justify-between text-xs text-gray-500">
          <div class="flex items-center space-x-2">
            <!-- Priority -->
            <span 
              class="px-1.5 py-0.5 rounded text-xs font-medium"
              :class="priorityClass"
            >
              {{ card.priority }}
            </span>
            
            <!-- Due date -->
            <span v-if="card.due_date" class="flex items-center" :class="dueDateClass">
              <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              {{ formatDueDate(card.due_date) }}
            </span>
          </div>
          
          <!-- Assignee -->
          <div v-if="card.assignee" class="flex items-center">
            <img 
              :src="card.assignee.profile?.avatar || `https://ui-avatars.com/api/?name=${card.assignee.username}&background=3B82F6&color=fff`"
              :alt="card.assignee.username"
              class="w-5 h-5 rounded-full"
              :title="card.assignee.username"
            />
          </div>
        </div>
        
        <!-- Board and list info -->
        <div class="mt-2 text-xs text-gray-400">
          {{ card.list?.board?.title }} → {{ card.list?.title }}
        </div>
      </div>
      
      <!-- Status indicator -->
      <div class="ml-2">
        <div 
          class="w-3 h-3 rounded-full"
          :class="statusIndicatorClass"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'TimelineCard',
  props: {
    card: {
      type: Object,
      required: true
    },
    type: {
      type: String,
      default: 'normal' // 'normal', 'overdue', 'due-soon'
    }
  },
  emits: ['cardClick'],
  setup(props) {
    const cardClass = computed(() => {
      const baseClass = 'bg-white border-gray-200'
      
      switch (props.type) {
        case 'overdue':
          return `${baseClass} border-red-200 bg-red-50`
        case 'due-soon':
          return `${baseClass} border-yellow-200 bg-yellow-50`
        default:
          return baseClass
      }
    })
    
    const priorityClass = computed(() => {
      const classes = {
        low: 'bg-green-100 text-green-800',
        medium: 'bg-yellow-100 text-yellow-800',
        high: 'bg-orange-100 text-orange-800',
        urgent: 'bg-red-100 text-red-800'
      }
      return classes[props.card.priority] || 'bg-gray-100 text-gray-800'
    })
    
    const dueDateClass = computed(() => {
      if (!props.card.due_date) return ''
      
      const now = new Date()
      const dueDate = new Date(props.card.due_date)
      const isOverdue = dueDate < now && !props.card.completed
      
      return isOverdue ? 'text-red-600' : 'text-gray-500'
    })
    
    const statusIndicatorClass = computed(() => {
      if (props.card.completed) {
        return 'bg-green-400'
      }
      
      if (!props.card.due_date) {
        return 'bg-gray-300'
      }
      
      const now = new Date()
      const dueDate = new Date(props.card.due_date)
      
      if (dueDate < now) {
        return 'bg-red-400' // Overdue
      } else if (dueDate - now < 24 * 60 * 60 * 1000) {
        return 'bg-yellow-400' // Due soon
      } else {
        return 'bg-blue-400' // Normal
      }
    })
    
    const formatDueDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      
      // Check if it's today
      if (date.toDateString() === now.toDateString()) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
      
      // Check if it's this year
      if (date.getFullYear() === now.getFullYear()) {
        return date.toLocaleDateString([], { month: 'short', day: 'numeric' })
      }
      
      return date.toLocaleDateString([], { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric' 
      })
    }
    
    return {
      cardClass,
      priorityClass,
      dueDateClass,
      statusIndicatorClass,
      formatDueDate
    }
  }
}
</script>