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
              <span class="text-xl font-bold text-gray-900">Reports & Analytics</span>
            </router-link>
          </div>
          
          <div class="flex items-center space-x-4">
            <!-- Time period selector -->
            <select 
              v-model="selectedPeriod"
              @change="fetchData"
              class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 3 months</option>
              <option value="365">Last year</option>
            </select>
            
            <!-- Export button -->
            <button 
              @click="exportData"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              Export Report
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Overview Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Total Tasks"
          :value="stats.totalTasks"
          :change="stats.tasksChange"
          icon="clipboard"
          color="blue"
        />
        <StatsCard
          title="Completed"
          :value="stats.completedTasks"
          :change="stats.completedChange"
          icon="check-circle"
          color="green"
        />
        <StatsCard
          title="Completion Rate"
          :value="`${stats.completionRate}%`"
          :change="stats.rateChange"
          icon="trending-up"
          color="purple"
        />
        <StatsCard
          title="Avg. Daily Tasks"
          :value="stats.avgDailyTasks"
          :change="stats.avgChange"
          icon="calendar"
          color="orange"
        />
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Task Completion Chart -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Task Completion Over Time</h3>
          <canvas ref="completionChart" class="w-full h-64"></canvas>
        </div>

        <!-- Priority Distribution -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Tasks by Priority</h3>
          <canvas ref="priorityChart" class="w-full h-64"></canvas>
        </div>
      </div>

      <!-- Activity Heatmap -->
      <div class="bg-white p-6 rounded-lg shadow mb-8">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Activity Heatmap</h3>
          <div class="flex items-center space-x-2 text-sm text-gray-500">
            <span>Less</span>
            <div class="flex space-x-1">
              <div class="w-3 h-3 bg-gray-100 rounded-sm"></div>
              <div class="w-3 h-3 bg-green-200 rounded-sm"></div>
              <div class="w-3 h-3 bg-green-400 rounded-sm"></div>
              <div class="w-3 h-3 bg-green-600 rounded-sm"></div>
              <div class="w-3 h-3 bg-green-800 rounded-sm"></div>
            </div>
            <span>More</span>
          </div>
        </div>
        <ActivityHeatmap :data="heatmapData" />
      </div>

      <!-- Weekly Summary -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Productivity Insights -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Productivity Insights</h3>
          <div class="space-y-4">
            <div v-for="insight in productivityInsights" :key="insight.title" class="flex items-start">
              <div 
                class="flex-shrink-0 w-2 h-2 rounded-full mt-2 mr-3"
                :class="insight.color"
              ></div>
              <div>
                <h4 class="text-sm font-medium text-gray-900">{{ insight.title }}</h4>
                <p class="text-sm text-gray-600">{{ insight.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Goal Progress -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Goal Progress</h3>
          <div class="space-y-4">
            <div v-for="goal in recentGoals" :key="goal.id" class="flex items-center justify-between">
              <div class="flex-1">
                <h4 class="text-sm font-medium text-gray-900">{{ goal.title }}</h4>
                <div class="w-full bg-gray-200 rounded-full h-2 mt-1">
                  <div 
                    class="h-2 rounded-full transition-all duration-300"
                    :class="getProgressColor(goal.progress_percentage)"
                    :style="{ width: `${goal.progress_percentage}%` }"
                  ></div>
                </div>
              </div>
              <span class="ml-4 text-sm text-gray-500">{{ goal.progress_percentage }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Reports -->
      <div class="bg-white p-6 rounded-lg shadow">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-medium text-gray-900">Detailed Analytics</h3>
          <div class="flex space-x-2">
            <button 
              v-for="tab in reportTabs" 
              :key="tab.id"
              @click="activeTab = tab.id"
              class="px-3 py-2 text-sm font-medium rounded-md"
              :class="activeTab === tab.id 
                ? 'bg-blue-100 text-blue-700' 
                : 'text-gray-500 hover:text-gray-700'"
            >
              {{ tab.name }}
            </button>
          </div>
        </div>

        <!-- Weekly Report -->
        <div v-if="activeTab === 'weekly'" class="space-y-6">
          <WeeklyReport :data="weeklyData" />
        </div>

        <!-- Monthly Report -->
        <div v-if="activeTab === 'monthly'" class="space-y-6">
          <MonthlyReport :data="monthlyData" />
        </div>

        <!-- Performance Metrics -->
        <div v-if="activeTab === 'performance'" class="space-y-6">
          <PerformanceMetrics :data="performanceData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import StatsCard from '../components/StatsCard.vue'
import ActivityHeatmap from '../components/ActivityHeatmap.vue'
import WeeklyReport from '../components/WeeklyReport.vue'
import MonthlyReport from '../components/MonthlyReport.vue'
import PerformanceMetrics from '../components/PerformanceMetrics.vue'
import axios from 'axios'

// Register Chart.js components
Chart.register(...registerables)

export default {
  name: 'Reports',
  components: {
    StatsCard,
    ActivityHeatmap,
    WeeklyReport,
    MonthlyReport,
    PerformanceMetrics
  },
  setup() {
    const selectedPeriod = ref(30)
    const activeTab = ref('weekly')
    
    const stats = ref({
      totalTasks: 0,
      completedTasks: 0,
      completionRate: 0,
      avgDailyTasks: 0,
      tasksChange: 0,
      completedChange: 0,
      rateChange: 0,
      avgChange: 0
    })
    
    const heatmapData = ref([])
    const weeklyData = ref({})
    const monthlyData = ref({})
    const performanceData = ref({})
    const productivityInsights = ref([])
    const recentGoals = ref([])
    
    const reportTabs = [
      { id: 'weekly', name: 'Weekly' },
      { id: 'monthly', name: 'Monthly' },
      { id: 'performance', name: 'Performance' }
    ]
    
    // Chart references
    const completionChart = ref(null)
    const priorityChart = ref(null)
    let completionChartInstance = null
    let priorityChartInstance = null
    
    const fetchData = async () => {
      try {
        // Fetch analytics data
        const response = await axios.get(`/api/analytics/?period=${selectedPeriod.value}`)
        const data = response.data
        
        stats.value = data.stats
        heatmapData.value = data.heatmap
        weeklyData.value = data.weekly
        monthlyData.value = data.monthly
        performanceData.value = data.performance
        productivityInsights.value = data.insights
        recentGoals.value = data.goals
        
        // Update charts
        await nextTick()
        updateCharts(data.charts)
      } catch (error) {
        console.error('Failed to fetch analytics data:', error)
        // Use mock data for development
        loadMockData()
      }
    }
    
    const loadMockData = () => {
      stats.value = {
        totalTasks: 145,
        completedTasks: 89,
        completionRate: 61,
        avgDailyTasks: 4.8,
        tasksChange: 12,
        completedChange: 8,
        rateChange: -2,
        avgChange: 5
      }
      
      productivityInsights.value = [
        {
          title: 'Peak Productivity Time',
          description: 'You complete most tasks between 9 AM - 11 AM',
          color: 'bg-green-400'
        },
        {
          title: 'Most Productive Day',
          description: 'Tuesday is your most productive day of the week',
          color: 'bg-blue-400'
        },
        {
          title: 'Task Completion Pattern',
          description: 'You tend to complete 70% of tasks within the first 3 days',
          color: 'bg-purple-400'
        }
      ]
      
      recentGoals.value = [
        { id: 1, title: 'Learn Vue.js', progress_percentage: 75 },
        { id: 2, title: 'Complete Project Alpha', progress_percentage: 45 },
        { id: 3, title: 'Read 12 Books', progress_percentage: 60 }
      ]
      
      // Generate mock heatmap data
      generateMockHeatmap()
      updateMockCharts()
    }
    
    const generateMockHeatmap = () => {
      const data = []
      const startDate = new Date()
      startDate.setDate(startDate.getDate() - 365)
      
      for (let i = 0; i < 365; i++) {
        const date = new Date(startDate)
        date.setDate(startDate.getDate() + i)
        
        data.push({
          date: date.toISOString().split('T')[0],
          count: Math.floor(Math.random() * 5),
          level: Math.floor(Math.random() * 5)
        })
      }
      
      heatmapData.value = data
    }
    
    const updateMockCharts = async () => {
      await nextTick()
      
      // Task completion chart
      if (completionChart.value) {
        const labels = []
        const completedData = []
        const createdData = []
        
        for (let i = 29; i >= 0; i--) {
          const date = new Date()
          date.setDate(date.getDate() - i)
          labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }))
          completedData.push(Math.floor(Math.random() * 10) + 2)
          createdData.push(Math.floor(Math.random() * 8) + 3)
        }
        
        if (completionChartInstance) {
          completionChartInstance.destroy()
        }
        
        completionChartInstance = new Chart(completionChart.value, {
          type: 'line',
          data: {
            labels,
            datasets: [
              {
                label: 'Tasks Completed',
                data: completedData,
                borderColor: 'rgb(34, 197, 94)',
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                tension: 0.4
              },
              {
                label: 'Tasks Created',
                data: createdData,
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        })
      }
      
      // Priority distribution chart
      if (priorityChart.value) {
        if (priorityChartInstance) {
          priorityChartInstance.destroy()
        }
        
        priorityChartInstance = new Chart(priorityChart.value, {
          type: 'doughnut',
          data: {
            labels: ['Low', 'Medium', 'High', 'Urgent'],
            datasets: [{
              data: [25, 45, 20, 10],
              backgroundColor: [
                'rgb(34, 197, 94)',
                'rgb(234, 179, 8)',
                'rgb(249, 115, 22)',
                'rgb(239, 68, 68)'
              ]
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom'
              }
            }
          }
        })
      }
    }
    
    const updateCharts = (chartsData) => {
      // Implementation for real chart data
      updateMockCharts() // For now, use mock data
    }
    
    const getProgressColor = (percentage) => {
      if (percentage >= 80) return 'bg-green-500'
      if (percentage >= 60) return 'bg-blue-500'
      if (percentage >= 40) return 'bg-yellow-500'
      if (percentage >= 20) return 'bg-orange-500'
      return 'bg-red-500'
    }
    
    const exportData = () => {
      // Create CSV data
      const csvData = [
        ['Date', 'Tasks Created', 'Tasks Completed', 'Completion Rate'],
        ...generateExportData()
      ]
      
      const csvContent = csvData.map(row => row.join(',')).join('\n')
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      
      const link = document.createElement('a')
      link.href = url
      link.download = `kanban_report_${new Date().toISOString().split('T')[0]}.csv`
      link.click()
      
      window.URL.revokeObjectURL(url)
    }
    
    const generateExportData = () => {
      // Generate sample export data
      const data = []
      for (let i = selectedPeriod.value - 1; i >= 0; i--) {
        const date = new Date()
        date.setDate(date.getDate() - i)
        data.push([
          date.toISOString().split('T')[0],
          Math.floor(Math.random() * 8) + 3,
          Math.floor(Math.random() * 10) + 2,
          Math.floor(Math.random() * 30) + 60
        ])
      }
      return data
    }
    
    onMounted(() => {
      fetchData()
    })
    
    return {
      selectedPeriod,
      activeTab,
      stats,
      heatmapData,
      weeklyData,
      monthlyData,
      performanceData,
      productivityInsights,
      recentGoals,
      reportTabs,
      completionChart,
      priorityChart,
      fetchData,
      getProgressColor,
      exportData
    }
  }
}
</script>