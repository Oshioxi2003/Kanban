<template>
  <div class="activity-heatmap">
    <!-- Month labels -->
    <div class="flex text-xs text-gray-500 mb-2">
      <div class="w-12"></div> <!-- Space for day labels -->
      <div v-for="month in monthLabels" :key="month.name" class="flex-1 text-center">
        <span v-if="month.visible">{{ month.name }}</span>
      </div>
    </div>
    
    <!-- Grid -->
    <div class="flex">
      <!-- Day labels -->
      <div class="w-12 text-xs text-gray-500 space-y-1">
        <div class="h-3"></div> <!-- Empty space for Monday -->
        <div class="h-3 flex items-center">Mon</div>
        <div class="h-3"></div> <!-- Empty space for Tuesday -->
        <div class="h-3 flex items-center">Wed</div>
        <div class="h-3"></div> <!-- Empty space for Thursday -->
        <div class="h-3 flex items-center">Fri</div>
        <div class="h-3"></div> <!-- Empty space for Saturday -->
      </div>
      
      <!-- Heatmap grid -->
      <div class="flex-1 grid grid-cols-53 gap-1">
        <div
          v-for="(day, index) in gridData"
          :key="index"
          class="w-3 h-3 rounded-sm cursor-pointer hover:ring-2 hover:ring-gray-300 transition-all duration-200"
          :class="getCellClass(day.level)"
          :title="getTooltip(day)"
          @click="$emit('day-click', day)"
        ></div>
      </div>
    </div>
    
    <!-- Legend -->
    <div class="flex items-center justify-end mt-2 text-xs text-gray-500">
      <span class="mr-2">{{ getPeriodText() }}</span>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'ActivityHeatmap',
  props: {
    data: {
      type: Array,
      default: () => []
    }
  },
  emits: ['day-click'],
  setup(props) {
    const monthLabels = computed(() => {
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      const labels = []
      const now = new Date()
      
      for (let i = 0; i < 12; i++) {
        const date = new Date(now.getFullYear(), now.getMonth() - i, 1)
        labels.unshift({
          name: months[date.getMonth()],
          visible: i % 2 === 0 // Show every other month for space
        })
      }
      
      return labels
    })
    
    const gridData = computed(() => {
      const grid = []
      const now = new Date()
      const startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 364)
      
      // Start from Sunday of the week containing startDate
      const firstSunday = new Date(startDate)
      firstSunday.setDate(startDate.getDate() - startDate.getDay())
      
      // Generate 53 weeks * 7 days = 371 cells
      for (let week = 0; week < 53; week++) {
        for (let day = 0; day < 7; day++) {
          const currentDate = new Date(firstSunday)
          currentDate.setDate(firstSunday.getDate() + (week * 7) + day)
          
          const dateStr = currentDate.toISOString().split('T')[0]
          const dayData = props.data.find(d => d.date === dateStr)
          
          grid.push({
            date: dateStr,
            count: dayData?.count || 0,
            level: dayData?.level || 0,
            isCurrentMonth: currentDate.getMonth() === now.getMonth(),
            isFuture: currentDate > now
          })
        }
      }
      
      return grid
    })
    
    const getCellClass = (level) => {
      const baseClass = 'border border-gray-100'
      
      if (level === 0) return `${baseClass} bg-gray-100`
      if (level === 1) return `${baseClass} bg-green-200`
      if (level === 2) return `${baseClass} bg-green-400`
      if (level === 3) return `${baseClass} bg-green-600`
      if (level >= 4) return `${baseClass} bg-green-800`
      
      return baseClass
    }
    
    const getTooltip = (day) => {
      const date = new Date(day.date)
      const dateStr = date.toLocaleDateString('en-US', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric',
        year: 'numeric'
      })
      
      if (day.count === 0) {
        return `No tasks completed on ${dateStr}`
      } else if (day.count === 1) {
        return `1 task completed on ${dateStr}`
      } else {
        return `${day.count} tasks completed on ${dateStr}`
      }
    }
    
    const getPeriodText = () => {
      const now = new Date()
      const startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 364)
      
      return `${startDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${now.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`
    }
    
    return {
      monthLabels,
      gridData,
      getCellClass,
      getTooltip,
      getPeriodText
    }
  }
}
</script>

<style scoped>
.activity-heatmap {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.grid-cols-53 {
  grid-template-columns: repeat(53, minmax(0, 1fr));
}
</style>