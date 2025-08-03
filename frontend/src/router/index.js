import { createRouter, createWebHistory } from 'vue-router'
import { requireAuth, redirectIfAuthenticated } from './auth'

// Views
import Dashboard from '../views/Dashboard.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'
import Labels from '../views/Labels.vue'
import BoardList from '../views/BoardList.vue'
import BoardDetail from '../views/BoardDetail.vue'
import Timeline from '../views/Timeline.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Public routes
    {
      path: '/login',
      name: 'login',
      component: Login,
      beforeEnter: redirectIfAuthenticated
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      beforeEnter: redirectIfAuthenticated
    },
    
    // Protected routes
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard,
      beforeEnter: requireAuth
    },
    {
      path: '/boards',
      name: 'boards',
      component: BoardList,
      beforeEnter: requireAuth
    },
    {
      path: '/board/:id',
      name: 'board',
      component: BoardDetail,
      props: true,
      beforeEnter: requireAuth
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      beforeEnter: requireAuth
    },
    {
      path: '/labels',
      name: 'labels',
      component: Labels,
      beforeEnter: requireAuth
    },
    {
      path: '/timeline',
      name: 'timeline',
      component: Timeline,
      beforeEnter: requireAuth
    },
    {
      path: '/goals',
      name: 'goals',
      component: () => import('../views/Goals.vue'),
      beforeEnter: requireAuth
    },
    {
      path: '/reports',
      name: 'reports',
      component: () => import('../views/Reports.vue'),
      beforeEnter: requireAuth
    },
    {
      path: '/teams',
      name: 'teams',
      component: () => import('../views/Teams.vue'),
      beforeEnter: requireAuth
    },
    {
      path: '/eisenhower',
      name: 'eisenhower',
      component: () => import('../views/EisenhowerMatrix.vue'),
      beforeEnter: requireAuth
    },
    
    // Redirect unknown routes
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

export default router