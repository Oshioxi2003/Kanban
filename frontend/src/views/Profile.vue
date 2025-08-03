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
              <span class="text-xl font-bold text-gray-900">Back to Dashboard</span>
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="md:grid md:grid-cols-3 md:gap-6">
        <!-- Sidebar -->
        <div class="md:col-span-1">
          <div class="px-4 sm:px-0">
            <h3 class="text-lg font-medium leading-6 text-gray-900">Profile Settings</h3>
            <p class="mt-1 text-sm text-gray-600">
              Update your personal information and preferences.
            </p>
          </div>
          
          <!-- Avatar -->
          <div class="mt-6">
            <div class="bg-white shadow rounded-lg p-6">
              <div class="text-center">
                <img 
                  :src="authStore.userAvatar"
                  :alt="authStore.user?.username"
                  class="mx-auto h-24 w-24 rounded-full"
                />
                <h3 class="mt-4 text-lg font-medium text-gray-900">{{ authStore.userFullName }}</h3>
                <p class="text-sm text-gray-500">@{{ authStore.user?.username }}</p>
                
                <div class="mt-4">
                  <input
                    ref="fileInput"
                    type="file"
                    accept="image/*"
                    @change="handleAvatarUpload"
                    class="hidden"
                  />
                  <button
                    @click="$refs.fileInput.click()"
                    class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                    Change Avatar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Main content -->
        <div class="mt-5 md:mt-0 md:col-span-2">
          <form @submit.prevent="handleUpdateProfile">
            <div class="shadow sm:rounded-md sm:overflow-hidden">
              <div class="px-4 py-5 bg-white space-y-6 sm:p-6">
                <!-- Success message -->
                <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
                  {{ successMessage }}
                </div>
                
                <!-- Error message -->
                <div v-if="authStore.error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                  <div v-if="typeof authStore.error === 'string'">{{ authStore.error }}</div>
                  <div v-else>
                    <div v-for="(errors, field) in authStore.error" :key="field">
                      <strong>{{ field }}:</strong> {{ errors.join(', ') }}
                    </div>
                  </div>
                </div>

                <!-- Personal Information -->
                <div>
                  <label class="text-base font-medium text-gray-900">Personal Information</label>
                  <p class="text-sm leading-5 text-gray-600">Use a permanent address where you can receive mail.</p>
                  
                  <div class="mt-6 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                    <div class="sm:col-span-3">
                      <label for="first_name" class="block text-sm font-medium text-gray-700">
                        First name
                      </label>
                      <div class="mt-1">
                        <input
                          id="first_name"
                          v-model="form.first_name"
                          name="first_name"
                          type="text"
                          class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                    </div>

                    <div class="sm:col-span-3">
                      <label for="last_name" class="block text-sm font-medium text-gray-700">
                        Last name
                      </label>
                      <div class="mt-1">
                        <input
                          id="last_name"
                          v-model="form.last_name"
                          name="last_name"
                          type="text"
                          class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                    </div>

                    <div class="sm:col-span-4">
                      <label for="display_name" class="block text-sm font-medium text-gray-700">
                        Display name
                      </label>
                      <div class="mt-1">
                        <input
                          id="display_name"
                          v-model="form.display_name"
                          name="display_name"
                          type="text"
                          class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                          placeholder="How you'd like to be called"
                        />
                      </div>
                      <p class="mt-2 text-sm text-gray-500">This will be shown to other users.</p>
                    </div>

                    <div class="sm:col-span-4">
                      <label for="email" class="block text-sm font-medium text-gray-700">
                        Email address
                      </label>
                      <div class="mt-1">
                        <input
                          id="email"
                          v-model="form.email"
                          name="email"
                          type="email"
                          class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                    </div>

                    <div class="sm:col-span-6">
                      <label for="bio" class="block text-sm font-medium text-gray-700">
                        Bio
                      </label>
                      <div class="mt-1">
                        <textarea
                          id="bio"
                          v-model="form.bio"
                          name="bio"
                          rows="3"
                          class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border border-gray-300 rounded-md"
                          placeholder="Tell us about yourself..."
                        ></textarea>
                      </div>
                      <p class="mt-2 text-sm text-gray-500">
                        Write a few sentences about yourself.
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Account Settings -->
                <div class="pt-8 border-t border-gray-200">
                  <div>
                    <h3 class="text-lg leading-6 font-medium text-gray-900">Account Settings</h3>
                    <p class="mt-1 text-sm text-gray-600">
                      Manage your account preferences.
                    </p>
                  </div>
                  
                  <div class="mt-6">
                    <fieldset>
                      <legend class="text-base font-medium text-gray-900">Notifications</legend>
                      <div class="mt-4 space-y-4">
                        <div class="flex items-start">
                          <div class="flex items-center h-5">
                            <input
                              id="email_notifications"
                              v-model="form.email_notifications"
                              name="email_notifications"
                              type="checkbox"
                              class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                            />
                          </div>
                          <div class="ml-3 text-sm">
                            <label for="email_notifications" class="font-medium text-gray-700">
                              Email notifications
                            </label>
                            <p class="text-gray-500">Get notified when someone comments on your cards.</p>
                          </div>
                        </div>
                        
                        <div class="flex items-start">
                          <div class="flex items-center h-5">
                            <input
                              id="due_date_reminders"
                              v-model="form.due_date_reminders"
                              name="due_date_reminders"
                              type="checkbox"
                              class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                            />
                          </div>
                          <div class="ml-3 text-sm">
                            <label for="due_date_reminders" class="font-medium text-gray-700">
                              Due date reminders
                            </label>
                            <p class="text-gray-500">Get reminders when your tasks are due soon.</p>
                          </div>
                        </div>
                      </div>
                    </fieldset>
                  </div>
                </div>
              </div>
              
              <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
                <button
                  type="submit"
                  :disabled="authStore.loading"
                  class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span v-if="authStore.loading">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Saving...
                  </span>
                  <span v-else>Save Changes</span>
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Profile',
  setup() {
    const authStore = useAuthStore()
    const successMessage = ref('')
    
    const form = reactive({
      first_name: '',
      last_name: '',
      email: '',
      display_name: '',
      bio: '',
      email_notifications: true,
      due_date_reminders: true
    })
    
    const initializeForm = () => {
      if (authStore.user) {
        form.first_name = authStore.user.first_name || ''
        form.last_name = authStore.user.last_name || ''
        form.email = authStore.user.email || ''
        form.display_name = authStore.user.profile?.display_name || ''
        form.bio = authStore.user.profile?.bio || ''
      }
    }
    
    const handleUpdateProfile = async () => {
      try {
        await authStore.updateProfile(form)
        successMessage.value = 'Profile updated successfully!'
        setTimeout(() => {
          successMessage.value = ''
        }, 3000)
      } catch (error) {
        console.error('Profile update error:', error)
      }
    }
    
    const handleAvatarUpload = async (event) => {
      const file = event.target.files[0]
      if (!file) return
      
      // Here you would upload the file to your storage service
      // For now, we'll just create a local URL
      const formData = new FormData()
      formData.append('avatar', file)
      
      try {
        // Replace with actual upload endpoint
        // const response = await axios.post('/api/upload-avatar/', formData)
        // await authStore.updateProfile({ avatar: response.data.url })
        
        // For demo purposes, use a local object URL
        const avatarUrl = URL.createObjectURL(file)
        await authStore.updateProfile({ avatar: avatarUrl })
        
        successMessage.value = 'Avatar updated successfully!'
        setTimeout(() => {
          successMessage.value = ''
        }, 3000)
      } catch (error) {
        console.error('Avatar upload error:', error)
      }
    }
    
    onMounted(() => {
      initializeForm()
    })
    
    return {
      authStore,
      form,
      successMessage,
      handleUpdateProfile,
      handleAvatarUpload
    }
  }
}
</script>