
<template>
<div class="h-full w-full max-h-[450px] rounded-md bg-surface-white shadow p-3 flex flex-col overflow-hidden">

  <div class="flex items-center justify-between mb-3 flex-shrink-0">
    <div>
      <h3 class="text-sm font-medium text-ink-gray-9">{{ config.title }}</h3>
      <p v-if="config.total" class="text-xs text-ink-gray-6 mt-0.5">
        Total: {{ config.total }} follow-ups
      </p>
    </div>
  </div>
  <div class="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-2 flex-1 min-h-0 overflow-y-auto call-insights-cards">
    
    <div
      v-for="item in config.data"
      :key="item.label"
      class="flex flex-col gap-1 min-w-0 p-2 rounded-lg border cursor-pointer hover:shadow-sm transition-all min-h-[55px]"
      :class="getBorderColor(item.color)"
      @click="navigateToLeads(item)"
    >
      <div class="flex items-center justify-between mb-1">
        <component
          :is="getIcon(item.icon)"
          class="size-4 flex-shrink-0"
          :class="getIconColor(item.color)"
        />
        <span class="text-lg font-semibold" :class="getTextColor(item.color)">
          {{ item.value }}
        </span>
      </div>

      <span class="text-xs font-medium text-ink-gray-7 whitespace-normal sm:whitespace-nowrap">
        {{ item.label }}
      </span>
    </div>
  </div>
</div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { inject } from 'vue'
import LucideCalendarCheck from '~icons/lucide/calendar-check'
import LucideClock from '~icons/lucide/clock'
import LucideCalendarClock from '~icons/lucide/calendar-clock'
import LucideXCircle from '~icons/lucide/x-circle'
import LucideCheckCircle from '~icons/lucide/check-circle-2'
import LucideAlertCircle from '~icons/lucide/alert-circle'

const router = useRouter()
const filters = inject('filters', {})
const fromDate = inject('fromDate', null)
const toDate = inject('toDate', null)

const props = defineProps({
  config: {
    type: Object,
    required: true,
  },
})

function getIcon(iconName) {
  const iconMap = {
    'calendar-check': LucideCalendarCheck,
    'clock': LucideClock,
    'calendar-clock': LucideCalendarClock,
    'x-circle': LucideXCircle,
    'check-circle': LucideCheckCircle,
    'alert-circle': LucideAlertCircle,
  }
  return iconMap[iconName] || LucideCalendarCheck
}
function getBorderColor(color) {
  const colorMap = {
    blue: 'border-blue-300 hover:border-blue-400',
    orange: 'border-orange-300 hover:border-orange-400',
    purple: 'border-purple-300 hover:border-purple-400',
    gray: 'border-gray-300 hover:border-gray-400',
    green: 'border-green-300 hover:border-green-400',
    red: 'border-red-300 hover:border-red-400',
  }
  return colorMap[color] || 'border-gray-300'
}

function getIconColor(color) {
  const colorMap = {
    blue: 'text-blue-600',
    orange: 'text-orange-600',
    purple: 'text-purple-600',
    gray: 'text-gray-600',
    green: 'text-green-600',
    red: 'text-red-600',
  }
  return colorMap[color] || 'text-gray-600'
}
function getTextColor(color) {
  const colorMap = {
    blue: 'text-blue-700',
    orange: 'text-orange-700',
    purple: 'text-purple-700',
    gray: 'text-gray-700',
    green: 'text-green-700',
    red: 'text-red-700',
  }
  return colorMap[color] || 'text-gray-700'
}

function navigateToLeads(item) {
  const query = {
    followup_status: item.status || item.label,
  }
  
  // Pass dashboard date range
  if (fromDate?.value) {
    query.from_date = fromDate.value
  }
  if (toDate?.value) {
    query.to_date = toDate.value
  }
  
  // Pass user filter from dashboard context
  if (filters?.user) {
    query.user = filters.user
  }
  
  console.log('FollowUpInsights: Navigating to Leads with query:', query)
  router.push({ name: 'Leads', query })
}
</script>

<style scoped>
.call-insights-cards {
  min-height: 200px;
  overflow: visible;
}

@media (min-width: 640px) and (max-width: 1023px) {
  .call-insights-cards {
    max-height: 420px;
    overflow-y: auto;
  }
}

@media (max-width: 639px) {
  .call-insights-cards {
    max-height: 350px;
    overflow-y: auto;
  }
}

.call-insights-cards::-webkit-scrollbar {
  width: 5px;
}

.call-insights-cards::-webkit-scrollbar-track {
  background: transparent;
}

.call-insights-cards::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 10px;
}

.call-insights-cards::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

.glass-widget {
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.15);
}
</style>
