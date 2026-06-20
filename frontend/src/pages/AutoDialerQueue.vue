<template>
  <LayoutHeader>
    <template #left-header>
      <Breadcrumbs :items="[{ label: __('Auto Dialer Queue'), route: '/auto-dialer' }]" />
    </template>
  </LayoutHeader>
  
  <div v-if="!queueId" class="flex h-full items-center justify-center">
    <div class="text-center">
      <div class="text-xl text-ink-gray-6 mb-2">{{ __('No Active Queue') }}</div>
      <div class="text-sm text-ink-gray-5">{{ __('Select leads and start auto dialer from Leads list') }}</div>
    </div>
  </div>

  <div v-else class="flex h-full flex-col p-5">
    <!-- Controls -->
    <div class="mb-5 flex items-center justify-between rounded-lg border border-stroke-gray-3 bg-surface-gray-1 p-4">
      <div class="flex items-center gap-4">
        <div class="text-lg font-semibold">
          {{ __('Auto Dialer') }}
        </div>
        <div class="flex items-center gap-2">
          <Badge :label="queueStatus" :theme="getStatusTheme(queueStatus)" />
          <div class="text-sm text-ink-gray-6">
            {{ completedCount + failedCount }} / {{ totalCount }} {{ __('attempted') }}
          </div>
        </div>
      </div>
      
      <div class="flex gap-2">
        <Button
          v-if="queueStatus === 'Active'"
          :label="__('Pause')"
          @click="pauseQueue"
        />
        <Button
          v-if="queueStatus === 'Paused'"
          variant="solid"
          :label="__('Resume')"
          @click="resumeQueue"
        />
        <Button
          v-if="queueStatus === 'Stopped' || queueStatus === 'Completed'"
          variant="solid"
          theme="blue"
          :label="__('Start Again')"
          @click="startAgain"
        />
        <Button
          v-if="queueStatus !== 'Completed' && queueStatus !== 'Stopped'"
          theme="red"
          :label="__('Stop')"
          @click="stopQueue"
        />
      </div>
    </div>

    <!-- Current Call -->
    <div v-if="currentLead" class="mb-5 rounded-lg border border-stroke-blue-3 bg-surface-blue-1 p-4">
      <div class="mb-2 text-sm font-medium text-ink-blue-6">{{ __('Current Call') }}</div>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <Avatar :label="currentLead.lead_name" size="lg" />
          <div>
            <div class="font-medium">{{ currentLead.lead_name }}</div>
            <div class="text-sm text-ink-gray-6">{{ currentLead.phone }}</div>
            <div v-if="currentLead.ref_id" class="text-xs text-ink-gray-5 mt-1">
              Ref ID: {{ currentLead.ref_id }}
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <Badge :label="currentLead.status" :theme="getCallStatusTheme(currentLead.status)" />
          <Button
            :label="__('View Lead')"
            @click="openLead(currentLead.lead_id)"
          />
          <Button
            v-if="queueStatus === 'Active' && currentLead.status === 'Calling'"
            variant="solid"
            theme="green"
            :label="__('Next Call')"
            @click="manualNextCall"
          />
        </div>
      </div>
    </div>

    <!-- Queue List -->
    <div class="flex-1 overflow-auto">
      <div class="mb-3 text-sm font-medium text-ink-gray-7">{{ __('Queue') }}</div>
      <div class="space-y-2">
        <div
          v-for="(lead, index) in leads"
          :key="lead.lead_id"
          class="flex items-center justify-between rounded-lg border p-3"
          :class="{
            'border-stroke-gray-3 bg-surface-gray-1': lead.status === 'Pending',
            'border-stroke-green-3 bg-surface-green-1': lead.status === 'Completed',
            'border-stroke-red-3 bg-surface-red-1': lead.status === 'Failed',
            'border-stroke-blue-3 bg-surface-blue-1': lead.status === 'Calling'
          }"
        >
          <div class="flex items-center gap-3">
            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-surface-gray-3 text-sm font-medium">
              {{ index + 1 }}
            </div>
            <Avatar :label="lead.lead_name" size="md" />
            <div>
              <div class="font-medium">{{ lead.lead_name }}</div>
              <div class="text-sm text-ink-gray-6">{{ lead.phone }}</div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <Badge :label="lead.status" :theme="getCallStatusTheme(lead.status)" />
            <Badge
              v-if="lead.crm_status && lead.crm_status !== lead.status"
              :label="lead.crm_status"
              theme="gray"
              size="sm"
            />
            <Button
              size="sm"
              :label="__('View')"
              @click="openLead(lead.lead_id)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { call, toast } from 'frappe-ui'
import { globalStore } from '@/stores/global'
import { Avatar, Badge, Button, Breadcrumbs } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'

const router = useRouter()
const route = useRoute()
const store = globalStore()

const queueId = ref(route.query.queue_id || null)
const queueStatus = ref('Active')
const leads = ref([])
const currentIndex = ref(0)
const totalCount = ref(0)
const completedCount = ref(0)
const failedCount = ref(0)

const currentLead = computed(() => {
  if (currentIndex.value >= 0 && currentIndex.value < leads.value.length) {
    return leads.value[currentIndex.value]
  }
  return null
})

let pollingInterval = null
let callEndCheckInterval = null

async function loadQueueStatus() {
  if (!queueId.value) return
  
  try {
    const result = await call('crm.integrations.tata_tele.auto_dialer.get_queue_status', {
      queue_id: queueId.value
    })
    
    queueStatus.value = result.status
    leads.value = result.leads || []
    currentIndex.value = result.current_index || 0
    totalCount.value = result.total_leads || 0
    completedCount.value = result.completed_leads || 0
    failedCount.value = result.failed_leads || 0
  } catch (error) {
    console.error('Failed to load queue status:', error)
  }
}

async function pauseQueue() {
  try {
    await call('crm.integrations.tata_tele.auto_dialer.pause_auto_dialer', {
      queue_id: queueId.value
    })
    queueStatus.value = 'Paused'
    toast.success(__('Auto dialer paused'))
  } catch (error) {
    toast.error(__('Failed to pause auto dialer'))
  }
}

async function resumeQueue() {
  try {
    await call('crm.integrations.tata_tele.auto_dialer.resume_auto_dialer', {
      queue_id: queueId.value
    })
    queueStatus.value = 'Active'
    toast.success(__('Auto dialer resumed'))
    processNextCall()
  } catch (error) {
    toast.error(__('Failed to resume auto dialer'))
  }
}

async function stopQueue() {
  store.$dialog({
    title: __('Stop Auto Dialer'),
    message: __('Are you sure you want to stop the auto dialer? This cannot be undone.'),
    variant: 'solid',
    theme: 'red',
    actions: [
      {
        label: __('Stop'),
        variant: 'solid',
        theme: 'red',
        onClick: async (close) => {
          try {
            await call('crm.integrations.tata_tele.auto_dialer.stop_auto_dialer', {
              queue_id: queueId.value
            })
            queueStatus.value = 'Stopped'
            toast.success(__('Auto dialer stopped'))
            close()
          } catch (error) {
            toast.error(__('Failed to stop auto dialer'))
          }
        }
      }
    ]
  })
}

async function startAgain() {
  try {
    await call('crm.integrations.tata_tele.auto_dialer.restart_auto_dialer', {
      queue_id: queueId.value
    })
    queueStatus.value = 'Active'
    toast.success(__('Auto dialer restarted'))
    processNextCall()
  } catch (error) {
    toast.error(__('Failed to restart auto dialer'))
  }
}

async function processNextCall() {
  if (!queueId.value || queueStatus.value !== 'Active') return
  
  try {
    const result = await call('crm.integrations.tata_tele.auto_dialer.process_next_call', {
      queue_id: queueId.value
    })
    
    if (result.completed) {
      toast.success(__('All calls completed'))
      queueStatus.value = 'Completed'
      return
    }
    
    if (result.paused) {
      return
    }
    
    if (result.success) {
      toast.success(__('Calling {0}', [result.lead.lead_name]))
      await loadQueueStatus()
    } else if (result.error) {
      toast.error(__('Call failed: {0}', [result.error]))
      await loadQueueStatus()
    }
  } catch (error) {
    console.error('Failed to process next call:', error)
    toast.error(__('Failed to initiate call'))
  }
}

async function manualNextCall() {
  // Mark current call as completed manually
  if (currentLead.value) {
    currentLead.value.status = 'Completed'
  }
  
  await loadQueueStatus()
  processNextCall()
}

function openLead(leadId) {
  router.push({ name: 'Lead', params: { leadId } })
}

function getStatusTheme(status) {
  const themes = {
    'Active': 'blue',
    'Paused': 'orange',
    'Stopped': 'red',
    'Completed': 'green'
  }
  return themes[status] || 'gray'
}

function getCallStatusTheme(status) {
  const themes = {
    'Pending': 'gray',
    'Calling': 'blue',
    'Completed': 'green',
    'Failed': 'red',
    'No Answer': 'orange',
    'Busy': 'orange'
  }
  return themes[status] || 'gray'
}

onMounted(async () => {
  if (queueId.value) {
    await loadQueueStatus()
    
    // Start polling for updates
    pollingInterval = setInterval(loadQueueStatus, 3000)
    
    // If queue is active and no current call, start processing
    if (queueStatus.value === 'Active' && currentIndex.value === 0) {
      processNextCall()
    }
  }
})

onUnmounted(() => {
  if (pollingInterval) {
    clearInterval(pollingInterval)
  }
})
</script>
