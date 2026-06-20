<template>
  <div v-if="loading || hasEnabledShifts" class="sidebar-hierarchy-menu bg-white dark:bg-[#313131]">
    <!-- Header -->
    <div class="menu-header">
      <div class="header-content text-black dark:text-gray-200">
        <h3>Shift Overview</h3>
        <span
          v-if="isFiltered"
          class="filter-badge hover:scale-110 transition"
          title="Showing only your team"
        >
          <UserIcon class="w-4 h-4" />
        </span>
      </div>

      <button @click="refreshData" class="refresh-btn" :disabled="loading">
        <RefreshIcon :class="{ 'animate-spin': loading }" />
      </button>
    </div>

    <!-- Shift List -->
    <div class="shift-list">
      <div v-for="shift in hierarchyData" :key="shift.name" class="shift-item">
        <!-- Shift Header -->
        <button
          class="shift-button"
          :class="{ expanded: expandedShifts.includes(shift.name) }"
          @click="toggleShift(shift.name)"
        >
          <div class="shift-content">
            <div class="shift-title">
              <ClockIcon class="icon" />
              <span class="shift-name">{{ shift.shift_name }}</span>
            </div>

            <div class="shift-meta">
              <span class="timing">
                {{ formatTime(shift.start_time) }} -
                {{ formatTime(shift.end_time) }}
              </span>

              <span class="duration">
                • {{ getShiftDuration(shift.start_time, shift.end_time) }}
              </span>

              <span class="count">
                [{{ shift.departments.length }} depts]
              </span>
            </div>
          </div>

          <ChevronDownIcon
            class="chevron"
            :class="{ rotated: expandedShifts.includes(shift.name) }"
          />
        </button>

        <!-- Departments -->
        <div
          v-if="expandedShifts.includes(shift.name)"
          class="departments-list"
        >
          <div
            v-for="dept in shift.departments"
            :key="dept.name"
            class="department-item"
          >
            <!-- Department Button -->
            <button
              class="department-button"
              :class="{ expanded: expandedDepartments.includes(dept.name) }"
              @click="toggleDepartment(dept.name)"
            >
              <div class="dept-content">
                <div class="dept-title">
                  <BuildingIcon class="icon" />
                  <span class="dept-name">
                    {{ dept.department_name }}
                  </span>
                </div>

                <div class="dept-meta">
                  <span class="dept-id">{{ dept.name }}</span>
                  <span class="count"> [{{ dept.teams.length }} teams] </span>
                </div>
              </div>

              <ChevronDownIcon
                class="chevron"
                :class="{ rotated: expandedDepartments.includes(dept.name) }"
              />
            </button>

            <!-- Teams -->
            <div
              v-if="expandedDepartments.includes(dept.name)"
              class="teams-list"
            >
              <div
                v-for="team in dept.teams"
                :key="team.name"
                class="team-item"
              >
                <!-- Team Button -->
                <button
                  class="team-button"
                  :class="{ expanded: expandedTeams.includes(team.name) }"
                  @click="toggleTeam(team.name)"
                >
                  <div class="team-content">
                    <div class="team-title">
                      <UsersIcon class="icon" />
                      <span class="team-name">
                        {{ team.team_name }}
                      </span>
                    </div>

                    <span class="count"> [{{ team.agents.length }}] </span>
                  </div>

                  <ChevronDownIcon
                    class="chevron"
                    :class="{ rotated: expandedTeams.includes(team.name) }"
                  />
                </button>

                <!-- Agents -->
                <div
                  v-if="expandedTeams.includes(team.name)"
                  class="agents-list"
                >
                  <div
                    v-for="agent in team.agents"
                    :key="agent.name"
                    class="agent-item-wrapper"
                  >
                    <!-- Agent Click -->
                    <div class="agent-item" @click="handleAgentClick(agent)">
                      <UserIcon class="icon" />
                      <span class="agent-name">{{ agent.full_name }}</span>
                    </div>
                  </div>

                  <div v-if="team.agents.length === 0" class="empty-message">
                    No agents
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State is intentionally hidden when there are no enabled shifts -->

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading...</p>
    </div>
  </div>

  <!-- Access Denied Popup -->
  <div
    v-if="selectedAgent"
    class="fixed inset-0 flex items-center justify-center bg-black/60 dark:bg-black/70 backdrop-blur-sm z-[9999]"
    @click="selectedAgent = null"
  >
    <div
      class="w-[92%] max-w-[380px] rounded-2xl p-8 flex flex-col items-center gap-5 shadow-2xl bg-white dark:bg-[#1f1f1f] border border-red-200 dark:border-red-900/40 text-center transition-all duration-200"
      @click.stop
    >
      <div
        class="w-20 h-20 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center text-red-600 dark:text-red-400 shadow-md"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="w-10 h-10"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
          />
        </svg>
      </div>

      <h3 class="text-2xl font-bold text-gray-900 dark:text-white">
        Access Denied
      </h3>
      <p class="text-[15px] text-[#090808] dark:text-gray-300 leading-relaxed">
        You do not have permission to view
        <strong class="text-gray-900 dark:text-white">
          {{ selectedAgent.full_name }} </strong
        >'s dashboard.
      </p>
      <button
        @click="selectedAgent = null"
        class="mt-2 w-full py-2.5 rounded-lg font-semibold bg-gray-900 text-white hover:bg-[#090808] hover:scale-[1.02] hover:shadow-lg dark:bg-white dark:text-black dark:hover:bg-gray-200 transition-all duration-200 ease-in-out"
      >
        Close
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import {usersStore} from '@/stores/users'
import { createResource } from 'frappe-ui'
import {
  RefreshCw as RefreshIcon,
  Clock as ClockIcon,
  Building2 as BuildingIcon,
  Users as UsersIcon,
  User as UserIcon,
  ChevronDown as ChevronDownIcon,
} from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()

const selectedAgent = ref(null)
const loading = ref(false)

const hierarchyData = ref([])

const expandedShifts = ref([])
const expandedDepartments = ref([])
const expandedTeams = ref([])

const isFiltered = ref(false)

const hasEnabledShifts = computed(() => {
  return Array.isArray(hierarchyData.value) && hierarchyData.value.length > 0
})

const sessionResource = createResource({
  url: 'frappe.auth.get_logged_user',
  auto: true,
})
const users=usersStore()
const currentUser = computed(() => sessionResource.data)

const isAdmin = computed(() => {
  return currentUser.value === 'Administrator' || users.isAdmin(currentUser.value)
})

function handleAgentClick(agent) {
  const sessionUser = currentUser.value?.toLowerCase()

  console.log('Session User:', sessionUser)
  console.log('Agent:', agent.name)

  const isSelf =
    sessionUser === agent.name?.toLowerCase() ||
    sessionUser === agent.email?.toLowerCase()

  if (isAdmin.value || isSelf) {
    router.push({
      name: 'Dashboard',
      query: { user: agent.name },
    })
  } else {
    selectedAgent.value = agent
  }
}

//API resource
const hierarchyResource = createResource({
  url: 'crm.api.hierarchy.get_hierarchy_tree',

  auto: false,

  onSuccess(data) {
    hierarchyData.value = data

    if (
      data.length === 1 &&
      data[0].departments.length === 1 &&
      data[0].departments[0].teams.length === 1
    ) {
      isFiltered.value = true
    }

    if (data.length > 0) {
      expandedShifts.value = [data[0].name]
    }
  },
})

//refresh
function refreshData() {
  loading.value = true

  hierarchyResource.reload().finally(() => {
    loading.value = false
  })
}

//expand controls
function toggleShift(name) {
  const i = expandedShifts.value.indexOf(name)

  i > -1 ? expandedShifts.value.splice(i, 1) : expandedShifts.value.push(name)
}

function toggleDepartment(name) {
  const i = expandedDepartments.value.indexOf(name)

  i > -1
    ? expandedDepartments.value.splice(i, 1)
    : expandedDepartments.value.push(name)
}

function toggleTeam(name) {
  const i = expandedTeams.value.indexOf(name)

  i > -1 ? expandedTeams.value.splice(i, 1) : expandedTeams.value.push(name)
}

//helpers
function formatTime(time) {
  if (!time) return ''

  const [h, m] = time.split(':')
  const hour = parseInt(h)

  const ampm = hour >= 12 ? 'PM' : 'AM'
  const displayHour = hour % 12 || 12

  return `${displayHour}:${m} ${ampm}`
}

function getShiftDuration(start, end) {
  if (!start || !end) return ''

  const s = parseInt(start.split(':')[0])
  const e = parseInt(end.split(':')[0])

  let d = e - s
  if (d < 0) d += 24

  return `${d}h`
}

//mounted
onMounted(async () => {
  refreshData()
})
</script>

<style scoped>
.sidebar-hierarchy-menu {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-right: 1px solid #e5e7eb;
  overflow-x: hidden;
  position: relative;
}
/* Header */
.menu-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.menu-header h3 {
  font-size: 0.9375rem;
  font-weight: 600;
  margin: 0;
}

.filter-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.25rem;
  height: 1.25rem;
  font-size: 0.75rem;
  background: #dbeafe;
  border-radius: 50%;
  cursor: help;
}

.refresh-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border: none;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: #f3f4f6;
  color: #111827;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-btn svg {
  width: 1rem;
  height: 1rem;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Shift List */
.shift-list {
  flex: 1;
  overflow: visible;
  padding: 0.5rem;
}
.shift-item {
  margin-bottom: 0.5rem;
}

/* Shift Button */
.shift-button {
  width: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 0.75rem;
  border: none;
  background: #eff6ff;
  color: #1e40af;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: all 0.2s;
  text-align: left;
}

.shift-button:hover {
  background: #dbeafe;
}

.shift-button.expanded {
  background: #3b82f6;
  color: white;
}

.shift-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.shift-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.shift-title .icon {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
}

.shift-name {
  font-size: 0.875rem;
  font-weight: 600;
}

.shift-meta {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;
  opacity: 0.9;
  flex-wrap: wrap;
}

.timing,
.duration,
.count {
  white-space: nowrap;
}

.chevron {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
  transition: transform 0.2s;
  margin-top: 0.125rem;
}

.chevron.rotated {
  transform: rotate(180deg);
}

/* Departments List */
.departments-list {
  margin-top: 0.375rem;
  margin-left: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.department-item {
  display: flex;
  flex-direction: column;
}

/* Department Button */
.department-button {
  width: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 0.625rem;
  border: none;
  background: #ecfdf5;
  color: #065f46;
  cursor: pointer;
  border-radius: 0.375rem;
  transition: all 0.2s;
  text-align: left;
}

.department-button:hover {
  background: #d1fae5;
}

.department-button.expanded {
  background: #10b981;
  color: white;
}

.dept-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.dept-title {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.dept-title .icon {
  width: 0.875rem;
  height: 0.875rem;
  flex-shrink: 0;
}

.dept-name {
  font-size: 0.8125rem;
  font-weight: 600;
}

.dept-meta {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.6875rem;
  opacity: 0.9;
}

.dept-id {
  font-family: monospace;
  font-size: 0.625rem;
}

/* Teams List */
.teams-list {
  margin-top: 0.375rem;
  margin-left: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.team-item {
  display: flex;
  flex-direction: column;
}

/* Team Button */
.team-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem;
  border: none;
  background: #fffbeb;
  color: #92400e;
  cursor: pointer;
  border-radius: 0.375rem;
  transition: all 0.2s;
  text-align: left;
}

.team-button:hover {
  background: #fef3c7;
}

.team-button.expanded {
  background: #f59e0b;
  color: white;
}

.team-content {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.team-title {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  flex: 1;
}

.team-title .icon {
  width: 0.75rem;
  height: 0.75rem;
  flex-shrink: 0;
}

.team-name {
  font-size: 0.75rem;
  font-weight: 600;
}

.team-content .count {
  font-size: 0.6875rem;
  opacity: 0.9;
}

/* Agents List */
.agents-list {
  margin-top: 0.25rem;
  margin-left: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.agent-item-wrapper {
  position: relative;
}

.agent-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.5rem;
  background: #f9fafb;
  border-radius: 0.25rem;
  font-size: 0.6875rem;
  color: #374151;
  transition: all 0.2s;
  text-decoration: none;
  cursor: pointer;
}

.agent-item:hover {
  background: #e0e7ff;
  color: #4f46e5;
}

.agent-item:hover .icon {
  color: #4f46e5;
}

.agent-item .icon {
  width: 0.75rem;
  height: 0.75rem;
  color: #6b7280;
  flex-shrink: 0;
  transition: color 0.2s;
}

.agent-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Agent Actions Dropdown */
.agent-actions {
  position: absolute;
  left: 100%;
  top: 0;
  margin-left: 0.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 0.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  z-index: 1000;
  min-width: 120px;
}

.action-link {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.5rem;
  font-size: 0.6875rem;
  color: #374151;
  text-decoration: none;
  border-radius: 0.25rem;
  transition: all 0.2s;
  white-space: nowrap;
}

.action-link:hover {
  background: #f3f4f6;
  color: #4f46e5;
}

/* Empty States */
.empty-state,
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  text-align: center;
  color: #9ca3af;
}

.empty-icon {
  width: 2rem;
  height: 2rem;
  margin-bottom: 0.5rem;
}

.empty-state p,
.loading-state p {
  font-size: 0.8125rem;
  margin: 0;
}

.empty-message {
  padding: 0.5rem;
  text-align: center;
  font-size: 0.6875rem;
  color: #9ca3af;
  font-style: italic;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 0.5rem;
}

/* Scrollbar */
.shift-list::-webkit-scrollbar {
  width: 0.375rem;
}

.shift-list::-webkit-scrollbar-track {
  background: #f9fafb;
}

.shift-list::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 0.25rem;
}

.shift-list::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>