<template>
  <div class="h-full w-full flex flex-col bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden">
    <!-- Header -->
    <div class="flex items-center justify-between px-5 py-3 border-b border-gray-100 dark:border-gray-800 flex-shrink-0">
      <h3 class="text-sm font-bold text-gray-800 dark:text-gray-100">{{ __(data.title) }}</h3>
      <div v-if="talkTime" class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">
        <Clock class="w-3.5 h-3.5" />
        <span>Total Talk Time</span>
        <span class="font-bold text-blue-600 dark:text-blue-400">{{ talkTime.value }}</span>
      </div>
    </div>

    <!-- Cards grid — only show cards with value > 0 -->
   <div class="flex-1 overflow-y-auto p-4 call-insights-cards">
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
        <div
          v-for="(card, idx) in visibleCards"
          :key="idx"
          class="flex flex-col items-center justify-center gap-1.5 p-4 rounded-2xl bg-white dark:bg-gray-900 border-2 cursor-pointer transition-all duration-200 hover:shadow-md hover:-translate-y-0.5 min-h-[110px]"
          :class="getBorderColor(card.label)"
          @click="navigateToCallLogs(card)"
        >
          <component :is="getIcon(card.label)" class="w-7 h-7" :class="getIconColor(card.label)" />
          <p class="text-[10px] uppercase font-semibold tracking-wider text-gray-400 dark:text-gray-500 text-center leading-tight">
            {{ __(card.label) }}
          </p>
          <p class="text-2xl font-bold leading-none" :class="getValueColor(card.label)">
            {{ card.value }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { inject } from 'vue'
import {
  Phone,
  PhoneIncoming,
  PhoneOutgoing,
  PhoneCall,
  PhoneOff,
  PhoneMissed,
  Clock,
  Loader,
  Ban,
  Smartphone,
  UserX,
  ShoppingBag,
} from 'lucide-vue-next'

const router = useRouter()
const injectedFilters = inject('filters', {})
const fromDate = inject('fromDate', null)
const toDate = inject('toDate', null)

const props = defineProps({
  data: { type: Object, required: true },
})

const talkTime = computed(() =>
  props.data.data?.find((c) => c.label.toLowerCase().includes('time'))
)

// All cards except talk time
const cards = computed(() =>
  (props.data.data || []).filter((c) => !c.label.toLowerCase().includes('time'))
)

// Only show cards where value > 0 OR it's a top-level summary card (total/incoming/outgoing)
const visibleCards = computed(() =>
  cards.value.filter((c) => {
    const l = c.label.toLowerCase()
    const isTopLevel = l.includes('total') || l.includes('incoming') || l.includes('outgoing')
    return isTopLevel || (c.value > 0 && !c.hidden)
  })
)

function getIcon(label) {
  const l = label.toLowerCase()
  if (l.includes('total')) return Phone
  if (l.includes('incoming')) return PhoneIncoming
  if (l.includes('outgoing')) return PhoneOutgoing
  if (l.includes('ringing')) return Loader
  if (l.includes('completed')) return PhoneCall
  if (l.includes('failed')) return PhoneMissed
  if (l.includes('busy')) return Ban
  if (l.includes('queued')) return Clock
  if (l.includes('cancel')) return PhoneOff
  if (l.includes('smartphone')) return Smartphone
  if (l.includes('agent')) return UserX
  if (l.includes('seller')) return ShoppingBag
  return Phone
}

function getBorderColor(label) {
  const l = label.toLowerCase()
  if (l.includes('total')) return 'border-gray-200 dark:border-gray-700'
  if (l.includes('incoming')) return 'border-green-300 dark:border-green-700'
  if (l.includes('outgoing')) return 'border-purple-300 dark:border-purple-700'
  if (l.includes('ringing')) return 'border-orange-300 dark:border-orange-700'
  if (l.includes('completed')) return 'border-green-300 dark:border-green-700'
  if (l.includes('failed')) return 'border-red-300 dark:border-red-700'
  if (l.includes('busy')) return 'border-orange-300 dark:border-orange-700'
  if (l.includes('queued')) return 'border-gray-200 dark:border-gray-700'
  if (l.includes('cancel')) return 'border-gray-200 dark:border-gray-700'
  if (l.includes('smartphone')) return 'border-yellow-300 dark:border-yellow-700'
  if (l.includes('agent')) return 'border-red-200 dark:border-red-800'
  if (l.includes('seller')) return 'border-violet-300 dark:border-violet-700'
  return 'border-gray-200 dark:border-gray-700'
}

function getIconColor(label) {
  const l = label.toLowerCase()
  if (l.includes('total')) return 'text-blue-500'
  if (l.includes('incoming')) return 'text-green-500'
  if (l.includes('outgoing')) return 'text-purple-500'
  if (l.includes('ringing')) return 'text-orange-400'
  if (l.includes('completed')) return 'text-green-500'
  if (l.includes('failed')) return 'text-red-500'
  if (l.includes('busy')) return 'text-orange-500'
  if (l.includes('queued')) return 'text-gray-400'
  if (l.includes('cancel')) return 'text-gray-400'
  if (l.includes('smartphone')) return 'text-yellow-500'
  if (l.includes('agent')) return 'text-red-400'
  if (l.includes('seller')) return 'text-violet-500'
  return 'text-gray-400'
}

function getValueColor(label) {
  const l = label.toLowerCase()
  if (l.includes('total')) return 'text-blue-600 dark:text-blue-400'
  if (l.includes('incoming')) return 'text-green-600 dark:text-green-400'
  if (l.includes('outgoing')) return 'text-purple-600 dark:text-purple-400'
  if (l.includes('ringing')) return 'text-orange-500 dark:text-orange-400'
  if (l.includes('completed')) return 'text-green-600 dark:text-green-400'
  if (l.includes('failed')) return 'text-red-600 dark:text-red-400'
  if (l.includes('busy')) return 'text-orange-600 dark:text-orange-400'
  if (l.includes('queued')) return 'text-gray-600 dark:text-gray-300'
  if (l.includes('cancel')) return 'text-gray-500 dark:text-gray-400'
  if (l.includes('smartphone')) return 'text-yellow-600 dark:text-yellow-400'
  if (l.includes('agent')) return 'text-red-500 dark:text-red-400'
  if (l.includes('seller')) return 'text-violet-600 dark:text-violet-400'
  return 'text-gray-700 dark:text-gray-200'
}

// Maps card label keywords → exact DB status value for filtering
const STATUS_MAP = [
  { match: 'ringing',    status: 'Ringing' },
  { match: 'completed',  status: 'Completed' },
  { match: 'failed',     status: 'Failed' },
  { match: 'busy',       status: 'Busy' },
  { match: 'queued',     status: 'Queued' },
  { match: 'cancel',     status: 'Canceled' },
  { match: 'smartphone', status: 'Call not receive by agent (Over Smartphone)' },
  { match: 'agent',      status: 'Call not receive by agent' },
  { match: 'seller',     status: 'Not received by seller' },
]

function navigateToCallLogs(card) {
  const query = {}
  if (fromDate?.value) query.from_date = fromDate.value
  if (toDate?.value) query.to_date = toDate.value
  if (injectedFilters?.user) query.user = injectedFilters.user

  const label = card.label.toLowerCase()

  // Type-based cards
  if (label.includes('incoming') && !label.includes('not')) {
    query.type = 'Incoming'
  } else if (label.includes('outgoing')) {
    query.type = 'Outgoing'
  } else {
    // Status-based — find first match
    for (const entry of STATUS_MAP) {
      if (label.includes(entry.match)) {
        query.status = entry.status
        break
      }
    }
  }

  router.push({ name: 'Call Logs', query: { ...query, _r: Date.now() } })
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