<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900">My Boards</h1>
      <button 
        @click="showCreateModal = true"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
        </svg>
        Create Board
      </button>
    </div>

    <!-- Loading -->
    <div v-if="kanbanStore.loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- Error -->
    <div v-else-if="kanbanStore.error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
      {{ kanbanStore.error }}
    </div>

    <!-- Empty state -->
    <div v-else-if="!kanbanStore.boards.length" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No boards</h3>
      <p class="mt-1 text-sm text-gray-500">Get started by creating a new board.</p>
      <div class="mt-6">
        <button 
          @click="showCreateModal = true"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
        >
          Create Board
        </button>
      </div>
    </div>

    <!-- Boards Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div 
        v-for="board in kanbanStore.boards" 
        :key="board.id"
        class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
        @click="$router.push(`/board/${board.id}`)"
      >
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ board.title }}</h3>
          <p class="text-gray-600 text-sm mb-4 line-clamp-2">{{ board.description || 'No description' }}</p>
          
          <div class="flex items-center justify-between text-sm text-gray-500">
            <div class="flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              {{ formatDate(board.created_at) }}
            </div>
            <div class="flex items-center space-x-3">
              <span>{{ board.lists_count || 0 }} lists</span>
              <span>{{ board.cards_count || 0 }} cards</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Board Modal -->
    <CreateBoardModal 
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="onBoardCreated"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useKanbanStore } from '../stores/kanban'
import CreateBoardModal from '../components/CreateBoardModal.vue'

export default {
  name: 'BoardList',
  components: {
    CreateBoardModal
  },
  setup() {
    const kanbanStore = useKanbanStore()
    const showCreateModal = ref(false)

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const onBoardCreated = (board) => {
      showCreateModal.value = false
      // Navigate to new board
      window.location.href = `/board/${board.id}`
    }

    onMounted(() => {
      kanbanStore.fetchBoards()
    })

    return {
      kanbanStore,
      showCreateModal,
      formatDate,
      onBoardCreated
    }
  }
}
</script>