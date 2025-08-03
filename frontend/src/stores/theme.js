import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    isDarkMode: false,
    primaryColor: '#3B82F6', // Blue
    accentColor: '#10B981', // Green
    theme: 'light',
    
    // Available theme colors
    availableColors: [
      { name: 'Blue', value: '#3B82F6', class: 'blue' },
      { name: 'Purple', value: '#8B5CF6', class: 'purple' },
      { name: 'Green', value: '#10B981', class: 'green' },
      { name: 'Red', value: '#EF4444', class: 'red' },
      { name: 'Orange', value: '#F97316', class: 'orange' },
      { name: 'Pink', value: '#EC4899', class: 'pink' },
      { name: 'Indigo', value: '#6366F1', class: 'indigo' },
      { name: 'Cyan', value: '#06B6D4', class: 'cyan' }
    ],
    
    // System preference
    systemPreference: 'light'
  }),

  getters: {
    currentTheme: (state) => {
      return state.isDarkMode ? 'dark' : 'light'
    },
    
    getCurrentColor: (state) => {
      return state.availableColors.find(color => color.value === state.primaryColor) || state.availableColors[0]
    },
    
    isDarkModeEnabled: (state) => {
      return state.isDarkMode
    }
  },

  actions: {
    initializeTheme() {
      // Check for saved theme preference
      const savedTheme = localStorage.getItem('theme')
      const savedColor = localStorage.getItem('primaryColor')
      
      // Detect system preference
      this.systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
      
      if (savedTheme) {
        this.theme = savedTheme
        this.isDarkMode = savedTheme === 'dark'
      } else {
        // Use system preference
        this.theme = this.systemPreference
        this.isDarkMode = this.systemPreference === 'dark'
      }
      
      if (savedColor) {
        this.primaryColor = savedColor
      }
      
      this.applyTheme()
      this.applyCustomColors()
      
      // Listen for system theme changes
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        this.systemPreference = e.matches ? 'dark' : 'light'
        
        // If user hasn't manually set a preference, follow system
        if (!localStorage.getItem('theme')) {
          this.setTheme(this.systemPreference)
        }
      })
    },
    
    setTheme(theme) {
      this.theme = theme
      this.isDarkMode = theme === 'dark'
      
      // Save preference
      localStorage.setItem('theme', theme)
      
      this.applyTheme()
    },
    
    toggleTheme() {
      const newTheme = this.isDarkMode ? 'light' : 'dark'
      this.setTheme(newTheme)
    },
    
    setPrimaryColor(color) {
      this.primaryColor = color
      localStorage.setItem('primaryColor', color)
      this.applyCustomColors()
    },
    
    setAccentColor(color) {
      this.accentColor = color
      localStorage.setItem('accentColor', color)
      this.applyCustomColors()
    },
    
    applyTheme() {
      const htmlElement = document.documentElement
      
      if (this.isDarkMode) {
        htmlElement.classList.add('dark')
      } else {
        htmlElement.classList.remove('dark')
      }
      
      // Update meta theme-color for mobile browsers
      const metaThemeColor = document.querySelector('meta[name="theme-color"]')
      if (metaThemeColor) {
        metaThemeColor.setAttribute('content', this.isDarkMode ? '#1F2937' : '#FFFFFF')
      }
    },
    
    applyCustomColors() {
      const root = document.documentElement
      
      // Convert hex to RGB for CSS custom properties
      const hexToRgb = (hex) => {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
        return result ? {
          r: parseInt(result[1], 16),
          g: parseInt(result[2], 16),
          b: parseInt(result[3], 16)
        } : null
      }
      
      const primaryRgb = hexToRgb(this.primaryColor)
      const accentRgb = hexToRgb(this.accentColor)
      
      if (primaryRgb) {
        root.style.setProperty('--color-primary', `${primaryRgb.r}, ${primaryRgb.g}, ${primaryRgb.b}`)
        root.style.setProperty('--color-primary-50', `${primaryRgb.r}, ${primaryRgb.g}, ${primaryRgb.b}`)
        root.style.setProperty('--color-primary-100', `${primaryRgb.r}, ${primaryRgb.g}, ${primaryRgb.b}`)
        root.style.setProperty('--color-primary-500', `${primaryRgb.r}, ${primaryRgb.g}, ${primaryRgb.b}`)
        root.style.setProperty('--color-primary-600', `${Math.max(0, primaryRgb.r - 20)}, ${Math.max(0, primaryRgb.g - 20)}, ${Math.max(0, primaryRgb.b - 20)}`)
        root.style.setProperty('--color-primary-700', `${Math.max(0, primaryRgb.r - 40)}, ${Math.max(0, primaryRgb.g - 40)}, ${Math.max(0, primaryRgb.b - 40)}`)
      }
      
      if (accentRgb) {
        root.style.setProperty('--color-accent', `${accentRgb.r}, ${accentRgb.g}, ${accentRgb.b}`)
      }
    },
    
    resetTheme() {
      this.theme = this.systemPreference
      this.isDarkMode = this.systemPreference === 'dark'
      this.primaryColor = '#3B82F6'
      this.accentColor = '#10B981'
      
      // Clear saved preferences
      localStorage.removeItem('theme')
      localStorage.removeItem('primaryColor')
      localStorage.removeItem('accentColor')
      
      this.applyTheme()
      this.applyCustomColors()
    },
    
    exportTheme() {
      return {
        theme: this.theme,
        primaryColor: this.primaryColor,
        accentColor: this.accentColor,
        isDarkMode: this.isDarkMode
      }
    },
    
    importTheme(themeConfig) {
      if (themeConfig.theme) {
        this.setTheme(themeConfig.theme)
      }
      if (themeConfig.primaryColor) {
        this.setPrimaryColor(themeConfig.primaryColor)
      }
      if (themeConfig.accentColor) {
        this.setAccentColor(themeConfig.accentColor)
      }
    }
  }
})