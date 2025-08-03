<template>
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div 
            class="p-2 rounded-md"
            :class="`bg-${color}-100`"
          >
            <component 
              :is="iconComponent" 
              class="h-6 w-6"
              :class="`text-${color}-600`"
            />
          </div>
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">{{ title }}</dt>
            <dd class="flex items-baseline">
              <div class="text-2xl font-semibold text-gray-900">{{ value }}</div>
              <div 
                v-if="change !== undefined"
                class="ml-2 flex items-baseline text-sm font-semibold"
                :class="changeClass"
              >
                <svg 
                  v-if="change > 0"
                  class="self-center flex-shrink-0 h-4 w-4"
                  :class="`text-${changeColor}-500`"
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path 
                    fill-rule="evenodd" 
                    d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" 
                    clip-rule="evenodd"
                  />
                </svg>
                <svg 
                  v-else-if="change < 0"
                  class="self-center flex-shrink-0 h-4 w-4"
                  :class="`text-${changeColor}-500`"
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path 
                    fill-rule="evenodd" 
                    d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" 
                    clip-rule="evenodd"
                  />
                </svg>
                <span class="sr-only">{{ change > 0 ? 'Increased' : 'Decreased' }} by</span>
                {{ Math.abs(change) }}%
              </div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'StatsCard',
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: [String, Number],
      required: true
    },
    change: {
      type: Number,
      default: undefined
    },
    icon: {
      type: String,
      required: true
    },
    color: {
      type: String,
      default: 'blue'
    }
  },
  setup(props) {
    const iconComponent = computed(() => {
      const icons = {
        clipboard: 'ClipboardIcon',
        'check-circle': 'CheckCircleIcon',
        'trending-up': 'TrendingUpIcon',
        calendar: 'CalendarIcon',
        users: 'UsersIcon',
        clock: 'ClockIcon'
      }
      
      return icons[props.icon] || 'ClipboardIcon'
    })
    
    const changeColor = computed(() => {
      if (props.change === undefined) return 'gray'
      return props.change >= 0 ? 'green' : 'red'
    })
    
    const changeClass = computed(() => {
      if (props.change === undefined) return ''
      return props.change >= 0 ? 'text-green-600' : 'text-red-600'
    })
    
    return {
      iconComponent,
      changeColor,
      changeClass
    }
  }
}
</script>

<!-- Icon components (simplified inline versions) -->
<template v-if="false">
  <svg class="ClipboardIcon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
  </svg>
  
  <svg class="CheckCircleIcon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
  </svg>
  
  <svg class="TrendingUpIcon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
  </svg>
  
  <svg class="CalendarIcon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
  </svg>
</template>