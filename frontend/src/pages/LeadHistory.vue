<template>
  <div class="flex flex-col h-full overflow-hidden">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs
          :items="[
            { label: __('Lead History'), route: { name: 'LeadHistory' } },
          ]"
        />
      </template>
      <template #right-header>
        <div class="flex items-center gap-2">
          <Button
            v-if="filteredLeads.length > 0"
            :label="__('Export')"
            variant="outline"
            :iconLeft="LucideDownload"
            @click="exportToExcel"
            :loading="exportLoading"
          />
          <Button
            :label="__('Refresh')"
            :iconLeft="LucideRefreshCcw"
            @click="loadHistory"
          />
        </div>
      </template>
    </LayoutHeader>

    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar for Admins / Managers -->
      <div
        v-if="isAdmin() || isManager()"
        class="w-64 max-md:w-16 border-r overflow-y-auto flex flex-col shrink-0 transition-all duration-300 bg-white border-gray-200 dark:bg-gray-900 dark:border-gray-700 sidebar-scroll"
      >
        <!-- Header -->
        <div
          class="px-4 py-3 text-sm font-semibold sticky top-0 z-10 border-b bg-white/90 text-gray-900 border-gray-200 dark:bg-gray-900/80 dark:text-gray-100 dark:border-gray-700 backdrop-blur"
        >
          <span class="max-md:hidden">{{ __('Team Members') }}</span>
        </div>

        <!-- Global History -->
        <button
          @click="onUserChange(null)"
          :class="[
            'flex items-center gap-3 px-4 py-3.5 text-left rounded-lg mx-2 my-1',
            'transition-all duration-200 ease-in-out group',
            'hover:bg-gray-100 dark:hover:bg-gray-800 hover:shadow-sm',
            !selectedUser ? 'bg-gray-100 dark:bg-gray-800 shadow-sm' : '',
          ]"
        >
          <div
            :class="[
              'w-9 h-9 rounded-lg flex items-center justify-center transition-all',
              !selectedUser
                ? 'bg-gray-900 text-white dark:bg-white dark:text-gray-900'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 group-hover:bg-gray-200 dark:group-hover:bg-gray-700',
            ]"
          >
            👤
          </div>

          <div class="flex flex-col max-md:hidden">
            <span
              :class="[
                'text-sm font-semibold',
                !selectedUser
                  ? 'text-gray-900 dark:text-white'
                  : 'text-gray-700 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white',
              ]"
            >
              {{ __('Global History') }}
            </span>
            <span
              class="text-[10px] uppercase tracking-wider text-gray-500 dark:text-gray-400"
            >
              {{ __('All Members') }}
            </span>
          </div>
        </button>

        <!-- Divider -->
        <div class="h-px bg-gray-200 dark:bg-gray-700 mx-3 my-2"></div>

        <!-- Users -->
        <button
          v-for="u in usersList"
          :key="u.name"
          @click="onUserChange(u.name)"
          :class="[
            'flex items-center gap-3 px-4 py-3 text-left rounded-lg mx-2 my-1 relative',
            'transition-all duration-200 ease-in-out group',
            'hover:bg-gray-100 dark:hover:bg-gray-800 hover:shadow-sm',
            selectedUser === u.name
              ? 'bg-gray-100 dark:bg-gray-800 shadow-sm'
              : '',
          ]"
        >
          <!-- Active indicator -->
          <div
            v-if="selectedUser === u.name"
            class="absolute left-0 top-2 bottom-2 w-1.5 rounded-r-full bg-gray-900 dark:bg-white"
          ></div>

          <!-- Avatar -->
          <UserAvatar
            :user="u.name"
            size="lg"
            class="shrink-0 transition-all duration-200 group-hover:scale-105 group-hover:shadow-sm"
          />

          <!-- Text -->
          <div
            class="flex flex-col justify-center overflow-hidden max-md:hidden"
          >
            <span
              :class="[
                'text-sm font-semibold truncate',
                selectedUser === u.name
                  ? 'text-gray-900 dark:text-white'
                  : 'text-gray-700 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white',
              ]"
            >
              {{ u.full_name }}
            </span>
            <span class="text-xs text-gray-500 dark:text-gray-400 truncate">
              {{ u.name }}
            </span>
          </div>
        </button>
      </div>

      <!-- Main Content Area -->
      <div class="flex-1 overflow-y-auto p-6 bg-base">
        <!-- Loading state -->
        <div v-if="loading" class="flex h-full items-center justify-center">
          <div class="text-base text-ink-gray-4">
            {{ __('Loading lead history...') }}
          </div>
        </div>

        <div v-else>
          <!-- Stats cards - Global view -->
          <div
            v-if="viewType === 'global'"
            class="grid grid-cols-1 sm:grid-cols-2 gap-5 mb-8"
          >
            <!-- Total Routed -->
            <div
              class="group rounded-xl border p-5 transition-all duration-200 bg-white border-gray-200 dark:bg-gray-900 dark:border-gray-700 hover:shadow-md hover:-translate-y-0.5"
            >
              <div class="flex items-center justify-between mb-3">
                <span
                  class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 truncate max-w-[80%]"
                >
                  {{ __('Total Routed') }}
                </span>

                <div class="w-2 h-2 rounded-full bg-blue-500 shrink-0"></div>
              </div>

              <div class="text-3xl font-bold text-gray-900 dark:text-white">
                {{ historyData?.total_routed || leads.length }}
              </div>
            </div>

            <!-- Working -->
            <div
              class="group rounded-xl border p-5 transition-all duration-200 bg-white border-gray-200 dark:bg-gray-900 dark:border-gray-700 hover:shadow-md hover:-translate-y-0.5"
            >
              <div class="flex items-center justify-between mb-3">
                <span
                  class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 truncate max-w-[80%]"
                >
                  {{ __('Working') }}
                </span>

                <div class="w-2 h-2 rounded-full bg-amber-500"></div>
              </div>

              <div class="text-3xl font-bold text-amber-500">
                {{ historyData?.working_count || 0 }}
              </div>
            </div>
          </div>

          <!-- Stats cards - Personal view -->

          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-5 mb-8">
            <!-- Viewing History card -->
            <div
              v-if="historyData?.full_name && selectedUser"
              class="group rounded-xl border p-5 transition-all duration-200 bg-white border-gray-200 dark:bg-gray-900 dark:border-gray-700 hover:shadow-md hover:-translate-y-0.5 flex items-center gap-3 overflow-hidden"
            >
              <UserAvatar
                :user="selectedUser"
                size="lg"
                class="flex-shrink-0"
              />
              <div class="flex flex-col min-w-0">
                <span
                  class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 truncate"
                >
                  {{ __('Viewing History Of') }}
                </span>
                <span
                  class="text-lg font-bold text-gray-900 dark:text-white leading-tight truncate"
                >
                  {{ historyData.full_name }}
                </span>
              </div>
            </div>
            <!-- Total Leads Handled card -->
            <div
              class="group rounded-xl border p-5 transition-all duration-200 bg-white border-gray-200 dark:bg-gray-900 dark:border-gray-700 hover:shadow-md hover:-translate-y-0.5"
            >
              <div
                class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-2"
              >
                {{ __('Total Leads Handled') }}
              </div>
              <div class="text-3xl font-bold text-gray-900 dark:text-white">
                {{ leads.length }}
              </div>
            </div>
          </div>

          <div
            class="mb-6 flex flex-wrap items-end gap-4 bg-white dark:bg-gray-900 px-5 py-4 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-md"
          >
            <!-- Action -->
            <div class="flex flex-col gap-2 min-w-[170px] relative dropdown">
              <label
                class="text-[10px] font-semibold text-gray-500 uppercase tracking-wider ml-1"
              >
                Action
              </label>

              <button
                @click="showActionDropdown = !showActionDropdown"
                class="h-11 w-full flex items-center justify-between px-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm hover:border-gray-400 transition"
              >
                <div
                  class="flex items-center gap-2 text-sm text-balck dark:text-white"
                >
                  <FeatherIcon name="settings" class="w-4 h-4 text-gray-400" />
                  <span>{{ selectedActionLabel || 'All Actions' }}</span>
                </div>
                <FeatherIcon
                  name="chevron-down"
                  class="w-4 h-4 text-gray-500"
                />
              </button>

              <div
                v-if="showActionDropdown"
                class="absolute z-50 mt-3 w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl shadow-xl transition-all duration-200 ease-out animate-in fade-in slide-in-from-top-1"
              >
                <div
                  v-for="option in actionOptions"
                  :key="option.value"
                  @click="selectAction(option)"
                  class="px-3 py-2 text-sm cursor-pointer text-balck dark:text-white flex items-center justify-between hover:bg-blue-50 dark:hover:bg-gray-800 transition-colors rounded-2xl"
                >
                  <span>{{ option.label }}</span>

                  <FeatherIcon
                    v-if="filterAction === option.value"
                    name="check"
                    class="w-4 h-4 text-blue-500"
                  />
                </div>
              </div>
            </div>

            <!-- Search -->
            <div class="flex flex-col gap-2 flex-1 min-w-[220px] max-w-[300px]">
              <label
                class="text-[10px] font-semibold text-gray-500 uppercase tracking-wider ml-1"
              >
                Search
              </label>

              <input
                v-model="searchQuery"
                type="text"
                placeholder="Lead name or ID..."
                class="h-11 text-sm w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 px-3"
              />
            </div>

            <!-- From Date -->
            <div class="flex flex-col gap-2 min-w-[150px]">
              <label
                class="text-[10px] font-semibold text-gray-500 uppercase tracking-wider ml-1"
              >
                From Date
              </label>
              <input
                v-model="filterDateFrom"
                type="date"
                class="h-11 text-sm w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 px-3 text-gray-700 dark:text-gray-200"
              />
            </div>

            <!-- To Date -->
            <div class="flex flex-col gap-2 min-w-[150px]">
              <label
                class="text-[10px] font-semibold text-gray-500 uppercase tracking-wider ml-1"
              >
                To Date
              </label>
              <input
                v-model="filterDateTo"
                type="date"
                class="h-11 text-sm w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 px-3 text-gray-700 dark:text-gray-200"
              />
            </div>

            <!-- Clear -->
            <div class="flex items-end">
              <button
                v-if="filterAction || searchQuery || filterDateFrom || filterDateTo"
                @click="clearFilters"
                class="h-11 px-4 text-sm rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition"
              >
                Clear Filters
              </button>
            </div>
          </div>
          <!-- Previously Handled Leads table -->
          <div>
            <h3
              class="text-base font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center justify-between"
            >
              <!-- Left Side -->
              <div class="flex items-center gap-2">
                <span class="p-1.5 rounded-md bg-gray-100 dark:bg-gray-800"
                  >📋</span
                >

                <span>
                  {{
                    viewType === 'global'
                      ? __('All Lead Routing History')
                      : __('Previously Handled Leads')
                  }}
                </span>
              </div>

              <!-- Right Side Count Badge -->
              <span
                class="text-xs font-medium px-2.5 py-1 rounded-full bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-300"
              >
                {{ filteredLeads.length }} records
              </span>
            </h3>
            <div
              v-if="filteredLeads.length"
              class="rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 shadow-sm flex flex-col h-[300px]"
            >
              <div class="flex-1 overflow-y-auto overflow-x-auto rounded-2xl">
                <table class="w-full min-w-[900px]">
                  <!-- HEADER -->
                  <thead class="sticky top-0 z-10 bg-gray-50 dark:bg-gray-800">
                    <tr
                      class="bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700"
                    >
                      <th
                        class="px-5 py-3 text-left text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                      >
                        {{ __('Lead ID') }}
                      </th>

                      <th
                        class="px-5 py-3 text-left text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                      >
                        {{ __('Lead Name') }}
                      </th>

                      <th
                        class="px-5 py-3 text-left text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                      >
                        {{ __('Department') }}
                      </th>

                      <th
                        class="px-5 py-3 text-left text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                      >
                        {{
                          viewType === 'global'
                            ? __('Last Action')
                            : __('Action Taken')
                        }}
                      </th>

                      <th
                        class="px-5 py-3 text-left text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                      >
                        {{ __('Status') }}
                      </th>

                      <th
                        v-if="viewType === 'global'"
                        class="px-5 py-3 text-left text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                      >
                        {{ __('Last Handled By') }}
                      </th>

                      <th
                        class="px-5 py-3 text-left text-[11px] font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider w-[180px]"
                      >
                        {{ __('Last Updated') }}
                      </th>
                    </tr>
                  </thead>

                  <!-- BODY -->
                  <tbody>
                    <tr
                      v-for="lead in paginatedLeads"
                      :key="lead.name"
                      @click="openLead(lead.name)"
                      class="border-b border-gray-100 dark:border-gray-800 last:border-0 cursor-pointer group transition-all duration-200 hover:bg-gray-50 dark:hover:bg-gray-800/70 hover:shadow-sm odd:bg-white even:bg-gray-50 dark:odd:bg-gray-900 dark:even:bg-gray-800/40"
                    >
                      <!-- Lead ID -->
                      <td class="px-5 py-3">
                        <span
                          class="text-sm font-semibold text-blue-600 group-hover:underline group-hover:text-blue-700 transition"
                        >
                          {{ lead.name }}
                        </span>
                      </td>

                      <!-- Lead Name -->
                      <td
                        class="px-5 py-3 text-sm text-gray-700 dark:text-gray-300 font-medium"
                      >
                        {{ lead.lead_name || '—' }}
                      </td>

                      <!-- Department -->
                      <td class="px-5 py-3">
                        <Badge
                          variant="subtle"
                          :label="lead.current_department || '—'"
                          theme="blue"
                        />
                      </td>

                      <!-- Action -->
                      <td class="px-5 py-3">
                        <Badge
                          v-if="getLeadAction(lead)"
                          variant="subtle"
                          :label="getActionLabel(getLeadAction(lead))"
                          :theme="getActionTheme(getLeadAction(lead))"
                        />
                        <span v-else class="text-sm text-gray-400">—</span>
                      </td>

                      <!-- Status -->
                      <td class="px-5 py-3">
                        <span
                          :class="getStatusClasses(getDisplayStatus(lead))"
                          class="px-2 py-1 text-xs font-medium rounded-full"
                        >
                          {{ getDisplayStatus(lead) }}
                        </span>
                      </td>

                      <!-- Last Handled By -->
                      <td
                        v-if="viewType === 'global'"
                        class="px-5 py-3 text-sm text-gray-600 dark:text-gray-400 font-medium"
                      >
                        {{ lead.last_handled_by_name || '—' }}
                      </td>

                      <!-- Last Updated -->
                      <td class="px-5 py-3 text-xs text-gray-500">
                        <Tooltip :text="timeAgo(lead.modified)">
                          <div class="flex items-center gap-2 justify-end">
                            <span
                              class="w-1.5 h-1.5 rounded-full bg-gray-400"
                            ></span>
                            <span
                              class="group-hover:text-gray-700 dark:group-hover:text-gray-200 transition whitespace-nowrap"
                            >
                              {{ formatDateTime(lead.modified) }}
                            </span>
                          </div>
                        </Tooltip>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div
                v-if="filteredLeads.length"
                class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between px-4 py-3 rounded-2xl"
              >
                <!-- Left info -->
                <div class="text-sm text-gray-500">
                  Showing
                  <span class="font-medium">
                    {{ (currentPage - 1) * pageSize + 1 }}
                  </span>
                  -
                  <span class="font-medium">
                    {{ Math.min(currentPage * pageSize, filteredLeads.length) }}
                  </span>
                  of
                  <span class="font-medium">{{ filteredLeads.length }}</span>
                </div>

                <!-- Buttons -->
                <!-- <div class="flex items-center gap-2">
                  <button
                    @click="currentPage--"
                    :disabled="currentPage === 1"
                    class="px-3 py-1.5 text-sm rounded-lg border border-gray-300 dark:border-gray-600 disabled:opacity-40 hover:bg-gray-100 dark:hover:bg-gray-800"
                  >
                    Prev
                  </button>

                  <span class="text-sm font-medium px-2">
                    {{ currentPage }} / {{ totalPages }}
                  </span>

                  <button
                    @click="currentPage++"
                    :disabled="currentPage === totalPages"
                    class="px-3 py-1.5 text-sm rounded-lg border border-gray-300 dark:border-gray-600 disabled:opacity-40 hover:bg-gray-100 dark:hover:bg-gray-800"
                  >
                    Next
                  </button>
                </div> -->
                <div class="flex items-center gap-2">
                  <button
                    @click="currentPage--"
                    :disabled="currentPage === 1"
                    class="px-3 py-1.5 text-sm rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-900 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-200"
                  >
                    Prev
                  </button>

                  <span
                    class="text-sm font-medium px-2 text-gray-800 dark:text-gray-200"
                  >
                    {{ currentPage }} / {{ totalPages }}
                  </span>

                  <button
                    @click="currentPage++"
                    :disabled="currentPage === totalPages"
                    class="px-3 py-1.5 text-sm rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-900 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-200"
                  >
                    Next
                  </button>
                </div>
              </div>
            </div>
            <div
              v-else
              class="flex items-center justify-center rounded-lg border border-dashed py-8"
            >
              <span class="text-sm text-ink-gray-4">
                {{
                  filterAction || searchQuery
                    ? __('No leads match the selected filters')
                    : viewType === 'global'
                      ? __('No routed leads found')
                      : __('No lead history found')
                }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import LucideRefreshCcw from '~icons/lucide/refresh-ccw'
import LucideDownload from '~icons/lucide/download'
import LayoutHeader from '@/components/LayoutHeader.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import Link from '@/components/Controls/Link.vue'
import { usersStore } from '@/stores/users'
import { timeAgo, formatDate } from '@/utils'
import {
  Breadcrumbs,
  Badge,
  Tooltip,
  Button,
  usePageMeta,
  call,
} from 'frappe-ui'
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const { getUser, isManager, isAdmin, users } = usersStore()

const usersList = ref([])
const loading = ref(false)
const exportLoading = ref(false)
const selectedUser = ref(null)
const historyData = ref(null)
const leads = ref([])
const viewType = ref('global')
const workingCount = ref(0)
const totalRouted = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const paginatedLeads = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredLeads.value.slice(start, start + pageSize.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredLeads.value.length / pageSize.value)
})

async function loadUsers() {
  try {
    const response = await call(
      'lead_routing.api.lead_history.get_users_with_lead_history',
    )
    usersList.value = response.users || []
  } catch (e) {
    console.error('Failed to load users:', e)

    usersList.value = users.data?.crmUsers || []
  }
}

// Filters
const filterAction = ref('')
const searchQuery = ref('')
const filterDateFrom = ref('')
const filterDateTo = ref('')
watch([filterAction, searchQuery, filterDateFrom, filterDateTo], () => {
  currentPage.value = 1
})

const showActionDropdown = ref(false)

const actionOptions = [
  { label: 'All Action', value: '' },
  { label: 'Mark Done', value: 'Forward' },
  { label: 'Send Back', value: 'Backward' },
  { label: 'Reject', value: 'Reject' },
  { label: 'Transfer', value: 'Manager Override' },
  { label: 'Initial', value: 'Initial' },
]

const selectedActionLabel = computed(
  () => actionOptions.find((o) => o.value === filterAction.value)?.label || '',
)
const selectAction = (option) => {
  filterAction.value = option.value
  showActionDropdown.value = false
}

const toggleAction = () => {
  showActionDropdown.value = !showActionDropdown.value
}

const filteredLeads = computed(() => {
  let result = leads.value
  if (filterAction.value) {
    result = result.filter((l) => {
      const action = l.last_action || l.user_action
      return action === filterAction.value
    })
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(
      (l) =>
        (l.name && l.name.toLowerCase().includes(q)) ||
        (l.lead_name && l.lead_name.toLowerCase().includes(q)),
    )
  }
  if (filterDateFrom.value) {
    const from = new Date(filterDateFrom.value)
    from.setHours(0, 0, 0, 0)
    result = result.filter((l) => {
      const d = new Date(l.modified)
      return d >= from
    })
  }
  if (filterDateTo.value) {
    const to = new Date(filterDateTo.value)
    to.setHours(23, 59, 59, 999)
    result = result.filter((l) => {
      const d = new Date(l.modified)
      return d <= to
    })
  }
  return result
})

function clearFilters() {
  filterAction.value = ''
  searchQuery.value = ''
  filterDateFrom.value = ''
  filterDateTo.value = ''
}

async function loadHistory() {
  loading.value = true
  try {
    const args = {}
    if (selectedUser.value) {
      args.user = selectedUser.value
    }
    const data = await call(
      'lead_routing.api.lead_history.get_my_lead_history',
      args,
    )
    historyData.value = data
    leads.value = data.leads || []
    viewType.value = data.view_type || 'global'
    workingCount.value = data.working_count || 0
    totalRouted.value = data.total_routed || 0
  } catch (e) {
    console.error('Failed to load lead history:', e)
    leads.value = []
  } finally {
    loading.value = false
  }
}

async function exportToExcel() {
  exportLoading.value = true
  try {
    // Prepare filters object
    const filters = {
      action: filterAction.value || '',
      search: searchQuery.value || '',
      date_from: filterDateFrom.value || '',
      date_to: filterDateTo.value || '',
    }

    // Build URL parameters
    const params = new URLSearchParams({
      filters: JSON.stringify(filters)
    })
    
    // Add user parameter if viewing specific user's history
    if (selectedUser.value) {
      params.append('user', selectedUser.value)
    }

    // Open download URL in new window
    const downloadUrl = `/api/method/lead_routing.api.lead_history.export_lead_history_to_excel?${params.toString()}`
    window.open(downloadUrl, '_blank')

    frappe.show_alert({
      message: __('Lead history export started'),
      indicator: 'green'
    })

  } catch (error) {
    console.error('Export failed:', error)
    frappe.show_alert({
      message: __('Export failed. Please try again.'),
      indicator: 'red'
    })
  } finally {
    exportLoading.value = false
  }
}

function onUserChange(value) {
  selectedUser.value = value
  clearFilters()
  loadHistory()
}

function openLead(leadId) {
  router.push({ name: 'Lead', params: { leadId } })
}

function getLeadAction(lead) {
  return lead.last_action || lead.user_action || null
}

const actionLabels = {
  Forward: 'Mark Done',
  Backward: 'Send Back',
  Reject: 'Reject to Onboarding',
  'Manager Override': 'Manager Override',
  Initial: 'Initial Assignment',
}

function getActionLabel(action) {
  return actionLabels[action] || action
}

function getActionTheme(action) {
  const themes = {
    Forward: 'green',
    Backward: 'orange',
    Reject: 'red',
    'Manager Override': 'blue',
    Initial: 'gray',
  }
  return themes[action] || 'gray'
}

function getDisplayStatus(lead) {
  // For personal view, show user-specific status based on their action
  if (viewType.value === 'personal') {
    const userAction = lead.user_action || lead.last_action
    
    if (userAction === 'Forward') {
      return 'Transferred'
    } else if (userAction === 'Backward') {
      return 'Sent Back'
    } else if (userAction === 'Reject') {
      return 'Rejected'
    } else if (userAction === 'Manager Override') {
      return 'Overridden'
    } else if (userAction === 'Initial') {
      return 'Assigned'
    } else {
      return 'Working'
    }
  }
  
  // For global view, use department/lead status
  return lead.department_status || lead.status || 'Working'
}

function getStatusClasses(status) {
  if (!status) return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'
  
  const s = status.toLowerCase()
  
  // User action statuses with high contrast colors
  if (s === 'transferred') {
    return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
  }
  if (s === 'sent back') {
    return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
  }
  if (s === 'rejected') {
    return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  if (s === 'overridden') {
    return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
  }
  if (s === 'assigned') {
    return 'bg-cyan-100 text-cyan-800 dark:bg-cyan-900 dark:text-cyan-200'
  }
  if (s === 'working') {
    return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
  }
  if (s === 'done' || s === 'completed') {
    return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
  }
  
  // Default
  return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'
}

function getStatusTheme(status) {
  if (!status) return 'gray'
  const s = status.toLowerCase()
  
  // User action statuses
  if (s === 'transferred') return 'blue'
  if (s === 'sent back') return 'orange'
  if (s === 'rejected') return 'red'
  if (s === 'overridden') return 'purple'
  if (s === 'assigned') return 'cyan'
  
  // Default statuses
  if (s === 'working') return 'orange'
  if (s === 'done' || s === 'completed') return 'green'
  
  return 'gray'
}

const handleClickOutside = (e) => {
  if (!e.target.closest('.dropdown')) {
    showActionDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  console.log(leads.value)
  loadUsers()
  loadHistory()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
function formatDateTime(dateString) {
  if (!dateString) return '—'
  const d = new Date(dateString)
  if (isNaN(d.getTime())) return dateString
  const day = d.getDate()
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  const month = months[d.getMonth()]
  const year = d.getFullYear()
  let hours = d.getHours()
  const mins = String(d.getMinutes()).padStart(2, '0')
  const ampm = hours >= 12 ? 'PM' : 'AM'
  hours = hours % 12 || 12
  return `${day} ${month} ${year}, ${hours}:${mins} ${ampm}`
}

usePageMeta(() => {
  if (viewType.value === 'global' && !selectedUser.value) {
    return { title: __('Lead History — All Routing Activity') }
  }
  if (historyData.value?.full_name) {
    return { title: __('Lead History: {0}', [historyData.value.full_name]) }
  }
  return { title: __('Lead History') }
})
</script>



