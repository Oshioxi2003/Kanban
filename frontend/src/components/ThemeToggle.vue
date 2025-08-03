<template>
  <div class="flex items-center space-x-2">
    <!-- Theme toggle button -->
    <button
      @click="themeStore.toggleTheme()"
      class="relative inline-flex items-center justify-center w-10 h-6 bg-gray-200 dark:bg-gray-700 rounded-full transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-gray-800"
      :class="themeStore.isDarkMode ? 'bg-blue-600' : 'bg-gray-200'"
    >
      <span class="sr-only">Toggle dark mode</span>
      
      <!-- Toggle circle -->
      <div
        class="absolute w-4 h-4 bg-white rounded-full shadow-sm transform transition-transform duration-200 ease-in-out"
        :class="themeStore.isDarkMode ? 'translate-x-4' : 'translate-x-0'"
      >
        <!-- Sun icon (light mode) -->
        <svg
          v-if="!themeStore.isDarkMode"
          class="w-3 h-3 text-yellow-500 absolute top-0.5 left-0.5"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fill-rule="evenodd"
            d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
            clip-rule="evenodd"
          />
        </svg>
        
        <!-- Moon icon (dark mode) -->
        <svg
          v-else
          class="w-3 h-3 text-blue-400 absolute top-0.5 left-0.5"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
        </svg>
      </div>
    </button>
    
    <!-- Theme label (optional) -->
    <span v-if="showLabel" class="text-sm text-gray-600 dark:text-gray-300">
      {{ themeStore.isDarkMode ? 'Dark' : 'Light' }}
    </span>
  </div>
</template>

<script>
import { useThemeStore } from '../stores/theme'

export default {
  name: 'ThemeToggle',
  props: {
    showLabel: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const themeStore = useThemeStore()
    
    return {
      themeStore
    }
  }
}
</script>