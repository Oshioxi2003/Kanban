import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export const useTeamsStore = defineStore('teams', {
  state: () => ({
    teams: [],
    currentTeam: null,
    members: [],
    loading: false,
    error: null
  }),

  getters: {
    getTeamById: (state) => (id) => {
      return state.teams.find(team => team.id === id)
    },
    
    ownedTeams: (state) => {
      return state.teams.filter(team => team.owner)
    },
    
    joinedTeams: (state) => {
      return state.teams.filter(team => !team.owner)
    }
  },

  actions: {
    async fetchTeams() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`${API_BASE_URL}/teams/`)
        this.teams = response.data.results || response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch teams'
        console.error('Error fetching teams:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchTeam(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`${API_BASE_URL}/teams/${id}/`)
        this.currentTeam = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch team'
        console.error('Error fetching team:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createTeam(teamData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/teams/`, teamData)
        this.teams.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create team'
        console.error('Error creating team:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateTeam(id, teamData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.patch(`${API_BASE_URL}/teams/${id}/`, teamData)
        const index = this.teams.findIndex(t => t.id === id)
        if (index !== -1) {
          this.teams[index] = response.data
        }
        if (this.currentTeam && this.currentTeam.id === id) {
          this.currentTeam = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update team'
        console.error('Error updating team:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteTeam(id) {
      this.loading = true
      this.error = null
      
      try {
        await axios.delete(`${API_BASE_URL}/teams/${id}/`)
        this.teams = this.teams.filter(t => t.id !== id)
        if (this.currentTeam && this.currentTeam.id === id) {
          this.currentTeam = null
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to delete team'
        console.error('Error deleting team:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async inviteMember(teamId, email, role = 'member') {
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/teams/${teamId}/invite_member/`, {
          email,
          role
        })
        
        // Refresh team data
        await this.fetchTeam(teamId)
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to invite member'
        console.error('Error inviting member:', error)
        throw error
      }
    },

    async removeMember(teamId, userId) {
      this.error = null
      
      try {
        await axios.post(`${API_BASE_URL}/teams/${teamId}/remove_member/`, {
          user_id: userId
        })
        
        // Refresh team data
        await this.fetchTeam(teamId)
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to remove member'
        console.error('Error removing member:', error)
        throw error
      }
    },

    async updateMemberRole(teamId, userId, role) {
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/teams/${teamId}/update_member_role/`, {
          user_id: userId,
          role
        })
        
        // Refresh team data
        await this.fetchTeam(teamId)
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to update member role'
        console.error('Error updating member role:', error)
        throw error
      }
    }
  }
})