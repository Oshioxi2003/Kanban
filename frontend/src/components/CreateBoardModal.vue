<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-medium text-gray-900">Create New Board</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
      
      <form @submit.prevent="createBoard" class="space-y-4">
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700 mb-1">
            Board Title *
          </label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter board title"
          />
        </div>
        
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            v-model="form.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter board description (optional)"
          ></textarea>
        </div>
        
        <div v-if="error" class="text-red-600 text-sm">{{ error }}</div>
        
        <div class="flex justify-end space-x-3 pt-4">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="loading || !form.title.trim()"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Creating...</span>
            <span v-else>Create Board</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useKanbanStore } from '../stores/kanban'

export default {
  name: 'CreateBoardModal',
  emits: ['close', 'created'],
  setup(_, { emit }) {
    const kanbanStore = useKanbanStore()
    
    const form = ref({
      title: '',
      description: ''
    })
    
    const loading = ref(false)
    const error = ref(null)
    
    const createBoard = async () => {
      if (!form.value.title.trim()) return
      
      loading.value = true
      error.value = null
      
      try {
        const board = await kanbanStore.createBoard(form.value)
        emit('created', board)
      } catch (err) {
        error.value = err.response?.data?.message || 'Failed to create board'
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      loading,
      error,
      createBoard
    }
  }
}
</script>