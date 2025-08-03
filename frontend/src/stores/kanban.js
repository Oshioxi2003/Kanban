import { defineStore } from 'pinia'
import { boardsAPI, listsAPI, cardsAPI, commentsAPI } from '../services/api'

export const useKanbanStore = defineStore('kanban', {
  state: () => ({
    boards: [],
    currentBoard: null,
    loading: false,
    error: null
  }),

  getters: {
    getBoardById: (state) => (id) => {
      return state.boards.find(board => board.id === id)
    },
    
    getListsByBoard: (state) => (boardId) => {
      const board = state.getBoardById(boardId)
      return board ? board.lists : []
    },
    
    getCardsByList: (state) => (listId) => {
      if (!state.currentBoard) return []
      const list = state.currentBoard.lists.find(l => l.id === listId)
      return list ? list.cards : []
    }
  },

  actions: {
    async fetchBoards() {
      this.loading = true
      this.error = null
      try {
        const response = await boardsAPI.getAll()
        this.boards = response.data.results || response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch boards'
        console.error('Error fetching boards:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchBoard(id) {
      this.loading = true
      this.error = null
      try {
        const response = await boardsAPI.get(id)
        this.currentBoard = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch board'
        console.error('Error fetching board:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createBoard(boardData) {
      this.loading = true
      this.error = null
      try {
        const response = await boardsAPI.create(boardData)
        this.boards.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create board'
        console.error('Error creating board:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateBoard(id, boardData) {
      this.loading = true
      this.error = null
      try {
        const response = await boardsAPI.update(id, boardData)
        const index = this.boards.findIndex(b => b.id === id)
        if (index !== -1) {
          this.boards[index] = response.data
        }
        if (this.currentBoard && this.currentBoard.id === id) {
          this.currentBoard = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update board'
        console.error('Error updating board:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteBoard(id) {
      this.loading = true
      this.error = null
      try {
        await boardsAPI.delete(id)
        this.boards = this.boards.filter(b => b.id !== id)
        if (this.currentBoard && this.currentBoard.id === id) {
          this.currentBoard = null
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to delete board'
        console.error('Error deleting board:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createList(listData) {
      this.error = null
      try {
        const response = await listsAPI.create(listData)
        if (this.currentBoard) {
          this.currentBoard.lists.push(response.data)
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create list'
        console.error('Error creating list:', error)
        throw error
      }
    },

    async updateList(id, listData) {
      this.error = null
      try {
        const response = await listsAPI.update(id, listData)
        if (this.currentBoard) {
          const listIndex = this.currentBoard.lists.findIndex(l => l.id === id)
          if (listIndex !== -1) {
            this.currentBoard.lists[listIndex] = { ...this.currentBoard.lists[listIndex], ...response.data }
          }
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update list'
        console.error('Error updating list:', error)
        throw error
      }
    },

    async deleteList(id) {
      this.error = null
      try {
        await listsAPI.delete(id)
        if (this.currentBoard) {
          this.currentBoard.lists = this.currentBoard.lists.filter(l => l.id !== id)
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to delete list'
        console.error('Error deleting list:', error)
        throw error
      }
    },

    async createCard(cardData) {
      this.error = null
      try {
        const response = await cardsAPI.create(cardData)
        if (this.currentBoard) {
          const list = this.currentBoard.lists.find(l => l.id === cardData.list)
          if (list) {
            list.cards.push(response.data)
          }
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create card'
        console.error('Error creating card:', error)
        throw error
      }
    },

    async updateCard(id, cardData) {
      this.error = null
      try {
        const response = await cardsAPI.update(id, cardData)
        if (this.currentBoard) {
          // Find and update card across all lists
          for (const list of this.currentBoard.lists) {
            const cardIndex = list.cards.findIndex(c => c.id === id)
            if (cardIndex !== -1) {
              list.cards[cardIndex] = { ...list.cards[cardIndex], ...response.data }
              break
            }
          }
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update card'
        console.error('Error updating card:', error)
        throw error
      }
    },

    async deleteCard(id) {
      this.error = null
      try {
        await cardsAPI.delete(id)
        if (this.currentBoard) {
          // Remove card from all lists
          for (const list of this.currentBoard.lists) {
            list.cards = list.cards.filter(c => c.id !== id)
          }
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to delete card'
        console.error('Error deleting card:', error)
        throw error
      }
    },

    async moveCard(cardId, newListId, newPosition) {
      this.error = null
      try {
        const response = await cardsAPI.move(cardId, newListId, newPosition)
        
        // Update local state
        if (this.currentBoard) {
          // Remove card from current list
          let movedCard = null
          for (const list of this.currentBoard.lists) {
            const cardIndex = list.cards.findIndex(c => c.id === cardId)
            if (cardIndex !== -1) {
              movedCard = list.cards.splice(cardIndex, 1)[0]
              break
            }
          }
          
          // Add card to new list
          if (movedCard) {
            const newList = this.currentBoard.lists.find(l => l.id === newListId)
            if (newList) {
              movedCard.list = newListId
              newList.cards.splice(newPosition, 0, movedCard)
            }
          }
        }
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to move card'
        console.error('Error moving card:', error)
        throw error
      }
    }
  }
})