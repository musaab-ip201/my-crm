<template>
  <LayoutHeader>
    <template #left-header>
      <ViewBreadcrumbs v-model="viewControls" routeName="Call Logs" />
    </template>
    <template #right-header>
      <CustomActions
        v-if="callLogsListView?.customListActions"
        :actions="callLogsListView.customListActions"
      />
      <Button
        variant="solid"
        :label="__('Create')"
        iconLeft="plus"
        @click="createCallLog"
      />
    </template>
  </LayoutHeader>

  <!-- Filter Bar -->
  <div class="flex flex-wrap items-center gap-2 px-4 py-2 border-b border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900">
    <!-- Start Date -->
    <div class="flex items-center gap-1.5">
      <span class="text-xs text-gray-500 dark:text-gray-400 whitespace-nowrap">Start Date</span>
      <input
        type="date"
        v-model="filterStartDate"
        class="text-xs border border-gray-300 dark:border-gray-600 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200"
      />
    </div>
    <!-- End Date -->
    <div class="flex items-center gap-1.5">
      <span class="text-xs text-gray-500 dark:text-gray-400 whitespace-nowrap">End Date</span>
      <input
        type="date"
        v-model="filterEndDate"
        class="text-xs border border-gray-300 dark:border-gray-600 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200"
      />
    </div>
    <!-- Status -->
    <div class="flex items-center gap-1.5">
      <span class="text-xs text-gray-500 dark:text-gray-400">Status</span>
      <select
        v-model="filterStatus"
        class="text-xs border border-gray-300 dark:border-gray-600 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200"
      >
        <option value="">All</option>
        <option>Initiated</option>
        <option>Ringing</option>
        <option>In Progress</option>
        <option>Completed</option>
        <option>Failed</option>
        <option>Busy</option>
        <option>Call not receive by agent</option>
        <option>Call not receive by agent (Over Smartphone)</option>
        <option>Not received by seller</option>
      </select>
    </div>
    <!-- Type -->
    <div class="flex items-center gap-1.5">
      <span class="text-xs text-gray-500 dark:text-gray-400">Type</span>
      <select
        v-model="filterType"
        class="text-xs border border-gray-300 dark:border-gray-600 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200"
      >
        <option value="">All</option>
        <option>Incoming</option>
        <option>Outgoing</option>
      </select>
    </div>
    <!-- Apply & Clear buttons -->
    <button
      @click="applyFilters"
      class="text-xs px-3 py-1 rounded bg-blue-600 text-white hover:bg-blue-700 transition"
    >
      Apply
    </button>
    <button
      @click="clearFilters"
      class="text-xs px-3 py-1 rounded border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition"
    >
      Clear
    </button>
  </div>

  <ViewControls
    ref="viewControls"
    v-model="callLogs"
    v-model:loadMore="loadMore"
    v-model:resizeColumn="triggerResize"
    v-model:updatedPageCount="updatedPageCount"
    doctype="CRM Call Log"
    :filters="combinedFilters"
  />
  <CallLogsListView
    ref="callLogsListView"
    v-if="callLogs.data && rows.length"
    v-model="callLogs.data.page_length_count"
    v-model:list="callLogs"
    :rows="rows"
    :columns="callLogs.data.columns"
    :options="{
      showTooltip: false,
      resizeColumn: true,
      rowCount: callLogs.data.row_count,
      totalCount: callLogs.data.total_count,
    }"
    @showCallLog="showCallLog"
    @loadMore="() => loadMore++"
    @columnWidthUpdated="() => triggerResize++"
    @updatePageCount="(count) => (updatedPageCount = count)"
    @applyFilter="(data) => viewControls.applyFilter(data)"
    @applyLikeFilter="(data) => viewControls.applyLikeFilter(data)"
    @likeDoc="(data) => viewControls.likeDoc(data)"
    @selectionsChanged="
      (selections) => viewControls.updateSelections(selections)
    "
  />
  <div
    v-else-if="callLogs.data"
    class="flex h-full items-center justify-center"
  >
    <div
      class="flex flex-col items-center gap-3 text-xl font-medium text-ink-gray-4"
    >
      <PhoneIcon class="h-10 w-10" />
      <span>{{ __('No {0} Found', [__('Logs')]) }}</span>
    </div>
  </div>
  <CallLogDetailModal
    v-model="showCallLogDetailModal"
    v-model:callLogModal="showCallLogModal"
    v-model:callLog="callLog"
  />
  <CallLogModal
    v-if="showCallLogModal"
    v-model="showCallLogModal"
    :data="callLog.data"
    :options="{ afterInsert: () => callLogs.reload() }"
  />
</template>

<script setup>
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import CustomActions from '@/components/CustomActions.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewControls from '@/components/ViewControls.vue'
import CallLogsListView from '@/components/ListViews/CallLogsListView.vue'
import CallLogDetailModal from '@/components/Modals/CallLogDetailModal.vue'
import CallLogModal from '@/components/Modals/CallLogModal.vue'
import { getCallLogDetail } from '@/utils/callLog'
import { createResource } from 'frappe-ui'
import { computed, ref, onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const callLogsListView = ref(null)
const showCallLogModal = ref(false)

// callLogs data is loaded in the ViewControls component
const callLogs = ref({})
const loadMore = ref(1)
const triggerResize = ref(1)
const updatedPageCount = ref(20)
const viewControls = ref(null)

// Filter bar state
const filterStartDate = ref('')
const filterEndDate = ref('')
const filterStatus = ref('')
const filterType = ref('')

// Active applied filters (only updated when Apply is clicked)
const activeStartDate = ref(route.query.from_date || '')
const activeEndDate = ref(route.query.to_date || '')
const activeStatus = ref(route.query.status || '')
const activeType = ref(route.query.type || '')

// Sync filter bar with URL query params on load
onMounted(() => {
  filterStartDate.value = route.query.from_date || ''
  filterEndDate.value = route.query.to_date || ''
  filterStatus.value = route.query.status || ''
  filterType.value = route.query.type || ''
  openCallLogFromURL()
})

function applyFilters() {
  activeStartDate.value = filterStartDate.value
  activeEndDate.value = filterEndDate.value
  activeStatus.value = filterStatus.value
  activeType.value = filterType.value
  nextTick(() => {
    if (viewControls.value?.reload) viewControls.value.reload()
    else if (callLogs.value?.reload) callLogs.value.reload()
  })
}

function clearFilters() {
  filterStartDate.value = ''
  filterEndDate.value = ''
  filterStatus.value = ''
  filterType.value = ''
  activeStartDate.value = ''
  activeEndDate.value = ''
  activeStatus.value = ''
  activeType.value = ''
  nextTick(() => {
    if (viewControls.value?.reload) viewControls.value.reload()
    else if (callLogs.value?.reload) callLogs.value.reload()
  })
}

// Combined filters from filter bar + URL query parameters
const combinedFilters = computed(() => {
  const filters = {}

  // Status filter — filter bar takes priority over URL
  const status = activeStatus.value || route.query.status
  if (status) filters.status = status

  // Type filter
  const type = activeType.value || route.query.type
  if (type) filters.type = type

  // Date range filter — filter bar uses start_time, URL uses creation
  const fromDate = activeStartDate.value || route.query.from_date
  const toDate = activeEndDate.value || route.query.to_date
  if (fromDate && toDate) {
    filters.start_time = ['Between', [fromDate, toDate]]
  } else if (fromDate) {
    filters.start_time = ['>=', fromDate]
  } else if (toDate) {
    filters.start_time = ['<=', toDate]
  }

  // User filter from URL
  if (route.query.user && route.query.user !== '') {
    const user = route.query.user
    if (type === 'Incoming') {
      filters.receiver = user
    } else if (type === 'Outgoing') {
      filters.caller = user
    } else {
      filters._agent_user = user
    }
  }

  return filters
})

// Watch for URL query param changes (dashboard card clicks)
watch(
  () => route.query,
  () => {
    nextTick(() => {
      if (viewControls.value && route.name === 'Call Logs') {
        if (viewControls.value.reload) {
          viewControls.value.reload()
        } else if (callLogs.value?.reload) {
          callLogs.value.reload()
        }
      }
    })
  },
  { deep: true }
)

const rows = computed(() => {
  if (
    !callLogs.value?.data?.data ||
    !['list', 'group_by'].includes(callLogs.value.data.view_type)
  )
    return []
  return callLogs.value?.data.data.map((callLog) => {
    let _rows = {}
    callLogs.value?.data.rows.forEach((row) => {
      _rows[row] = getCallLogDetail(row, callLog, callLogs.value?.data.columns)
    })
    return _rows
  })
})

const showCallLogDetailModal = ref(false)
const callLog = ref({})

function showCallLog(name) {
  showCallLogDetailModal.value = true
  callLog.value = createResource({
    url: 'crm.fcrm.doctype.crm_call_log.crm_call_log.get_call_log',
    params: { name },
    cache: ['call_log', name],
    auto: true,
  })
}

function createCallLog() {
  callLog.value = {}
  showCallLogModal.value = true
}

const openCallLogFromURL = () => {
  const searchParams = new URLSearchParams(window.location.search)
  const callLogName = searchParams.get('open')

  if (callLogName) {
    showCallLog(callLogName)
    searchParams.delete('open')
    window.history.replaceState(null, '', window.location.pathname)
  }
}
</script>

