<template>
  <div 
    class="bg-white rounded-lg shadow-sm border border-gray-200 p-3 cursor-pointer hover:shadow-md transition-all duration-200"
    :class="[priorityClass, { 'ring-2 ring-blue-400 ring-opacity-50': isDragging }]"
    @click="showDetails = !showDetails"
    draggable="true"
    @dragstart="onDragStart"
    @dragend="onDragEnd"
  >
    <!-- Card Title -->
    <h4 class="text-sm font-medium text-gray-900 mb-2">{{ card.title }}</h4>
    
    <!-- Card Description (if exists) -->
    <p v-if="card.description" class="text-xs text-gray-600 mb-3 line-clamp-2">
      {{ card.description }}
    </p>
    
    <!-- Labels -->
    <div v-if="card.labels && card.labels.length > 0" class="flex flex-wrap gap-1 mb-3">
      <span 
        v-for="label in card.labels" 
        :key="label.id"
        class="px-2 py-0.5 text-xs font-medium rounded-full"
        :style="{ backgroundColor: label.color + '20', color: label.color }"
      >
        {{ label.name }}
      </span>
    </div>
    
    <!-- Progress bar for estimated hours -->
    <div v-if="card.estimated_hours" class="mb-3">
      <div class="flex justify-between text-xs text-gray-500 mb-1">
        <span>Progress</span>
        <span>{{ card.completed ? card.estimated_hours : 0 }}/{{ card.estimated_hours }}h</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-1.5">
        <div 
          class="h-1.5 rounded-full transition-all duration-300"
          :class="card.completed ? 'bg-green-500' : 'bg-blue-500'"
          :style="{ width: card.completed ? '100%' : '0%' }"
        ></div>
      </div>
    </div>
    
    <!-- Card Meta -->
    <div class="flex items-center justify-between text-xs text-gray-500">
      <div class="flex items-center space-x-2">
        <!-- Priority -->
        <span 
          class="px-1.5 py-0.5 rounded-full text-xs font-medium"
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
        
        <!-- Completed checkbox -->
        <button 
          @click.stop="toggleCompleted"
          class="flex items-center"
          :class="card.completed ? 'text-green-600' : 'text-gray-400 hover:text-gray-600'"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path v-if="card.completed" fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            <path v-else fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12z" clip-rule="evenodd"/>
          </svg>
        </button>
      </div>
      
      <!-- Actions and Assignee -->
      <div class="flex items-center space-x-1">
        <!-- Comments Count -->
        <span v-if="card.comments && card.comments.length" class="flex items-center text-gray-400">
          <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
          </svg>
          {{ card.comments.length }}
        </span>
        
        <!-- Assignee -->
        <div v-if="card.assignee" class="w-6 h-6 bg-gray-300 rounded-full flex items-center justify-center overflow-hidden">
          <img 
            v-if="card.assignee.profile?.avatar"
            :src="card.assignee.profile.avatar"
            :alt="card.assignee.username"
            class="w-full h-full object-cover"
          />
          <span v-else class="text-xs font-medium text-gray-700">
            {{ (card.assignee.profile?.display_name || card.assignee.username)[0].toUpperCase() }}
          </span>
        </div>
        
        <!-- Menu -->
        <button 
          @click.stop="showMenu = !showMenu"
          class="text-gray-400 hover:text-gray-600 p-1 relative"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
          </svg>
          
          <!-- Dropdown Menu -->
          <div v-if="showMenu" class="absolute right-0 mt-1 w-32 bg-white shadow-lg rounded-md py-1 z-20 border">
            <button 
              @click.stop="editCard"
              class="block px-3 py-1 text-xs text-gray-700 hover:bg-gray-50 w-full text-left"
            >
              Edit
            </button>
            <button 
              @click.stop="duplicateCard"
              class="block px-3 py-1 text-xs text-gray-700 hover:bg-gray-50 w-full text-left"
            >
              Duplicate
            </button>
            <button 
              @click.stop="deleteCard"
              class="block px-3 py-1 text-xs text-red-600 hover:bg-red-50 w-full text-left"
            >
              Delete
            </button>
          </div>
        </button>
      </div>
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
  name: 'EnhancedKanbanCard',
  components: {
    CardDetailsModal
  },
  props: {
    card: {
      type: Object,
      required: true
    }
  },
  emits: ['update', 'delete', 'move', 'duplicate'],
  setup(props, { emit }) {
    const showDetails = ref(false)
    const showMenu = ref(false)
    const isDragging = ref(false)
    
    const priorityClass = computed(() => {
      const classes = {
        low: 'border-l-4 border-green-400',
        medium: 'border-l-4 border-yellow-400',
        high: 'border-l-4 border-orange-400',
        urgent: 'border-l-4 border-red-400'
      }
      return classes[props.card.priority] || 'border-l-4 border-yellow-400'
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
      
      return isOverdue ? 'text-red-600 font-medium' : 'text-gray-500'
    })
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      
      // Check if it's today
      if (date.toDateString() === now.toDateString()) {
        return `Today ${date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}`
      }
      
      // Check if it's tomorrow
      const tomorrow = new Date(now)
      tomorrow.setDate(now.getDate() + 1)
      if (date.toDateString() === tomorrow.toDateString()) {
        return `Tomorrow ${date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}`
      }
      
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric'
      })
    }
    
    const toggleCompleted = () => {
      emit('update', { completed: !props.card.completed })
    }
    
    const editCard = () => {
      showMenu.value = false
      showDetails.value = true
    }
    
    const deleteCard = () => {
      showMenu.value = false
      if (confirm('Are you sure you want to delete this card?')) {
        emit('delete')
      }
    }
    
    const duplicateCard = () => {
      showMenu.value = false
      emit('duplicate')
    }
    
    const updateCard = (data) => {
      emit('update', data)
    }
    
    const onDragStart = (event) => {
      isDragging.value = true
      event.dataTransfer.setData('text/plain', JSON.stringify({
        cardId: props.card.id,
        sourceListId: props.card.list
      }))
      event.dataTransfer.effectAllowed = 'move'
    }
    
    const onDragEnd = () => {
      isDragging.value = false
    }
    
    return {
      showDetails,
      showMenu,
      isDragging,
      priorityClass,
      priorityBadgeClass,
      dueDateClass,
      formatDate,
      toggleCompleted,
      editCard,
      deleteCard,
      duplicateCard,
      updateCard,
      onDragStart,
      onDragEnd
    }
  }
}
</script>