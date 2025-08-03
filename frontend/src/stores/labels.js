import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export const useLabelsStore = defineStore('labels', {
  state: () => ({
    labels: [],
    loading: false,
    error: null
  }),

  getters: {
    getLabelById: (state) => (id) => {
      return state.labels.find(label => label.id === id)
    },
    
    getLabelsByIds: (state) => (ids) => {
      return state.labels.filter(label => ids.includes(label.id))
    }
  },

  actions: {
    async fetchLabels() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`${API_BASE_URL}/labels/`)
        this.labels = response.data.results || response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch labels'
        console.error('Error fetching labels:', error)
      } finally {
        this.loading = false
      }
    },

    async createLabel(labelData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/labels/`, labelData)
        this.labels.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create label'
        console.error('Error creating label:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateLabel(id, labelData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.patch(`${API_BASE_URL}/labels/${id}/`, labelData)
        const index = this.labels.findIndex(l => l.id === id)
        if (index !== -1) {
          this.labels[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update label'
        console.error('Error updating label:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteLabel(id) {
      this.loading = true
      this.error = null
      
      try {
        await axios.delete(`${API_BASE_URL}/labels/${id}/`)
        this.labels = this.labels.filter(l => l.id !== id)
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to delete label'
        console.error('Error deleting label:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})