<template>
  <div class="bg-gray-100 rounded-lg p-4 w-72 flex-shrink-0 max-h-full flex flex-col">
    <!-- List Header -->
    <div class="flex items-center justify-between mb-4">
      <h3 
        v-if="!editing"
        @click="startEdit"
        class="font-medium text-gray-900 cursor-pointer hover:text-gray-700"
      >
        {{ list.title }}
      </h3>
      <input
        v-else
        v-model="editTitle"
        @blur="saveTitle"
        @keyup.enter="saveTitle"
        @keyup.escape="cancelEdit"
        class="font-medium text-gray-900 bg-transparent border-none focus:outline-none focus:bg-white focus:border focus:border-blue-500 rounded px-1"
        autofocus
      />
      
      <div class="flex items-center space-x-1">
        <span class="text-sm text-gray-500">{{ list.cards.length }}</span>
        <button 
          @click="showMenu = !showMenu"
          class="text-gray-400 hover:text-gray-600 p-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Dropdown Menu -->
    <div v-if="showMenu" class="absolute bg-white shadow-lg rounded-md py-1 z-10 mt-8 right-4">
      <button 
        @click="deleteList"
        class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 w-full text-left"
      >
        Delete List
      </button>
    </div>
    
    <!-- Cards Container -->
    <div class="flex-1 overflow-y-auto space-y-3 mb-4">
      <KanbanCard
        v-for="card in list.cards"
        :key="card.id"
        :card="card"
        @update="(data) => $emit('update-card', card.id, data)"
        @delete="$emit('delete-card', card.id)"
      />
    </div>
    
    <!-- Add Card -->
    <div v-if="showAddCard" class="space-y-2">
      <textarea
        v-model="newCardTitle"
        @keyup.enter.exact="addCard"
        @keyup.escape="cancelAddCard"
        placeholder="Enter a title for this card..."
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        rows="3"
        autofocus
      ></textarea>
      <div class="flex items-center space-x-2">
        <button 
          @click="addCard"
          class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-md text-sm"
        >
          Add Card
        </button>
        <button 
          @click="cancelAddCard"
          class="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm"
        >
          Cancel
        </button>
      </div>
    </div>
    <button 
      v-else
      @click="showAddCard = true"
      class="w-full text-left text-gray-500 hover:text-gray-700 hover:bg-gray-200 rounded-md px-3 py-2 text-sm flex items-center"
    >
      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
      </svg>
      Add a card
    </button>
  </div>
</template>

<script>
import { ref } from 'vue'
import KanbanCard from './KanbanCard.vue'

export default {
  name: 'KanbanList',
  components: {
    KanbanCard
  },
  props: {
    list: {
      type: Object,
      required: true
    }
  },
  emits: ['update-list', 'delete-list', 'add-card', 'update-card', 'delete-card', 'move-card'],
  setup(props, { emit }) {
    const editing = ref(false)
    const editTitle = ref('')
    const showMenu = ref(false)
    const showAddCard = ref(false)
    const newCardTitle = ref('')
    
    const startEdit = () => {
      editing.value = true
      editTitle.value = props.list.title
    }
    
    const saveTitle = () => {
      if (editTitle.value.trim() && editTitle.value !== props.list.title) {
        emit('update-list', props.list.id, { title: editTitle.value })
      }
      editing.value = false
    }
    
    const cancelEdit = () => {
      editing.value = false
      editTitle.value = ''
    }
    
    const deleteList = () => {
      emit('delete-list', props.list.id)
      showMenu.value = false
    }
    
    const addCard = () => {
      if (!newCardTitle.value.trim()) return
      
      emit('add-card', props.list.id, {
        title: newCardTitle.value
      })
      newCardTitle.value = ''
      showAddCard.value = false
    }
    
    const cancelAddCard = () => {
      newCardTitle.value = ''
      showAddCard.value = false
    }
    
    return {
      editing,
      editTitle,
      showMenu,
      showAddCard,
      newCardTitle,
      startEdit,
      saveTitle,
      cancelEdit,
      deleteList,
      addCard,
      cancelAddCard
    }
  }
}
</script>