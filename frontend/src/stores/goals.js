import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export const useGoalsStore = defineStore('goals', {
  state: () => ({
    goals: [],
    currentGoal: null,
    loading: false,
    error: null
  }),

  getters: {
    getGoalById: (state) => (id) => {
      return state.goals.find(goal => goal.id === id)
    },
    
    activeGoals: (state) => {
      return state.goals.filter(goal => !goal.is_completed)
    },
    
    completedGoals: (state) => {
      return state.goals.filter(goal => goal.is_completed)
    },
    
    overdueGoals: (state) => {
      return state.goals.filter(goal => 
        goal.is_overdue && !goal.is_completed
      )
    },
    
    goalsByProgress: (state) => {
      return state.goals.reduce((groups, goal) => {
        const progress = goal.progress_percentage
        let category
        
        if (progress === 0) category = 'not_started'
        else if (progress < 50) category = 'in_progress'
        else if (progress < 100) category = 'almost_done'
        else category = 'completed'
        
        if (!groups[category]) groups[category] = []
        groups[category].push(goal)
        
        return groups
      }, {})
    }
  },

  actions: {
    async fetchGoals() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`${API_BASE_URL}/goals/`)
        this.goals = response.data.results || response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch goals'
        console.error('Error fetching goals:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchGoal(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`${API_BASE_URL}/goals/${id}/`)
        this.currentGoal = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch goal'
        console.error('Error fetching goal:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createGoal(goalData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/goals/`, goalData)
        this.goals.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create goal'
        console.error('Error creating goal:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateGoal(id, goalData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.patch(`${API_BASE_URL}/goals/${id}/`, goalData)
        const index = this.goals.findIndex(g => g.id === id)
        if (index !== -1) {
          this.goals[index] = response.data
        }
        if (this.currentGoal && this.currentGoal.id === id) {
          this.currentGoal = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update goal'
        console.error('Error updating goal:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteGoal(id) {
      this.loading = true
      this.error = null
      
      try {
        await axios.delete(`${API_BASE_URL}/goals/${id}/`)
        this.goals = this.goals.filter(g => g.id !== id)
        if (this.currentGoal && this.currentGoal.id === id) {
          this.currentGoal = null
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to delete goal'
        console.error('Error deleting goal:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async completeGoal(id) {
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/goals/${id}/complete/`)
        const index = this.goals.findIndex(g => g.id === id)
        if (index !== -1) {
          this.goals[index] = response.data
        }
        if (this.currentGoal && this.currentGoal.id === id) {
          this.currentGoal = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to complete goal'
        console.error('Error completing goal:', error)
        throw error
      }
    },

    async reopenGoal(id) {
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/goals/${id}/reopen/`)
        const index = this.goals.findIndex(g => g.id === id)
        if (index !== -1) {
          this.goals[index] = response.data
        }
        if (this.currentGoal && this.currentGoal.id === id) {
          this.currentGoal = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to reopen goal'
        console.error('Error reopening goal:', error)
        throw error
      }
    },

    async linkCardToGoal(goalId, cardId) {
      this.error = null
      
      try {
        await axios.post(`${API_BASE_URL}/goals/${goalId}/link_card/`, {
          card_id: cardId
        })
        
        // Refresh the goal to get updated progress
        await this.fetchGoal(goalId)
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to link card to goal'
        console.error('Error linking card to goal:', error)
        throw error
      }
    },

    async unlinkCardFromGoal(goalId, cardId) {
      this.error = null
      
      try {
        await axios.post(`${API_BASE_URL}/goals/${goalId}/unlink_card/`, {
          card_id: cardId
        })
        
        // Refresh the goal to get updated progress
        await this.fetchGoal(goalId)
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to unlink card from goal'
        console.error('Error unlinking card from goal:', error)
        throw error
      }
    }
  }
})