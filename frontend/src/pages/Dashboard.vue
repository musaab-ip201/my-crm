<template>
  <div class="flex flex-col h-full overflow-hidden">
    <LayoutHeader>
      <template #left-header>
        <ViewBreadcrumbs routeName="Dashboard" />
      </template>
      <template #right-header>
        <Button
          v-if="!editing"
          :label="__('Export')"
          :iconLeft="LucideDownload"
          @click="exportDashboard"
        />
        <Button
          v-if="!editing"
          :label="__('Refresh')"
          :iconLeft="LucideRefreshCcw"
          @click="dashboardItems.reload"
        />
        <Button
          v-if="!editing && isAdmin()"
          :label="__('Edit')"
          :iconLeft="LucidePenLine"
          @click="enableEditing"
        />
        <Button
          v-if="editing"
          :label="__('Chart')"
          iconLeft="plus"
          @click="showAddChartModal = true"
        />
        <Button
          v-if="editing && isAdmin()"
          :label="__('Reset to default')"
          :iconLeft="LucideUndo2"
          @click="resetToDefault"
        />
        <Button v-if="editing" :label="__('Cancel')" @click="cancel" />
        <Button
          v-if="editing"
          variant="solid"
          :label="__('Save')"
          :disabled="!dirty"
          :loading="saveDashboard.loading"
          @click="save"
        />
      </template>
    </LayoutHeader>

    <div class="p-5 pb-2 flex flex-wrap items-center gap-4">
      <Dropdown
        v-if="!showDatePicker"
        :options="options"
        class="form-control"
        v-model="preset"
        :placeholder="__('Select Range')"
        :button="{
          label: __(preset),
          class:
            '!w-full justify-start [&>span]:mr-auto [&>svg]:text-ink-gray-5 ',
          variant: 'outline',
          iconRight: 'chevron-down',
          iconLeft: 'calendar',
        }"
      />
      <DateRangePicker
        v-else
        class="!w-48"
        ref="datePickerRef"
        :value="filters.period"
        variant="outline"
        :placeholder="__('Period')"
        @change="
          (v) =>
            updateFilter('period', v, () => {
              showDatePicker = false
              if (!v) {
                filters.period = getLastXDays()
                preset = 'Last 30 Days'
              } else {
                preset = formatter(v)
              }
            })
        "
        :formatter="formatRange"
      >
        <template #prefix>
          <LucideCalendar class="size-4 text-ink-gray-5 mr-2" />
        </template>
      </DateRangePicker>

      <!-- Department Filter -->
      <div v-if="isAdmin() || isManager()" class="relative">
        <select
          v-model="filters.department"
          @change="onDepartmentChange"
          class="h-8 pl-3 pr-8 text-sm rounded-lg border border-outline-gray-2 bg-surface-white dark:bg-gray-800 text-ink-gray-8 dark:text-gray-200 appearance-none cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          <option value="">{{ __('All Departments') }}</option>
          <option
            v-for="d in departmentList.data || []"
            :key="d.name"
            :value="d.name"
          >
            {{ d.name }}
          </option>
        </select>
        <FeatherIcon
          name="chevron-down"
          class="absolute right-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-ink-gray-5 pointer-events-none"
        />
      </div>

      <!-- User Filter -->
      <Link
        v-if="isAdmin() || isManager()"
        class="form-control w-48"
        variant="outline"
        :value="filters.user && getUser(filters.user).full_name"
        doctype="User"
        :filters="userLinkFilters"
        @change="(v) => updateFilter('user', v)"
        :placeholder="__('Sales user')"
        :hideMe="true"
      >
        <template #prefix>
          <UserAvatar
            v-if="filters.user"
            class="mr-2"
            :user="filters.user"
            size="sm"
          />
        </template>
        <template #item-prefix="{ option }">
          <UserAvatar class="mr-2" :user="option.value" size="sm" />
        </template>
        <template #item-label="{ option }">
          <Tooltip :text="option.value">
            <div class="cursor-pointer text-gray-800 dark:text-white">
              {{ getUser(option.value).full_name }}
            </div>
          </Tooltip>
        </template>
      </Link>
    </div>

    <!-- Department Users Pills -->
    <div
      v-if="filters.department && departmentUsers.length"
      class="px-5 pb-2 flex flex-wrap items-center gap-2"
    >
      <span class="text-xs text-ink-gray-5 font-medium mr-1">{{ __('Team') }}:</span>
      <span
        v-for="u in departmentUsers"
        :key="u.name"
        class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border transition-colors"
        :class="
          filters.user === u.name
            ? 'bg-blue-50 dark:bg-blue-900/30 border-blue-300 dark:border-blue-600 text-blue-700 dark:text-blue-300'
            : 'bg-surface-gray-2 dark:bg-gray-700 border-outline-gray-1 dark:border-gray-600 text-ink-gray-7 dark:text-gray-300 hover:bg-surface-gray-3 dark:hover:bg-gray-600 cursor-pointer'
        "
        @click="toggleUserFilter(u.name)"
      >
        <UserAvatar :user="u.name" size="xs" />
        {{ u.full_name }}
      </span>
    </div>

    <div class="w-full overflow-y-scroll">
      <DashboardGrid
        class="pt-1"
        v-if="!dashboardItems.loading && dashboardItems.data"
        v-model="dashboardItems.data"
        :editing="editing"
      />
    </div>
  </div>
  <AddChartModal
    v-if="showAddChartModal"
    v-model="showAddChartModal"
    v-model:items="dashboardItems.data"
  />
</template>

<script setup lang="ts">
import AddChartModal from '@/components/Dashboard/AddChartModal.vue'
import LucideRefreshCcw from '~icons/lucide/refresh-ccw'
import LucideUndo2 from '~icons/lucide/undo-2'
import LucidePenLine from '~icons/lucide/pen-line'
import LucideDownload from '~icons/lucide/download'
import DashboardGrid from '@/components/Dashboard/DashboardGrid.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Link from '@/components/Controls/Link.vue'
import { usersStore } from '@/stores/users'
import { copy } from '@/utils'
import { getLastXDays, formatter, formatRange } from '@/utils/dashboard'
import {
  usePageMeta,
  createResource,
  DateRangePicker,
  Dropdown,
  Tooltip,
  FeatherIcon,
  call,
} from 'frappe-ui'
import { ref, reactive, computed, provide, watch } from 'vue'
import { useRoute } from 'vue-router'

const { users, getUser, isManager, isAdmin } = usersStore()

const editing = ref(false)

const showDatePicker = ref(false)
const datePickerRef = ref(null)
const preset = ref('Last 30 Days')
const showAddChartModal = ref(false)

const route = useRoute()

const filters = reactive({
  period: getLastXDays(),
  user:
    route.query.user && typeof route.query.user === 'string'
      ? route.query.user
      : null,
  department: '',
})

const departmentUsers = ref([])

const departmentList = createResource({
  url: 'crm.api.dashboard.get_departments',
  auto: true,
})

const userLinkFilters = computed(() => {
  if (filters.department) {
    // Department selected: only show users from that department (or none if empty)
    const deptUserNames = departmentUsers.value.map((u: any) => u.name)
    return {
      name: ['in', deptUserNames.length ? deptUserNames : ['__no_match__']],
    }
  }
  return {
    name: ['in', users.data?.crmUsers?.map((u: any) => u.name)],
  }
})

function onDepartmentChange() {
  filters.user = null
  if (filters.department) {
    call('crm.api.dashboard.get_department_users_list', {
      department: filters.department,
    }).then((data: any) => {
      departmentUsers.value = data || []
      dashboardItems.reload()
    })
  } else {
    departmentUsers.value = []
    dashboardItems.reload()
  }
}

function toggleUserFilter(userName: string) {
  if (filters.user === userName) {
    filters.user = null
  } else {
    filters.user = userName
  }
  dashboardItems.reload()
}

const fromDate = computed(() => {
  if (!filters.period) return null
  return filters.period.split(',')[0]
})

const toDate = computed(() => {
  if (!filters.period) return null
  return filters.period.split(',')[1]
})

function updateFilter(key: string, value: any, callback?: () => void) {
  filters[key] = value
  callback?.()
  dashboardItems.reload()
}

const options = computed(() => [
  {
    group: 'Presets',
    hideLabel: true,
    items: [
      {
        label: 'Last 7 Days',
        onClick: () => {
          preset.value = 'Last 7 Days'
          filters.period = getLastXDays(7)
          dashboardItems.reload()
        },
      },
      {
        label: 'Last 30 Days',
        onClick: () => {
          preset.value = 'Last 30 Days'
          filters.period = getLastXDays(30)
          dashboardItems.reload()
        },
      },
      {
        label: 'Last 60 Days',
        onClick: () => {
          preset.value = 'Last 60 Days'
          filters.period = getLastXDays(60)
          dashboardItems.reload()
        },
      },
      {
        label: 'Last 90 Days',
        onClick: () => {
          preset.value = 'Last 90 Days'
          filters.period = getLastXDays(90)
          dashboardItems.reload()
        },
      },
    ],
  },
  {
    label: 'Custom Range',
    onClick: () => {
      showDatePicker.value = true
      setTimeout(() => datePickerRef.value?.open(), 0)
      preset.value = 'Custom Range'
      filters.period = null // Reset period to allow custom date selection
    },
  },
])

const dashboardItems = createResource({
  url: 'crm.api.dashboard.get_dashboard',
  makeParams() {
    return {
      from_date: fromDate.value,
      to_date: toDate.value,
      user: filters.user,
      department: filters.department,
    }
  },
  auto: true,
})

const dirty = computed(() => {
  if (!editing.value) return false
  return JSON.stringify(dashboardItems.data) !== JSON.stringify(oldItems.value)
})

const oldItems = ref([])

provide('fromDate', fromDate)
provide('toDate', toDate)
provide('filters', filters)

function enableEditing() {
  editing.value = true
  oldItems.value = copy(dashboardItems.data)
}

function cancel() {
  editing.value = false
  dashboardItems.data = copy(oldItems.value)
}

const saveDashboard = createResource({
  url: 'frappe.client.set_value',
  method: 'POST',
  onSuccess: () => {
    dashboardItems.reload()
    editing.value = false
  },
})

function save() {
  const dashboardItemsCopy = copy(dashboardItems.data)

  dashboardItemsCopy.forEach((item: any) => {
    delete item.data
  })

  saveDashboard.submit({
    doctype: 'CRM Dashboard',
    name: 'Manager Dashboard',
    fieldname: 'layout',
    value: JSON.stringify(dashboardItemsCopy),
  })
}

function resetToDefault() {
  createResource({
    url: 'crm.api.dashboard.reset_to_default',
    auto: true,
    onSuccess: () => {
      dashboardItems.reload()
      editing.value = false
    },
  })
}

function exportDashboard() {
  call('crm.api.dashboard.export_dashboard_data', {
    from_date: fromDate.value,
    to_date: toDate.value,
    user: filters.user || '',
    department: filters.department || '',
  }).then((result: any) => {
    if (!result || !result.file_data) return

    // Decode base64 to binary
    const byteChars = atob(result.file_data)
    const byteNumbers = new Array(byteChars.length)
    for (let i = 0; i < byteChars.length; i++) {
      byteNumbers[i] = byteChars.charCodeAt(i)
    }
    const byteArray = new Uint8Array(byteNumbers)
    const blob = new Blob([byteArray], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    })

    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = result.file_name || 'CRM_Dashboard.xlsx'
    a.click()
    URL.revokeObjectURL(url)
  })
}

usePageMeta(() => {
  return { title: __('CRM Dashboard') }
})
</script>
