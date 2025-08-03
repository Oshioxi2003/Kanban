<template>
  <div class="space-y-3">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <svg class="w-4 h-4 text-gray-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
        </svg>
        <span class="text-sm font-medium text-gray-900 dark:text-white">
          Checklist
          <span v-if="items.length > 0" class="text-gray-500">
            ({{ completedCount }}/{{ items.length }})
          </span>
        </span>
      </div>
      
      <button
        @click="showAddItem = !showAddItem"
        class="text-sm text-blue-600 hover:text-blue-500 font-medium"
      >
        Add item
      </button>
    </div>

    <!-- Progress bar -->
    <div v-if="items.length > 0" class="w-full bg-gray-200 rounded-full h-2">
      <div 
        class="bg-green-500 h-2 rounded-full transition-all duration-300"
        :style="{ width: `${progressPercentage}%` }"
      ></div>
    </div>

    <!-- Add new item form -->
    <div v-if="showAddItem" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
      <form @submit.prevent="addItem" class="space-y-2">
        <input
          v-model="newItemTitle"
          ref="newItemInput"
          type="text"
          placeholder="Add checklist item..."
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          @keydown.escape="cancelAdd"
        />
        <div class="flex justify-end space-x-2">
          <button
            type="button"
            @click="cancelAdd"
            class="px-3 py-1 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="!newItemTitle.trim()"
            class="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Add
          </button>
        </div>
      </form>
    </div>

    <!-- Checklist items -->
    <div class="space-y-2">
      <draggable
        v-model="localItems"
        @end="onReorder"
        item-key="id"
        handle=".drag-handle"
        ghost-class="opacity-50"
      >
        <template #item="{ element: item, index }">
          <div 
            class="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 group"
            :class="{ 'opacity-60': item.is_completed }"
          >
            <!-- Drag handle -->
            <div class="drag-handle cursor-move opacity-0 group-hover:opacity-100 transition-opacity">
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
            </div>

            <!-- Checkbox -->
            <button
              @click="toggleItem(item)"
              class="flex-shrink-0 w-4 h-4 border-2 rounded transition-colors"
              :class="item.is_completed 
                ? 'bg-green-500 border-green-500' 
                : 'border-gray-300 dark:border-gray-600 hover:border-green-400'"
            >
              <svg v-if="item.is_completed" class="w-3 h-3 text-white m-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </button>

            <!-- Item content -->
            <div class="flex-1 min-w-0">
              <div v-if="editingItem === item.id" class="flex space-x-2">
                <input
                  v-model="editTitle"
                  ref="editInput"
                  type="text"
                  class="flex-1 px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  @keydown.enter="saveEdit(item)"
                  @keydown.escape="cancelEdit"
                />
                <button
                  @click="saveEdit(item)"
                  class="px-2 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700"
                >
                  Save
                </button>
                <button
                  @click="cancelEdit"
                  class="px-2 py-1 text-xs bg-gray-600 text-white rounded hover:bg-gray-700"
                >
                  Cancel
                </button>
              </div>
              
              <div v-else class="flex items-center justify-between group">
                <span 
                  class="text-sm text-gray-900 dark:text-white cursor-pointer hover:text-blue-600"
                  :class="{ 'line-through text-gray-500': item.is_completed }"
                  @click="startEdit(item)"
                >
                  {{ item.title }}
                </span>
                
                <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    @click="startEdit(item)"
                    class="p-1 text-gray-400 hover:text-blue-600"
                    title="Edit"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  
                  <button
                    @click="deleteItem(item)"
                    class="p-1 text-gray-400 hover:text-red-600"
                    title="Delete"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </template>
      </draggable>
    </div>

    <!-- Empty state -->
    <div v-if="items.length === 0 && !showAddItem" class="text-center py-4 text-gray-500 dark:text-gray-400">
      <svg class="w-8 h-8 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
      </svg>
      <p class="text-sm">No checklist items yet</p>
      <button
        @click="showAddItem = true"
        class="mt-1 text-sm text-blue-600 hover:text-blue-500"
      >
        Add your first item
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, nextTick } from 'vue'
import draggable from 'vuedraggable'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export default {
  name: 'TaskChecklist',
  components: {
    draggable
  },
  props: {
    cardId: {
      type: Number,
      required: true
    },
    items: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:items', 'progress-changed'],
  setup(props, { emit }) {
    const showAddItem = ref(false)
    const newItemTitle = ref('')
    const editingItem = ref(null)
    const editTitle = ref('')
    const newItemInput = ref(null)
    const editInput = ref(null)
    
    const localItems = ref([...props.items])
    
    // Computed properties
    const completedCount = computed(() => {
      return localItems.value.filter(item => item.is_completed).length
    })
    
    const progressPercentage = computed(() => {
      if (localItems.value.length === 0) return 0
      return Math.round((completedCount.value / localItems.value.length) * 100)
    })
    
    // Watch for prop changes
    watch(() => props.items, (newItems) => {
      localItems.value = [...newItems]
    }, { deep: true })
    
    // Watch for local changes to emit updates
    watch(localItems, () => {
      emit('update:items', [...localItems.value])
      emit('progress-changed', {
        total: localItems.value.length,
        completed: completedCount.value,
        percentage: progressPercentage.value
      })
    }, { deep: true })
    
    // Methods
    const addItem = async () => {
      if (!newItemTitle.value.trim()) return
      
      try {
        const response = await axios.post(`${API_BASE_URL}/checklists/`, {
          card: props.cardId,
          title: newItemTitle.value.trim()
        })
        
        localItems.value.push(response.data)
        newItemTitle.value = ''
        showAddItem.value = false
      } catch (error) {
        console.error('Failed to add checklist item:', error)
      }
    }
    
    const cancelAdd = () => {
      newItemTitle.value = ''
      showAddItem.value = false
    }
    
    const toggleItem = async (item) => {
      try {
        const response = await axios.post(`${API_BASE_URL}/checklists/${item.id}/toggle_completed/`)
        
        // Update local item
        const index = localItems.value.findIndex(i => i.id === item.id)
        if (index !== -1) {
          localItems.value[index] = response.data
        }
      } catch (error) {
        console.error('Failed to toggle checklist item:', error)
      }
    }
    
    const startEdit = (item) => {
      editingItem.value = item.id
      editTitle.value = item.title
      
      nextTick(() => {
        if (editInput.value) {
          editInput.value.focus()
          editInput.value.select()
        }
      })
    }
    
    const saveEdit = async (item) => {
      if (!editTitle.value.trim()) {
        cancelEdit()
        return
      }
      
      try {
        const response = await axios.patch(`${API_BASE_URL}/checklists/${item.id}/`, {
          title: editTitle.value.trim()
        })
        
        // Update local item
        const index = localItems.value.findIndex(i => i.id === item.id)
        if (index !== -1) {
          localItems.value[index] = response.data
        }
        
        cancelEdit()
      } catch (error) {
        console.error('Failed to update checklist item:', error)
      }
    }
    
    const cancelEdit = () => {
      editingItem.value = null
      editTitle.value = ''
    }
    
    const deleteItem = async (item) => {
      if (!confirm('Are you sure you want to delete this checklist item?')) return
      
      try {
        await axios.delete(`${API_BASE_URL}/checklists/${item.id}/`)
        
        // Remove from local items
        const index = localItems.value.findIndex(i => i.id === item.id)
        if (index !== -1) {
          localItems.value.splice(index, 1)
        }
      } catch (error) {
        console.error('Failed to delete checklist item:', error)
      }
    }
    
    const onReorder = async () => {
      // Update positions
      const itemsWithPositions = localItems.value.map((item, index) => ({
        id: item.id,
        position: index
      }))
      
      try {
        await axios.post(`${API_BASE_URL}/checklists/reorder/`, {
          items: itemsWithPositions
        })
      } catch (error) {
        console.error('Failed to reorder checklist items:', error)
      }
    }
    
    // Focus new item input when shown
    watch(showAddItem, (show) => {
      if (show) {
        nextTick(() => {
          if (newItemInput.value) {
            newItemInput.value.focus()
          }
        })
      }
    })
    
    return {
      showAddItem,
      newItemTitle,
      editingItem,
      editTitle,
      newItemInput,
      editInput,
      localItems,
      completedCount,
      progressPercentage,
      addItem,
      cancelAdd,
      toggleItem,
      startEdit,
      saveEdit,
      cancelEdit,
      deleteItem,
      onReorder
    }
  }
}
</script>