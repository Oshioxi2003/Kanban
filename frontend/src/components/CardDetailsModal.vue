<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-10 mx-auto p-6 border max-w-2xl shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-start justify-between mb-6">
        <div class="flex-1">
          <input
            v-model="form.title"
            class="text-xl font-semibold text-gray-900 bg-transparent border-none focus:outline-none focus:bg-gray-50 focus:border focus:border-blue-500 rounded px-2 py-1 w-full"
            @blur="updateCard"
          />
        </div>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 ml-4">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
      
      <div class="grid grid-cols-3 gap-6">
        <!-- Main Content -->
        <div class="col-span-2 space-y-6">
          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea
              v-model="form.description"
              @blur="updateCard"
              placeholder="Add a more detailed description..."
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows="4"
            ></textarea>
          </div>
          
          <!-- Comments -->
          <div>
            <h4 class="text-sm font-medium text-gray-700 mb-3">Comments</h4>
            <div class="space-y-3 mb-4 max-h-60 overflow-y-auto">
              <div 
                v-for="comment in card.comments" 
                :key="comment.id"
                class="bg-gray-50 rounded-lg p-3"
              >
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-gray-900">
                    {{ comment.author.first_name || comment.author.username }}
                  </span>
                  <span class="text-xs text-gray-500">
                    {{ formatDate(comment.created_at) }}
                  </span>
                </div>
                <p class="text-sm text-gray-700">{{ comment.content }}</p>
              </div>
            </div>
            
            <!-- Add Comment -->
            <div class="flex space-x-2">
              <textarea
                v-model="newComment"
                placeholder="Write a comment..."
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="2"
              ></textarea>
              <button 
                @click="addComment"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm"
              >
                Post
              </button>
            </div>
          </div>
        </div>
        
        <!-- Sidebar -->
        <div class="space-y-4">
          <!-- Priority -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Priority</label>
            <select
              v-model="form.priority"
              @change="updateCard"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
          
          <!-- Due Date -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
            <input
              v-model="form.due_date"
              @change="updateCard"
              type="datetime-local"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <!-- Completed -->
          <div class="flex items-center">
            <input
              v-model="form.completed"
              @change="updateCard"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label class="ml-2 text-sm text-gray-700">Mark as completed</label>
          </div>
          
          <!-- Actions -->
          <div class="pt-4 border-t">
            <button 
              @click="deleteCard"
              class="w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md border border-red-200"
            >
              Delete Card
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'

export default {
  name: 'CardDetailsModal',
  props: {
    card: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'update', 'delete'],
  setup(props, { emit }) {
    const form = reactive({
      title: props.card.title,
      description: props.card.description || '',
      priority: props.card.priority,
      due_date: props.card.due_date ? props.card.due_date.slice(0, 16) : '',
      completed: props.card.completed
    })
    
    const newComment = ref('')
    
    const updateCard = () => {
      const changes = {}
      Object.keys(form).forEach(key => {
        if (form[key] !== props.card[key]) {
          changes[key] = form[key]
        }
      })
      
      if (Object.keys(changes).length > 0) {
        emit('update', changes)
      }
    }
    
    const addComment = () => {
      if (!newComment.value.trim()) return
      
      // Here you would typically call an API to add the comment
      // For now, we'll just log it
      console.log('Adding comment:', newComment.value)
      newComment.value = ''
    }
    
    const deleteCard = () => {
      if (confirm('Are you sure you want to delete this card?')) {
        emit('delete')
        emit('close')
      }
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }
    
    return {
      form,
      newComment,
      updateCard,
      addComment,
      deleteCard,
      formatDate
    }
  }
}
</script>