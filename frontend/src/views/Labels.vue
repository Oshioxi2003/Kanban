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
              <span class="text-xl font-bold text-gray-900">Manage Labels</span>
            </router-link>
          </div>
          
          <div class="flex items-center">
            <button 
              @click="showCreateModal = true"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              New Label
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Success/Error messages -->
      <div v-if="successMessage" class="mb-4 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
        {{ successMessage }}
      </div>
      
      <div v-if="labelsStore.error" class="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {{ labelsStore.error }}
      </div>

      <!-- Loading state -->
      <div v-if="labelsStore.loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <!-- Labels grid -->
      <div v-else class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-6">Your Labels</h3>
          
          <div v-if="labelsStore.labels.length === 0" class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No labels</h3>
            <p class="mt-1 text-sm text-gray-500">Get started by creating a new label.</p>
            <div class="mt-6">
              <button 
                @click="showCreateModal = true"
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Create Label
              </button>
            </div>
          </div>
          
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div 
              v-for="label in labelsStore.labels" 
              :key="label.id"
              class="border rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center flex-1">
                  <div 
                    class="w-4 h-4 rounded-full mr-3"
                    :style="{ backgroundColor: label.color }"
                  ></div>
                  <span class="font-medium text-gray-900">{{ label.name }}</span>
                </div>
                
                <div class="flex items-center space-x-2">
                  <button 
                    @click="editLabel(label)"
                    class="text-gray-400 hover:text-gray-600"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  <button 
                    @click="deleteLabel(label)"
                    class="text-gray-400 hover:text-red-600"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </div>
              
              <div class="mt-2 text-sm text-gray-500">
                Created {{ formatDate(label.created_at) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Label Modal -->
    <div v-if="showCreateModal || editingLabel" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ editingLabel ? 'Edit Label' : 'Create New Label' }}
          </h3>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="saveLabel" class="space-y-4">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
              Label Name *
            </label>
            <input
              id="name"
              v-model="labelForm.name"
              type="text"
              required
              maxlength="50"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter label name"
            />
          </div>
          
          <div>
            <label for="color" class="block text-sm font-medium text-gray-700 mb-1">
              Color
            </label>
            <div class="flex items-center space-x-2">
              <input
                id="color"
                v-model="labelForm.color"
                type="color"
                class="w-12 h-10 border border-gray-300 rounded-md"
              />
              <input
                v-model="labelForm.color"
                type="text"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="#3B82F6"
              />
            </div>
            
            <!-- Preset colors -->
            <div class="mt-2">
              <span class="text-sm text-gray-600">Quick colors:</span>
              <div class="flex space-x-2 mt-1">
                <button
                  v-for="color in presetColors"
                  :key="color"
                  type="button"
                  @click="labelForm.color = color"
                  class="w-6 h-6 rounded border-2 hover:border-gray-400"
                  :class="labelForm.color === color ? 'border-gray-900' : 'border-gray-200'"
                  :style="{ backgroundColor: color }"
                ></button>
              </div>
            </div>
          </div>
          
          <!-- Preview -->
          <div class="bg-gray-50 p-3 rounded-md">
            <span class="text-sm text-gray-600">Preview:</span>
            <div class="flex items-center mt-1">
              <div 
                class="w-4 h-4 rounded-full mr-2"
                :style="{ backgroundColor: labelForm.color }"
              ></div>
              <span class="text-sm font-medium">{{ labelForm.name || 'Label name' }}</span>
            </div>
          </div>
          
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="!labelForm.name.trim()"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ editingLabel ? 'Update Label' : 'Create Label' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useLabelsStore } from '../stores/labels'

export default {
  name: 'Labels',
  setup() {
    const labelsStore = useLabelsStore()
    const showCreateModal = ref(false)
    const editingLabel = ref(null)
    const successMessage = ref('')
    
    const labelForm = reactive({
      name: '',
      color: '#3B82F6'
    })
    
    const presetColors = [
      '#3B82F6', // Blue
      '#EF4444', // Red
      '#10B981', // Green
      '#F59E0B', // Yellow
      '#8B5CF6', // Purple
      '#EC4899', // Pink
      '#06B6D4', // Cyan
      '#84CC16', // Lime
      '#F97316', // Orange
      '#6B7280'  // Gray
    ]
    
    const editLabel = (label) => {
      editingLabel.value = label
      labelForm.name = label.name
      labelForm.color = label.color
    }
    
    const closeModal = () => {
      showCreateModal.value = false
      editingLabel.value = null
      labelForm.name = ''
      labelForm.color = '#3B82F6'
    }
    
    const saveLabel = async () => {
      try {
        if (editingLabel.value) {
          await labelsStore.updateLabel(editingLabel.value.id, labelForm)
          successMessage.value = 'Label updated successfully!'
        } else {
          await labelsStore.createLabel(labelForm)
          successMessage.value = 'Label created successfully!'
        }
        
        closeModal()
        setTimeout(() => {
          successMessage.value = ''
        }, 3000)
      } catch (error) {
        console.error('Save label error:', error)
      }
    }
    
    const deleteLabel = async (label) => {
      if (confirm(`Are you sure you want to delete the label "${label.name}"? This action cannot be undone.`)) {
        try {
          await labelsStore.deleteLabel(label.id)
          successMessage.value = 'Label deleted successfully!'
          setTimeout(() => {
            successMessage.value = ''
          }, 3000)
        } catch (error) {
          console.error('Delete label error:', error)
        }
      }
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }
    
    onMounted(() => {
      labelsStore.fetchLabels()
    })
    
    return {
      labelsStore,
      showCreateModal,
      editingLabel,
      successMessage,
      labelForm,
      presetColors,
      editLabel,
      closeModal,
      saveLabel,
      deleteLabel,
      formatDate
    }
  }
}
</script>