<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-medium text-gray-900 dark:text-white">Theme Customization</h3>
      <button
        @click="$emit('close')"
        class="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>
    
    <!-- Theme Mode Selection -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
        Theme Mode
      </label>
      <div class="grid grid-cols-3 gap-3">
        <button
          @click="themeStore.setTheme('light')"
          class="flex flex-col items-center p-3 border-2 rounded-lg transition-colors"
          :class="themeStore.theme === 'light' 
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
        >
          <svg class="w-6 h-6 text-yellow-500 mb-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"/>
          </svg>
          <span class="text-sm font-medium text-gray-900 dark:text-white">Light</span>
        </button>
        
        <button
          @click="themeStore.setTheme('dark')"
          class="flex flex-col items-center p-3 border-2 rounded-lg transition-colors"
          :class="themeStore.theme === 'dark' 
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
        >
          <svg class="w-6 h-6 text-blue-400 mb-2" fill="currentColor" viewBox="0 0 20 20">
            <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/>
          </svg>
          <span class="text-sm font-medium text-gray-900 dark:text-white">Dark</span>
        </button>
        
        <button
          @click="themeStore.setTheme(themeStore.systemPreference)"
          class="flex flex-col items-center p-3 border-2 rounded-lg transition-colors"
          :class="!localStorage.getItem('theme')
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
        >
          <svg class="w-6 h-6 text-gray-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
          <span class="text-sm font-medium text-gray-900 dark:text-white">System</span>
        </button>
      </div>
    </div>
    
    <!-- Primary Color Selection -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
        Primary Color
      </label>
      <div class="grid grid-cols-4 gap-3">
        <button
          v-for="color in themeStore.availableColors"
          :key="color.value"
          @click="themeStore.setPrimaryColor(color.value)"
          class="group relative w-full h-12 rounded-lg border-2 transition-all duration-200"
          :class="themeStore.primaryColor === color.value 
            ? 'border-gray-400 dark:border-gray-500 ring-2 ring-offset-2 ring-gray-400 dark:ring-offset-gray-800' 
            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
          :style="{ backgroundColor: color.value }"
        >
          <span 
            v-if="themeStore.primaryColor === color.value"
            class="absolute inset-0 flex items-center justify-center"
          >
            <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          </span>
          <span class="sr-only">{{ color.name }}</span>
        </button>
      </div>
    </div>
    
    <!-- Custom Color Input -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
        Custom Primary Color
      </label>
      <div class="flex items-center space-x-3">
        <input
          v-model="customColor"
          type="color"
          class="w-12 h-10 border border-gray-300 dark:border-gray-600 rounded-lg cursor-pointer"
        />
        <input
          v-model="customColor"
          type="text"
          placeholder="#3B82F6"
          class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          @click="applyCustomColor"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Apply
        </button>
      </div>
    </div>
    
    <!-- Preview Section -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
        Preview
      </label>
      <div class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-900">
        <div class="space-y-3">
          <!-- Button preview -->
          <button 
            class="px-4 py-2 rounded-md text-white font-medium"
            :style="{ backgroundColor: themeStore.primaryColor }"
          >
            Primary Button
          </button>
          
          <!-- Card preview -->
          <div class="bg-white dark:bg-gray-800 p-3 rounded-lg border border-gray-200 dark:border-gray-700">
            <h4 class="font-medium text-gray-900 dark:text-white">Sample Card</h4>
            <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">
              This is how your content will look with the selected theme.
            </p>
            <div class="mt-2">
              <span 
                class="inline-block w-3 h-3 rounded-full"
                :style="{ backgroundColor: themeStore.primaryColor }"
              ></span>
              <span class="ml-2 text-xs text-gray-500 dark:text-gray-400">Accent color</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Action Buttons -->
    <div class="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
      <button
        @click="themeStore.resetTheme()"
        class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500"
      >
        Reset to Default
      </button>
      
      <div class="flex space-x-3">
        <button
          @click="exportTheme"
          class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Export Theme
        </button>
        <button
          @click="$emit('close')"
          class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Done
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useThemeStore } from '../stores/theme'

export default {
  name: 'ThemeCustomizer',
  emits: ['close'],
  setup() {
    const themeStore = useThemeStore()
    const customColor = ref('#3B82F6')
    
    const applyCustomColor = () => {
      if (isValidHexColor(customColor.value)) {
        themeStore.setPrimaryColor(customColor.value)
      }
    }
    
    const isValidHexColor = (hex) => {
      return /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(hex)
    }
    
    const exportTheme = () => {
      const themeConfig = themeStore.exportTheme()
      const dataStr = JSON.stringify(themeConfig, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      
      const link = document.createElement('a')
      link.href = URL.createObjectURL(dataBlob)
      link.download = 'kanban-theme.json'
      link.click()
      
      URL.revokeObjectURL(link.href)
    }
    
    onMounted(() => {
      customColor.value = themeStore.primaryColor
    })
    
    return {
      themeStore,
      customColor,
      applyCustomColor,
      exportTheme
    }
  }
}
</script>