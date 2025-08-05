import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL}/api` : 'http://localhost:8000/api'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API functions
export const boardsAPI = {
  getAll: () => api.get('/boards/'),
  get: (id) => api.get(`/boards/${id}/`),
  create: (data) => api.post('/boards/', data),
  update: (id, data) => api.patch(`/boards/${id}/`, data),
  delete: (id) => api.delete(`/boards/${id}/`),
  duplicate: (id) => api.post(`/boards/${id}/duplicate/`)
}

export const listsAPI = {
  getAll: () => api.get('/lists/'),
  get: (id) => api.get(`/lists/${id}/`),
  create: (data) => api.post('/lists/', data),
  update: (id, data) => api.patch(`/lists/${id}/`, data),
  delete: (id) => api.delete(`/lists/${id}/`),
  reorder: (id, position) => api.post(`/lists/${id}/reorder/`, { position })
}

export const cardsAPI = {
  getAll: () => api.get('/cards/'),
  get: (id) => api.get(`/cards/${id}/`),
  create: (data) => api.post('/cards/', data),
  update: (id, data) => api.patch(`/cards/${id}/`, data),
  delete: (id) => api.delete(`/cards/${id}/`),
  move: (id, listId, position) => api.post(`/cards/${id}/move/`, { 
    list_id: listId, 
    position 
  })
}

export const commentsAPI = {
  getAll: () => api.get('/comments/'),
  create: (data) => api.post('/comments/', data),
  update: (id, data) => api.patch(`/comments/${id}/`, data),
  delete: (id) => api.delete(`/comments/${id}/`)
}

export const usersAPI = {
  getAll: () => api.get('/users/')
}

export default api