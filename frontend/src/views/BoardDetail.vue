<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button 
            @click="$router.push('/')"
            class="text-gray-500 hover:text-gray-700"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          <h1 v-if="board" class="text-xl font-semibold text-gray-900">{{ board.title }}</h1>
          <div v-else class="h-6 bg-gray-200 rounded w-48 animate-pulse"></div>
        </div>
        
        <div class="flex items-center space-x-3">
          <button 
            @click="showAddList = true"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
          >
            Add List
          </button>
          <button class="text-gray-500 hover:text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Board Content -->
    <div class="flex-1 overflow-hidden">
      <div v-if="loading" class="flex justify-center items-center h-full">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      
      <div v-else-if="error" class="p-6">
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {{ error }}
        </div>
      </div>
      
      <div v-else-if="board" class="h-full overflow-x-auto">
        <div class="flex space-x-4 p-6 h-full min-w-max">
          <!-- Lists -->
          <KanbanList
            v-for="list in board.lists"
            :key="list.id"
            :list="list"
            @update-list="updateList"
            @delete-list="deleteList"
            @add-card="addCard"
            @update-card="updateCard"
            @delete-card="deleteCard"
            @move-card="moveCard"
          />
          
          <!-- Add List Button -->
          <div class="flex-shrink-0">
            <div v-if="showAddList" class="bg-white rounded-lg shadow-sm border p-4 w-72">
              <input
                v-model="newListTitle"
                @keyup.enter="createList"
                @keyup.escape="showAddList = false"
                placeholder="Enter list title..."
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                autofocus
              />
              <div class="flex items-center space-x-2 mt-3">
                <button 
                  @click="createList"
                  class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-md text-sm"
                >
                  Add List
                </button>
                <button 
                  @click="showAddList = false"
                  class="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm"
                >
                  Cancel
                </button>
              </div>
            </div>
            <button 
              v-else
              @click="showAddList = true"
              class="bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-lg p-4 w-72 text-left border-2 border-dashed border-gray-300"
            >
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                </svg>
                Add another list
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useKanbanStore } from '../stores/kanban'
import KanbanList from '../components/KanbanList.vue'

export default {
  name: 'BoardDetail',
  components: {
    KanbanList
  },
  setup() {
    const route = useRoute()
    const kanbanStore = useKanbanStore()
    
    const showAddList = ref(false)
    const newListTitle = ref('')
    
    const board = computed(() => kanbanStore.currentBoard)
    const loading = computed(() => kanbanStore.loading)
    const error = computed(() => kanbanStore.error)
    
    const createList = async () => {
      if (!newListTitle.value.trim()) return
      
      try {
        await kanbanStore.createList({
          title: newListTitle.value,
          board: board.value.id
        })
        newListTitle.value = ''
        showAddList.value = false
      } catch (err) {
        console.error('Failed to create list:', err)
      }
    }
    
    const updateList = async (listId, data) => {
      try {
        await kanbanStore.updateList(listId, data)
      } catch (err) {
        console.error('Failed to update list:', err)
      }
    }
    
    const deleteList = async (listId) => {
      if (confirm('Are you sure you want to delete this list?')) {
        try {
          await kanbanStore.deleteList(listId)
        } catch (err) {
          console.error('Failed to delete list:', err)
        }
      }
    }
    
    const addCard = async (listId, cardData) => {
      try {
        await kanbanStore.createCard({
          ...cardData,
          list: listId
        })
      } catch (err) {
        console.error('Failed to create card:', err)
      }
    }
    
    const updateCard = async (cardId, data) => {
      try {
        await kanbanStore.updateCard(cardId, data)
      } catch (err) {
        console.error('Failed to update card:', err)
      }
    }
    
    const deleteCard = async (cardId) => {
      if (confirm('Are you sure you want to delete this card?')) {
        try {
          await kanbanStore.deleteCard(cardId)
        } catch (err) {
          console.error('Failed to delete card:', err)
        }
      }
    }
    
    const moveCard = async (cardId, newListId, newPosition) => {
      try {
        await kanbanStore.moveCard(cardId, newListId, newPosition)
      } catch (err) {
        console.error('Failed to move card:', err)
      }
    }
    
    onMounted(() => {
      kanbanStore.fetchBoard(route.params.id)
    })
    
    return {
      board,
      loading,
      error,
      showAddList,
      newListTitle,
      createList,
      updateList,
      deleteList,
      addCard,
      updateCard,
      deleteCard,
      moveCard
    }
  }
}
</script>