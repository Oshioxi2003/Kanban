<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
              <span class="text-xl font-bold text-gray-900">Goals & Objectives</span>
            </router-link>
          </div>
          
          <div class="flex items-center">
            <button 
              @click="showCreateModal = true"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              New Goal
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Success/Error messages -->
      <div v-if="successMessage" class="mb-4 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
        {{ successMessage }}
      </div>
      
      <div v-if="goalsStore.error" class="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {{ goalsStore.error }}
      </div>

      <!-- Stats overview -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Active Goals</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ goalsStore.activeGoals.length }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Completed</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ goalsStore.completedGoals.length }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Overdue</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ goalsStore.overdueGoals.length }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v4"/>
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Avg. Progress</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ averageProgress }}%</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="goalsStore.loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <!-- Goals grid -->
      <div v-else-if="goalsStore.goals.length > 0" class="space-y-8">
        <!-- Active Goals -->
        <div v-if="goalsStore.activeGoals.length > 0">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Active Goals</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <GoalCard 
              v-for="goal in goalsStore.activeGoals" 
              :key="goal.id"
              :goal="goal"
              @edit="editGoal"
              @complete="completeGoal"
              @delete="deleteGoal"
              @view-details="viewGoalDetails"
            />
          </div>
        </div>

        <!-- Completed Goals -->
        <div v-if="goalsStore.completedGoals.length > 0">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Completed Goals</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <GoalCard 
              v-for="goal in goalsStore.completedGoals" 
              :key="goal.id"
              :goal="goal"
              @edit="editGoal"
              @reopen="reopenGoal"
              @delete="deleteGoal"
              @view-details="viewGoalDetails"
            />
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No goals</h3>
        <p class="mt-1 text-sm text-gray-500">Get started by creating a new goal to track your progress.</p>
        <div class="mt-6">
          <button 
            @click="showCreateModal = true"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
          >
            Create Goal
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Goal Modal -->
    <GoalModal
      v-if="showCreateModal || editingGoal"
      :goal="editingGoal"
      @close="closeModal"
      @saved="onGoalSaved"
    />

    <!-- Goal Details Modal -->
    <GoalDetailsModal
      v-if="selectedGoal"
      :goal="selectedGoal"
      @close="selectedGoal = null"
      @updated="onGoalUpdated"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useGoalsStore } from '../stores/goals'
import GoalCard from '../components/GoalCard.vue'
import GoalModal from '../components/GoalModal.vue'
import GoalDetailsModal from '../components/GoalDetailsModal.vue'

export default {
  name: 'Goals',
  components: {
    GoalCard,
    GoalModal,
    GoalDetailsModal
  },
  setup() {
    const goalsStore = useGoalsStore()
    const showCreateModal = ref(false)
    const editingGoal = ref(null)
    const selectedGoal = ref(null)
    const successMessage = ref('')
    
    const averageProgress = computed(() => {
      const activeGoals = goalsStore.activeGoals
      if (activeGoals.length === 0) return 0
      
      const totalProgress = activeGoals.reduce((sum, goal) => sum + goal.progress_percentage, 0)
      return Math.round(totalProgress / activeGoals.length)
    })
    
    const editGoal = (goal) => {
      editingGoal.value = goal
    }
    
    const closeModal = () => {
      showCreateModal.value = false
      editingGoal.value = null
    }
    
    const onGoalSaved = (goal) => {
      closeModal()
      successMessage.value = editingGoal.value ? 'Goal updated successfully!' : 'Goal created successfully!'
      setTimeout(() => {
        successMessage.value = ''
      }, 3000)
    }
    
    const completeGoal = async (goal) => {
      try {
        await goalsStore.completeGoal(goal.id)
        successMessage.value = 'Goal completed! Congratulations! 🎉'
        setTimeout(() => {
          successMessage.value = ''
        }, 3000)
      } catch (error) {
        console.error('Failed to complete goal:', error)
      }
    }
    
    const reopenGoal = async (goal) => {
      try {
        await goalsStore.reopenGoal(goal.id)
        successMessage.value = 'Goal reopened successfully!'
        setTimeout(() => {
          successMessage.value = ''
        }, 3000)
      } catch (error) {
        console.error('Failed to reopen goal:', error)
      }
    }
    
    const deleteGoal = async (goal) => {
      if (confirm(`Are you sure you want to delete the goal "${goal.title}"? This action cannot be undone.`)) {
        try {
          await goalsStore.deleteGoal(goal.id)
          successMessage.value = 'Goal deleted successfully!'
          setTimeout(() => {
            successMessage.value = ''
          }, 3000)
        } catch (error) {
          console.error('Failed to delete goal:', error)
        }
      }
    }
    
    const viewGoalDetails = (goal) => {
      selectedGoal.value = goal
    }
    
    const onGoalUpdated = () => {
      goalsStore.fetchGoals()
    }
    
    onMounted(() => {
      goalsStore.fetchGoals()
    })
    
    return {
      goalsStore,
      showCreateModal,
      editingGoal,
      selectedGoal,
      successMessage,
      averageProgress,
      editGoal,
      closeModal,
      onGoalSaved,
      completeGoal,
      reopenGoal,
      deleteGoal,
      viewGoalDetails,
      onGoalUpdated
    }
  }
}
</script>