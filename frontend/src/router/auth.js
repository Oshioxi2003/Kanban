import { useAuthStore } from '../stores/auth'

export function requireAuth(to, from, next) {
  const authStore = useAuthStore()
  
  if (!authStore.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
}

export function redirectIfAuthenticated(to, from, next) {
  const authStore = useAuthStore()
  
  if (authStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
}