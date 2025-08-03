<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
              <span class="text-xl font-bold text-gray-900 dark:text-white">Team Management</span>
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
              Create Team
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
      
      <div v-if="teamsStore.error" class="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {{ teamsStore.error }}
      </div>

      <!-- Team Statistics -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">My Teams</dt>
                  <dd class="text-lg font-medium text-gray-900 dark:text-white">{{ teamsStore.teams.length }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">Teams I Own</dt>
                  <dd class="text-lg font-medium text-gray-900 dark:text-white">{{ teamsStore.ownedTeams.length }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">Teams I Joined</dt>
                  <dd class="text-lg font-medium text-gray-900 dark:text-white">{{ teamsStore.joinedTeams.length }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="teamsStore.loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <!-- Teams grid -->
      <div v-else-if="teamsStore.teams.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <TeamCard 
          v-for="team in teamsStore.teams" 
          :key="team.id"
          :team="team"
          @edit="editTeam"
          @delete="deleteTeam"
          @view-details="viewTeamDetails"
        />
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">No teams</h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Get started by creating a new team or joining an existing one.</p>
        <div class="mt-6">
          <button 
            @click="showCreateModal = true"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
          >
            Create Team
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Team Modal -->
    <TeamModal
      v-if="showCreateModal || editingTeam"
      :team="editingTeam"
      @close="closeModal"
      @saved="onTeamSaved"
    />

    <!-- Team Details Modal -->
    <TeamDetailsModal
      v-if="selectedTeam"
      :team="selectedTeam"
      @close="selectedTeam = null"
      @updated="onTeamUpdated"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useTeamsStore } from '../stores/teams'
import TeamCard from '../components/TeamCard.vue'
import TeamModal from '../components/TeamModal.vue'
import TeamDetailsModal from '../components/TeamDetailsModal.vue'

export default {
  name: 'Teams',
  components: {
    TeamCard,
    TeamModal,
    TeamDetailsModal
  },
  setup() {
    const teamsStore = useTeamsStore()
    const showCreateModal = ref(false)
    const editingTeam = ref(null)
    const selectedTeam = ref(null)
    const successMessage = ref('')
    
    const editTeam = (team) => {
      editingTeam.value = team
    }
    
    const closeModal = () => {
      showCreateModal.value = false
      editingTeam.value = null
    }
    
    const onTeamSaved = (team) => {
      closeModal()
      successMessage.value = editingTeam.value ? 'Team updated successfully!' : 'Team created successfully!'
      setTimeout(() => {
        successMessage.value = ''
      }, 3000)
    }
    
    const deleteTeam = async (team) => {
      if (confirm(`Are you sure you want to delete the team "${team.name}"? This action cannot be undone.`)) {
        try {
          await teamsStore.deleteTeam(team.id)
          successMessage.value = 'Team deleted successfully!'
          setTimeout(() => {
            successMessage.value = ''
          }, 3000)
        } catch (error) {
          console.error('Failed to delete team:', error)
        }
      }
    }
    
    const viewTeamDetails = (team) => {
      selectedTeam.value = team
    }
    
    const onTeamUpdated = () => {
      teamsStore.fetchTeams()
    }
    
    onMounted(() => {
      teamsStore.fetchTeams()
    })
    
    return {
      teamsStore,
      showCreateModal,
      editingTeam,
      selectedTeam,
      successMessage,
      editTeam,
      closeModal,
      onTeamSaved,
      deleteTeam,
      viewTeamDetails,
      onTeamUpdated
    }
  }
}
</script>