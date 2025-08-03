<template>
  <div class="bg-white shadow rounded-lg p-6 mb-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-medium text-gray-900">Search & Filter</h3>
      <button 
        @click="clearAllFilters"
        v-if="hasActiveFilters"
        class="text-sm text-gray-500 hover:text-gray-700"
      >
        Clear all filters
      </button>
    </div>
    
    <!-- Search input -->
    <div class="mb-4">
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
        <input
          v-model="searchQuery"
          @input="debouncedSearch"
          type="text"
          placeholder="Search tasks by title, description, or labels..."
          class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
        />
        <div v-if="searchQuery" class="absolute inset-y-0 right-0 pr-3 flex items-center">
          <button
            @click="clearSearch"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Filter toggles -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
      <!-- Labels filter -->
      <div class="relative">
        <button
          @click="showLabelsFilter = !showLabelsFilter"
          class="w-full flex items-center justify-between px-3 py-2 border border-gray-300 rounded-md text-sm bg-white hover:bg-gray-50"
        >
          <span class="flex items-center">
            <svg class="w-4 h-4 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
            </svg>
            Labels
            <span v-if="selectedLabels.length" class="ml-1 bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full">
              {{ selectedLabels.length }}
            </span>
          </span>
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
        
        <!-- Labels dropdown -->
        <div v-if="showLabelsFilter" class="absolute z-10 mt-1 w-full bg-white shadow-lg rounded-md border max-h-60 overflow-y-auto">
          <div class="p-2">
            <div v-for="label in labelsStore.labels" :key="label.id" class="flex items-center p-2 hover:bg-gray-50 rounded">
              <input
                :id="`label-${label.id}`"
                v-model="selectedLabels"
                :value="label.id"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label :for="`label-${label.id}`" class="ml-2 flex items-center cursor-pointer flex-1">
                <div 
                  class="w-3 h-3 rounded-full mr-2"
                  :style="{ backgroundColor: label.color }"
                ></div>
                <span class="text-sm text-gray-900">{{ label.name }}</span>
              </label>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Priority filter -->
      <div class="relative">
        <button
          @click="showPriorityFilter = !showPriorityFilter"
          class="w-full flex items-center justify-between px-3 py-2 border border-gray-300 rounded-md text-sm bg-white hover:bg-gray-50"
        >
          <span class="flex items-center">
            <svg class="w-4 h-4 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
            </svg>
            Priority
            <span v-if="selectedPriorities.length" class="ml-1 bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full">
              {{ selectedPriorities.length }}
            </span>
          </span>
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
        
        <!-- Priority dropdown -->
        <div v-if="showPriorityFilter" class="absolute z-10 mt-1 w-full bg-white shadow-lg rounded-md border">
          <div class="p-2">
            <div v-for="priority in priorities" :key="priority.value" class="flex items-center p-2 hover:bg-gray-50 rounded">
              <input
                :id="`priority-${priority.value}`"
                v-model="selectedPriorities"
                :value="priority.value"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label :for="`priority-${priority.value}`" class="ml-2 flex items-center cursor-pointer flex-1">
                <span 
                  class="w-3 h-3 rounded-full mr-2"
                  :class="priority.colorClass"
                ></span>
                <span class="text-sm text-gray-900">{{ priority.label }}</span>
              </label>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Due date filter -->
      <div class="relative">
        <button
          @click="showDueDateFilter = !showDueDateFilter"
          class="w-full flex items-center justify-between px-3 py-2 border border-gray-300 rounded-md text-sm bg-white hover:bg-gray-50"
        >
          <span class="flex items-center">
            <svg class="w-4 h-4 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            Due Date
            <span v-if="selectedDueDate" class="ml-1 bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full">
              1
            </span>
          </span>
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
        
        <!-- Due date dropdown -->
        <div v-if="showDueDateFilter" class="absolute z-10 mt-1 w-full bg-white shadow-lg rounded-md border">
          <div class="p-2">
            <div v-for="option in dueDateOptions" :key="option.value" class="flex items-center p-2 hover:bg-gray-50 rounded">
              <input
                :id="`due-${option.value}`"
                v-model="selectedDueDate"
                :value="option.value"
                name="due-date"
                type="radio"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
              />
              <label :for="`due-${option.value}`" class="ml-2 flex items-center cursor-pointer flex-1">
                <span class="text-sm text-gray-900">{{ option.label }}</span>
              </label>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Status filter -->
      <div class="relative">
        <button
          @click="showStatusFilter = !showStatusFilter"
          class="w-full flex items-center justify-between px-3 py-2 border border-gray-300 rounded-md text-sm bg-white hover:bg-gray-50"
        >
          <span class="flex items-center">
            <svg class="w-4 h-4 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            Status
            <span v-if="selectedStatuses.length" class="ml-1 bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full">
              {{ selectedStatuses.length }}
            </span>
          </span>
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
        
        <!-- Status dropdown -->
        <div v-if="showStatusFilter" class="absolute z-10 mt-1 w-full bg-white shadow-lg rounded-md border">
          <div class="p-2">
            <div v-for="status in statuses" :key="status.value" class="flex items-center p-2 hover:bg-gray-50 rounded">
              <input
                :id="`status-${status.value}`"
                v-model="selectedStatuses"
                :value="status.value"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label :for="`status-${status.value}`" class="ml-2 flex items-center cursor-pointer flex-1">
                <span 
                  class="w-3 h-3 rounded-full mr-2"
                  :class="status.colorClass"
                ></span>
                <span class="text-sm text-gray-900">{{ status.label }}</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Active filters display -->
    <div v-if="hasActiveFilters" class="flex flex-wrap gap-2">
      <span v-if="searchQuery" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
        Search: {{ searchQuery }}
        <button @click="clearSearch" class="ml-1.5 h-4 w-4 text-blue-400 hover:text-blue-600">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </span>
      
      <span v-for="labelId in selectedLabels" :key="`label-${labelId}`" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
        {{ labelsStore.getLabelById(labelId)?.name }}
        <button @click="removeLabel(labelId)" class="ml-1.5 h-4 w-4 text-purple-400 hover:text-purple-600">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </span>
      
      <span v-for="priority in selectedPriorities" :key="`priority-${priority}`" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
        {{ priority }} priority
        <button @click="removePriority(priority)" class="ml-1.5 h-4 w-4 text-orange-400 hover:text-orange-600">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </span>
      
      <span v-if="selectedDueDate" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
        {{ dueDateOptions.find(d => d.value === selectedDueDate)?.label }}
        <button @click="selectedDueDate = null" class="ml-1.5 h-4 w-4 text-yellow-400 hover:text-yellow-600">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </span>
      
      <span v-for="status in selectedStatuses" :key="`status-${status}`" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
        {{ status }}
        <button @click="removeStatus(status)" class="ml-1.5 h-4 w-4 text-green-400 hover:text-green-600">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </span>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useLabelsStore } from '../stores/labels'

export default {
  name: 'SearchFilter',
  emits: ['search', 'filter'],
  setup(_, { emit }) {
    const labelsStore = useLabelsStore()
    
    // Search
    const searchQuery = ref('')
    
    // Filter dropdowns visibility
    const showLabelsFilter = ref(false)
    const showPriorityFilter = ref(false)
    const showDueDateFilter = ref(false)
    const showStatusFilter = ref(false)
    
    // Filter selections
    const selectedLabels = ref([])
    const selectedPriorities = ref([])
    const selectedDueDate = ref(null)
    const selectedStatuses = ref([])
    
    // Filter options
    const priorities = [
      { value: 'low', label: 'Low', colorClass: 'bg-green-400' },
      { value: 'medium', label: 'Medium', colorClass: 'bg-yellow-400' },
      { value: 'high', label: 'High', colorClass: 'bg-orange-400' },
      { value: 'urgent', label: 'Urgent', colorClass: 'bg-red-400' }
    ]
    
    const dueDateOptions = [
      { value: null, label: 'All' },
      { value: 'overdue', label: 'Overdue' },
      { value: 'due_soon', label: 'Due Soon (3 days)' },
      { value: 'no_due_date', label: 'No Due Date' }
    ]
    
    const statuses = [
      { value: 'completed', label: 'Completed', colorClass: 'bg-green-400' },
      { value: 'pending', label: 'Pending', colorClass: 'bg-gray-400' }
    ]
    
    const hasActiveFilters = computed(() => {
      return searchQuery.value ||
             selectedLabels.value.length > 0 ||
             selectedPriorities.value.length > 0 ||
             selectedDueDate.value ||
             selectedStatuses.value.length > 0
    })
    
    // Debounced search
    let searchTimeout = null
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        emitSearch()
      }, 300)
    }
    
    const emitSearch = () => {
      emit('search', searchQuery.value)
    }
    
    const emitFilters = () => {
      const filters = {}
      
      if (selectedLabels.value.length > 0) {
        filters.labels = selectedLabels.value
      }
      
      if (selectedPriorities.value.length > 0) {
        filters.priority = selectedPriorities.value
      }
      
      if (selectedDueDate.value) {
        filters.due_date = selectedDueDate.value
      }
      
      if (selectedStatuses.value.length > 0) {
        filters.status = selectedStatuses.value
      }
      
      emit('filter', filters)
    }
    
    const clearSearch = () => {
      searchQuery.value = ''
      emitSearch()
    }
    
    const clearAllFilters = () => {
      searchQuery.value = ''
      selectedLabels.value = []
      selectedPriorities.value = []
      selectedDueDate.value = null
      selectedStatuses.value = []
      closeAllDropdowns()
      emitSearch()
      emitFilters()
    }
    
    const removeLabel = (labelId) => {
      selectedLabels.value = selectedLabels.value.filter(id => id !== labelId)
    }
    
    const removePriority = (priority) => {
      selectedPriorities.value = selectedPriorities.value.filter(p => p !== priority)
    }
    
    const removeStatus = (status) => {
      selectedStatuses.value = selectedStatuses.value.filter(s => s !== status)
    }
    
    const closeAllDropdowns = () => {
      showLabelsFilter.value = false
      showPriorityFilter.value = false
      showDueDateFilter.value = false
      showStatusFilter.value = false
    }
    
    // Close dropdowns when clicking outside
    const handleClickOutside = (event) => {
      if (!event.target.closest('.relative')) {
        closeAllDropdowns()
      }
    }
    
    // Watch for filter changes
    watch([selectedLabels, selectedPriorities, selectedDueDate, selectedStatuses], () => {
      emitFilters()
    }, { deep: true })
    
    onMounted(() => {
      labelsStore.fetchLabels()
      document.addEventListener('click', handleClickOutside)
    })
    
    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })
    
    return {
      labelsStore,
      searchQuery,
      showLabelsFilter,
      showPriorityFilter,
      showDueDateFilter,
      showStatusFilter,
      selectedLabels,
      selectedPriorities,
      selectedDueDate,
      selectedStatuses,
      priorities,
      dueDateOptions,
      statuses,
      hasActiveFilters,
      debouncedSearch,
      clearSearch,
      clearAllFilters,
      removeLabel,
      removePriority,
      removeStatus
    }
  }
}
</script>