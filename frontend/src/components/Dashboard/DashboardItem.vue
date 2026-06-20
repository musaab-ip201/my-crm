<template>
  <div
    class="h-full w-full bg-[#fdfdfd] dark:bg-black p-2 dashboard-widget transition-colors duration-300"
  >
    <div
      v-if="item.type == 'number_chart'"
      class="flex h-full w-full rounded-xl border border-purple-400 bg-white dark:bg-gray-900 shadow-lg dark:shadow-none overflow-hidden transition-all duration-300 hover:shadow-xl dark:hover:shadow-none hover:-translate-y-1"
      :class="
        isClickable(item)
          ? 'cursor-pointer hover:border-purple-600 transition-colors'
          : 'cursor-default'
      "
      @click="isClickable(item) && navigateToPage(item)"
    >
      <Tooltip :text="__(item.data.tooltip)">
        <NumberChart
          class="!items-start !bg-transparent"
          v-if="item.data"
          :key="index"
          :config="item.data"
        />
      </Tooltip>
    </div>

    <div
      v-else-if="item.type === 'custom' && item.name === 'call_insights'"
      class="h-full w-full"
    >
      <CallInsights v-if="item.data" :data="item.data" />
    </div>

    <div
      v-else-if="item.type === 'custom' && item.name === 'followup_insights'"
      class="h-full w-full"
    >
      <FollowUpInsights v-if="item.data" :config="item.data" />
    </div>

    <!-- <div
      v-else-if="
        item.name === 'call_lifecycle_sunburst' ||
        item.name === 'call_volume_data' ||
        item.name === 'lead_status_analytics' ||
        item.data?.type === 'lead_actions_donut'
      "
      class="h-full w-full rounded-2xl backdrop-blur-lg bg-white/70 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 shadow-lg p-6 flex flex-col transition-all duration-300 hover:shadow-2xl"
    >
      <div class="mb-2 flex justify-between items-start">
        <div>
          <h3 class="font-bold text-sm text-gray-800 dark:text-gray-400">
            {{ item.data.title }}
          </h3>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ item.data.subtitle }}
          </p>
        </div>
        <div
          v-if="item.data.department"
          class="px-2 py-1 rounded bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-[10px] font-bold uppercase tracking-wider"
        >
          {{ item.data.department }}
        </div>
      </div>
      <div
        :id="'chart-' + item.name + index"
        class="flex-1 w-full h-full min-h-[300px]"
      ></div>
    </div> -->

    <!-- updated code at 07-04-2026 -->
    <div
      v-else-if="
        item.name === 'call_lifecycle_sunburst' ||
        item.name === 'call_volume_data' ||
        item.name === 'lead_status_analytics' ||
        item.data?.type === 'lead_actions_donut'
      "
      class="h-full w-full rounded-2xl backdrop-blur-lg bg-white/70 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 shadow-lg p-6 flex flex-col transition-all duration-300 hover:shadow-2xl"
    >
      <div class="mb-2 flex justify-between items-start">
        <div>
          <h3 class="font-bold text-sm text-gray-800 dark:text-gray-400">
            {{
              item.data.type === 'lead_actions_donut'
                ? item.data.title
                : item.data.title
            }}
          </h3>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ item.data.subtitle }}
          </p>
        </div>

        <div class="flex flex-col items-end gap-1">
          <template v-if="item.data?.type === 'lead_actions_donut'">
            <div
              class="flex items-center gap-2 px-2 py-1 rounded bg-purple-50 dark:bg-purple-900/20 border border-purple-100 dark:border-purple-800"
            >
              <span
                class="text-[11px] font-medium text-gray-600 dark:text-gray-400 uppercase tracking-tight"
              >
                Success Rate
              </span>
              <span
                class="text-sm font-bold text-purple-600 dark:text-purple-400"
              >
                {{ item.data.mark_done_percent }}%
              </span>
            </div>
          </template>

          <div
            v-if="item.data.department"
            class="px-2 py-1 rounded bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-[10px] font-bold uppercase tracking-wider"
          >
            {{ item.data.department }}
          </div>
        </div>
      </div>
      <div
        :id="'chart-' + item.name + index"
        class="flex-1 w-full h-full min-h-[300px]"
      ></div>
    </div>
    <!-- --------------- -->
    
    
    <div
      v-else-if="item.type == 'axis_chart'"
      class="h-full w-full rounded-md bg-surface-white shadow-md dark:shadow-none transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
    >
      <AxisChart v-if="item.data" :config="item.data" />
    </div>

    <div
      v-else-if="item.type == 'donut_chart'"
      class="h-full w-full rounded-md bg-surface-white shadow-md dark:shadow-none overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
    >
      <DonutChart v-if="item.data" :config="item.data" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { AxisChart, DonutChart, NumberChart, Tooltip } from 'frappe-ui'
import FollowUpInsights from './FollowUpInsights.vue'
import CallInsights from './CallInsights.vue'
import { useRouter } from 'vue-router'
import { inject } from 'vue'
import {
  Phone,
  PhoneCall,
  PhoneIncoming,
  PhoneOutgoing,
  PhoneOff,
  PhoneMissed,
  Clock,
  Loader,
  Ban,
} from 'lucide-vue-next'

// const colorClasses = {
//   blue: {
//     text: 'text-blue-600',
//     icon: 'text-blue-500',
//     border: 'border-blue-400',
//   },
//   green: {
//     text: 'text-green-600',
//     icon: 'text-green-500',
//     border: 'border-green-400',
//   },
//   purple: {
//     text: 'text-purple-600',
//     icon: 'text-purple-500',
//     border: 'border-purple-400',
//   },
//   indigo: {
//     text: 'text-indigo-600 dark:text-indigo-400',
//     icon: 'text-indigo-500 dark:text-indigo-400',
//     border: 'border-indigo-400 dark:border-indigo-500',
//   },
//   orange: {
//     text: 'text-orange-600',
//     icon: 'text-orange-500',
//     border: 'border-orange-400',
//   },
//   red: {
//     text: 'text-red-600',
//     icon: 'text-red-500',
//     border: 'border-red-400',
//   },
//   yellow: {
//     text: 'text-amber-600',
//     icon: 'text-amber-500',
//     border: 'border-amber-400',
//   },
//   gray: {
//     text: 'text-gray-700 dark:text-gray-300',
//     icon: 'text-gray-500 dark:text-gray-400',
//     border: 'border-gray-300 dark:border-gray-600',
//   },
// }

function getCallIcon(label) {
  const l = label.toLowerCase()
  if (l.includes('total calls')) return Phone
  if (l.includes('incoming')) return PhoneIncoming
  if (l.includes('outgoing')) return PhoneOutgoing
  if (l.includes('initiated')) return PhoneOutgoing
  if (l.includes('ringing')) return Loader
  if (l.includes('in progress')) return PhoneIncoming
  if (l.includes('completed')) return PhoneCall
  if (l.includes('failed')) return PhoneOff
  if (l.includes('no answer')) return PhoneMissed
  if (l.includes('busy')) return Ban
  if (l.includes('queued')) return Clock
  if (l.includes('canceled')) return PhoneOff
  if (l.includes('time')) return Clock
  return Phone
}

const router = useRouter()

const props = defineProps({
  index: {
    type: Number,
    required: true,
  },
  item: {
    type: Object,
    required: true,
  },
  editing: {
    type: Boolean,
    default: false,
  },
})

const fromDate = inject('fromDate', null)
const toDate = inject('toDate', null)
const dashboardFilters = inject('filters', null)

function isClickable(item) {
  if (props.editing) return false
  if (!item || !item.name) return false
  const itemName = item.name.toLowerCase().trim()
  const clickableCards = [
    'total_leads',
    'fresh_leads',
    'ongoing_deals',
    'won_deals',
    'lost_deals',
    'converted_leads',
  ]
  return clickableCards.some((card) => card === itemName)
}

function navigateToPage(item) {
  if (!isClickable(item)) return
  const route = router.currentRoute.value
  let from_date, to_date, user

  if (dashboardFilters && fromDate && toDate) {
    from_date = fromDate.value ? fromDate.value.split('-').join('-') : null
    to_date = toDate.value ? toDate.value.split('-').join('-') : null
    user = dashboardFilters.user
  } else {
    from_date = route.query.from_date
    to_date = route.query.to_date
    user = route.query.user
  }

  let targetRoute = 'Leads'
  let additionalQueryParams = {}

  if (item.name) {
    switch (item.name.toLowerCase()) {
      case 'total_leads':
        targetRoute = 'Leads'
        break
      case 'fresh_leads':
        targetRoute = 'Leads'
        const today = new Date().toISOString().split('T')[0]
        additionalQueryParams.from_date = today
        additionalQueryParams.to_date = today
        break
      case 'ongoing_deals':
        targetRoute = 'Deals'
        additionalQueryParams.status_type = 'Ongoing'
        break
      case 'won_deals':
        targetRoute = 'Deals'
        additionalQueryParams.status_type = 'Won'
        break
      case 'lost_deals':
        targetRoute = 'Deals'
        additionalQueryParams.status_type = 'Lost'
        break
      case 'converted_leads':
        targetRoute = 'Contacts'
        break
      default:
        return
    }
  }

  const queryParams = {}
  if (from_date) queryParams.from_date = from_date
  if (to_date) queryParams.to_date = to_date
  if (user !== undefined) queryParams.user = user
  Object.assign(queryParams, additionalQueryParams)

  router.push({ name: targetRoute, query: queryParams })
}

function goToCallLogs(card) {
  if (props.editing) return
  const label = card.label.toLowerCase()
  const query = {}
  const route = router.currentRoute.value
  let from_date, to_date, user

  if (dashboardFilters && fromDate && toDate) {
    from_date = fromDate.value ? fromDate.value.split('-').join('-') : null
    to_date = toDate.value ? toDate.value.split('-').join('-') : null
    user = dashboardFilters.user
  } else {
    from_date = route.query.from_date
    to_date = route.query.to_date
    user = route.query.user
  }

  if (from_date) query.from_date = from_date
  if (to_date) query.to_date = to_date
  if (user !== undefined) query.user = user

  const statusMap = {
    initiated: 'Initiated',
    ringing: 'Ringing',
    'in progress': 'In Progress',
    completed: 'Completed',
    failed: 'Failed',
    busy: 'Busy',
    'no answer': 'No Answer',
    queued: 'Queued',
    canceled: 'Canceled',
  }

  Object.keys(statusMap).forEach((key) => {
    if (label.includes(key)) {
      query.status = statusMap[key]
    }
  })

  if (label.includes('incoming')) query.type = 'Incoming'
  if (label.includes('outgoing')) query.type = 'Outgoing'

  console.log('[DashboardItem] Navigating to Call Logs with query:', query)
  console.log('[DashboardItem] Card label:', label)
  router.push({ name: 'Call Logs', query: { ...query, _r: Date.now() } })
}

function renderCustomChart() {
  const chartData = props.item.data

  // If your API returns a raw array, wrap it so the rest of the logic works
  if (Array.isArray(chartData) && props.item.name === 'lead_status_analytics') {
    chartData = {
      type: 'lead_status_distribution',
      data: chartData,
    }
  }
  // Update the check to include lead_actions_donut
  if (
    !chartData ||
    ![
      'sunburst',
      'bar_volume',
      'pie',
      'lead_actions_donut',
      'lead_status_distribution',
    ].includes(chartData.type)
  )
    return

  const chartDom = document.getElementById(
    'chart-' + props.item.name + props.index,
  )
  if (!chartDom) return

  let myChart = echarts.getInstanceByDom(chartDom)
  if (myChart) myChart.dispose()
  myChart = echarts.init(chartDom)

  let option = {}

  if (chartData.type === 'sunburst' || chartData.type === 'pie') {
    const statusTotals = {}
    chartData.data.forEach((d) => {
      statusTotals[d.status] = (statusTotals[d.status] || 0) + d.count
    })
    const simplePieData = Object.keys(statusTotals).map((status) => ({
      name: status,
      value: statusTotals[status],
    }))
    option = {
      tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
      animation: true,
      animationDuration: 1200,
      animationEasing: 'elasticOut',
      series: [
        {
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
          label: { show: true, position: 'outside', formatter: '{b}' },
          data: simplePieData,
        },
      ],
    }
  } else if (chartData.type === 'bar_volume') {
    const counts = chartData.data
    option = {
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      animation: true,
      animationDuration: 1200,
      animationEasing: 'elasticOut',
      grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
      xAxis: {
        type: 'category',
        data: ['Incoming', 'Outgoing', 'Total Calls'],
        axisLabel: { fontWeight: 'bold' },
      },
      yAxis: { type: 'value', minInterval: 1 },
      series: [
        {
          name: 'Calls',
          type: 'bar',
          barWidth: '50%',
          data: [
            { value: counts.Incoming, itemStyle: { color: '#fac858' } },
            { value: counts.Outgoing, itemStyle: { color: '#91cc75' } },
            { value: counts.Total, itemStyle: { color: '#5470c6' } },
          ],
          label: { show: true, position: 'top', fontWeight: 'bold' },
        },
      ],
    }
  } 
  // else if (chartData.type === 'lead_actions_donut') {
  //   const pieData = chartData.data.map((row) => ({
  //     name: row.action,
  //     value: row.count,
  //   }))

  //   option = {
  //     tooltip: { trigger: 'item', formatter: '{b}: <b>{c}</b> ({d}%)' },
  //     series: [
  //       {
  //         name: 'Actions',
  //         type: 'pie',
  //         color: chartData.colors,
  //         radius: ['40%', '70%'],
  //         avoidLabelOverlap: true,
  //         itemStyle: {
  //           borderRadius: 8,
  //           borderColor: '#fff',
  //           borderWidth: 2,
  //         },
  //         label: { show: true },
  //         emphasis: {
  //           label: { show: true, fontSize: '14', fontWeight: 'bold' },
  //         },
  //         data: pieData,
  //       },
  //     ],
  //   }
  // } 
  else if (chartData.type === 'lead_actions_donut') {
    const pieData = chartData.data.map((row) => ({
      name: row.action,
      value: row.count,
    }))

    option = {
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)',
      },
      series: [
        {
          name: 'Actions',
          type: 'pie',
          color: chartData.colors,
          radius: ['40%', '70%'],
          avoidLabelOverlap: true,

          scale: false,
          itemStyle: {
            borderRadius: 8,
            borderColor: '#fff',
            borderWidth: 2,
          },
          label: {
            show: true,
            position: 'outside',
            fontSize: 12,
            fontWeight: 'normal',
          },

          emphasis: {
            label: {
              show: true,
              fontSize: 12,
              fontWeight: 'normal',
            },
          },
          data: pieData,
        },
      ],
    }
  }
  else if (chartData.type === 'lead_status_distribution') {
    // Calculate total for the percentage in the tooltip
    const total = chartData.data.reduce((sum, item) => sum + item.count, 0)

    option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        formatter: (params) => {
          let data = params[0]
          let percent = total > 0 ? ((data.value / total) * 100).toFixed(1) : 0
          return `${data.name}: <b>${data.value}</b> (${percent}%)`
        },
      },
      grid: { left: '3%', right: '10%', bottom: '3%', containLabel: true },
      xAxis: { type: 'value', boundaryGap: [0, 0.01] },
      yAxis: {
        type: 'category',
        data: chartData.data.map((item) => item.status),
        inverse: true, // Highest count at the top
        axisLabel: { fontSize: 10 },
      },
      series: [
        {
          name: 'Leads',
          type: 'bar',
          data: chartData.data.map((item) => item.count),
          itemStyle: {
            color: (params) => {
              return (
                chartData.colors?.[
                  params.dataIndex % chartData.colors.length
                ] || '#5470c6'
              )
            },
          },
          label: {
            show: true,
            position: 'right',
            formatter: '{c}',
            fontSize: 10,
          },
        },
      ],
    }
  }

  myChart.setOption(option)
}

onMounted(() => {
  nextTick(() => {
    renderCustomChart()
  })
})

watch(
  () => props.item.data,
  () => {
    nextTick(() => {
      renderCustomChart()
    })
  },
  { deep: true },
)

let resizeObserver

onMounted(() => {
  const chartDom = document.getElementById(
    'chart-' + props.item.name + props.index,
  )
  if (!chartDom) return
  resizeObserver = new ResizeObserver(() => {
    const chart = echarts.getInstanceByDom(chartDom)
    chart && chart.resize()
  })
  resizeObserver.observe(chartDom)
})

onBeforeUnmount(() => {
  if (resizeObserver) resizeObserver.disconnect()
})
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