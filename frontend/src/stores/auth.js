import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    tokens: {
      access: null,
      refresh: null
    },
    isAuthenticated: false,
    loading: false,
    error: null
  }),

  getters: {
    isLoggedIn: (state) => state.isAuthenticated && state.user !== null,
    
    userFullName: (state) => {
      if (!state.user) return ''
      return state.user.profile?.display_name || 
             state.user.full_name || 
             `${state.user.first_name} ${state.user.last_name}`.trim() ||
             state.user.username
    },
    
    userAvatar: (state) => {
      return state.user?.profile?.avatar || `https://ui-avatars.com/api/?name=${state.user?.username || 'User'}&background=3B82F6&color=fff`
    }
  },

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/login/`, credentials)
        
        this.user = response.data.user
        this.tokens = response.data.tokens
        this.isAuthenticated = true
        
        // Store tokens in localStorage
        localStorage.setItem('access_token', this.tokens.access)
        localStorage.setItem('refresh_token', this.tokens.refresh)
        localStorage.setItem('user', JSON.stringify(this.user))
        
        // Set default axios header
        this.setAuthHeader()
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Login failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/register/`, userData)
        
        this.user = response.data.user
        this.tokens = response.data.tokens
        this.isAuthenticated = true
        
        // Store tokens in localStorage
        localStorage.setItem('access_token', this.tokens.access)
        localStorage.setItem('refresh_token', this.tokens.refresh)
        localStorage.setItem('user', JSON.stringify(this.user))
        
        // Set default axios header
        this.setAuthHeader()
        
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Registration failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async logout() {
      try {
        if (this.tokens.refresh) {
          await axios.post(`${API_BASE_URL}/auth/logout/`, {
            refresh_token: this.tokens.refresh
          })
        }
      } catch (error) {
        console.error('Logout error:', error)
      }
      
      this.user = null
      this.tokens = { access: null, refresh: null }
      this.isAuthenticated = false
      
      // Remove from localStorage
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      
      // Remove axios header
      delete axios.defaults.headers.common['Authorization']
    },
    
    async refreshToken() {
      if (!this.tokens.refresh) {
        this.logout()
        return false
      }
      
      try {
        const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
          refresh: this.tokens.refresh
        })
        
        this.tokens.access = response.data.access
        localStorage.setItem('access_token', this.tokens.access)
        this.setAuthHeader()
        
        return true
      } catch (error) {
        console.error('Token refresh failed:', error)
        this.logout()
        return false
      }
    },
    
    async updateProfile(profileData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.patch(`${API_BASE_URL}/auth/update_profile/`, profileData)
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(this.user))
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Profile update failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchProfile() {
      try {
        const response = await axios.get(`${API_BASE_URL}/auth/profile/`)
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(this.user))
        return response.data
      } catch (error) {
        console.error('Failed to fetch profile:', error)
        this.logout()
        throw error
      }
    },
    
    initializeAuth() {
      const accessToken = localStorage.getItem('access_token')
      const refreshToken = localStorage.getItem('refresh_token')
      const userData = localStorage.getItem('user')
      
      if (accessToken && refreshToken && userData) {
        this.tokens = {
          access: accessToken,
          refresh: refreshToken
        }
        this.user = JSON.parse(userData)
        this.isAuthenticated = true
        this.setAuthHeader()
      }
    },
    
    setAuthHeader() {
      if (this.tokens.access) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.tokens.access}`
      }
    }
  }
})

// Axios interceptor for token refresh
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const authStore = useAuthStore()
      const success = await authStore.refreshToken()
      
      if (success) {
        originalRequest.headers['Authorization'] = `Bearer ${authStore.tokens.access}`
        return axios(originalRequest)
      }
    }
    
    return Promise.reject(error)
  }
)