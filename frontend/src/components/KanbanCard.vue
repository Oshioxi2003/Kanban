<template>
  <div 
    class="bg-white rounded-lg shadow-sm border border-gray-200 p-3 cursor-pointer hover:shadow-md transition-shadow"
    :class="priorityClass"
    @click="showDetails = !showDetails"
  >
    <!-- Card Title -->
    <h4 class="text-sm font-medium text-gray-900 mb-2">{{ card.title }}</h4>
    
    <!-- Card Description (if exists) -->
    <p v-if="card.description" class="text-xs text-gray-600 mb-3">
      {{ card.description.substring(0, 100) }}{{ card.description.length > 100 ? '...' : '' }}
    </p>
    
    <!-- Card Meta -->
    <div class="flex items-center justify-between text-xs text-gray-500">
      <div class="flex items-center space-x-2">
        <!-- Priority -->
        <span 
          class="px-2 py-1 rounded-full text-xs font-medium"
          :class="priorityBadgeClass"
        >
          {{ card.priority }}
        </span>
        
        <!-- Due Date -->
        <span v-if="card.due_date" class="flex items-center" :class="dueDateClass">
          <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          {{ formatDate(card.due_date) }}
        </span>
      </div>
      
      <!-- Actions -->
      <div class="flex items-center space-x-1">
        <!-- Comments Count -->
        <span v-if="card.comments && card.comments.length" class="flex items-center">
          <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
          </svg>
          {{ card.comments.length }}
        </span>
        
        <!-- Assignee -->
        <div v-if="card.assignee" class="w-5 h-5 bg-gray-300 rounded-full flex items-center justify-center">
          <span class="text-xs font-medium text-gray-700">
            {{ card.assignee.first_name ? card.assignee.first_name[0] : card.assignee.username[0] }}
          </span>
        </div>
        
        <!-- Menu -->
        <button 
          @click.stop="showMenu = !showMenu"
          class="text-gray-400 hover:text-gray-600 p-1"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Dropdown Menu -->
    <div v-if="showMenu" class="absolute bg-white shadow-lg rounded-md py-1 z-20 mt-2 right-0">
      <button 
        @click.stop="editCard"
        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 w-full text-left"
      >
        Edit
      </button>
      <button 
        @click.stop="deleteCard"
        class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 w-full text-left"
      >
        Delete
      </button>
    </div>
    
    <!-- Card Details Modal -->
    <CardDetailsModal
      v-if="showDetails"
      :card="card"
      @close="showDetails = false"
      @update="updateCard"
      @delete="deleteCard"
    />
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import CardDetailsModal from './CardDetailsModal.vue'

export default {
  name: 'KanbanCard',
  components: {
    CardDetailsModal
  },
  props: {
    card: {
      type: Object,
      required: true
    }
  },
  emits: ['update', 'delete'],
  setup(props, { emit }) {
    const showDetails = ref(false)
    const showMenu = ref(false)
    
    const priorityClass = computed(() => {
      const classes = {
        low: 'priority-low',
        medium: 'priority-medium',
        high: 'priority-high',
        urgent: 'priority-urgent'
      }
      return classes[props.card.priority] || 'priority-medium'
    })
    
    const priorityBadgeClass = computed(() => {
      const classes = {
        low: 'bg-green-100 text-green-800',
        medium: 'bg-yellow-100 text-yellow-800',
        high: 'bg-orange-100 text-orange-800',
        urgent: 'bg-red-100 text-red-800'
      }
      return classes[props.card.priority] || 'bg-yellow-100 text-yellow-800'
    })
    
    const dueDateClass = computed(() => {
      if (!props.card.due_date) return ''
      
      const now = new Date()
      const dueDate = new Date(props.card.due_date)
      const isOverdue = dueDate < now && !props.card.completed
      
      return isOverdue ? 'text-red-600' : 'text-gray-500'
    })
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      })
    }
    
    const editCard = () => {
      showMenu.value = false
      showDetails.value = true
    }
    
    const deleteCard = () => {
      showMenu.value = false
      emit('delete')
    }
    
    const updateCard = (data) => {
      emit('update', data)
    }
    
    return {
      showDetails,
      showMenu,
      priorityClass,
      priorityBadgeClass,
      dueDateClass,
      formatDate,
      editCard,
      deleteCard,
      updateCard
    }
  }
}
</script>