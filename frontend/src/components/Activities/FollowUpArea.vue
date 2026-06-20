<template>
  <div class="flex flex-col gap-4">
    <div class="text-lg font-semibold text-ink-gray-9">Follow-Up Details</div>
    
    <div v-if="loading" class="flex items-center justify-center py-10">
      <LoadingIndicator class="h-6 w-6" />
    </div>
    
    <div v-else class="flex flex-col gap-4">
      <!-- Follow-Up Date & Time -->
      <div class="grid grid-cols-2 gap-4">
        <FormControl
          type="date"
          label="Next Follow-Up Date"
          v-model="followupData.next_followup_date"
          @change="saveFollowUp"
        />
        <FormControl
          type="time"
          label="Follow-Up Time"
          v-model="followupData.next_followup_time"
          @change="saveFollowUp"
        />
      </div>
      
      <!-- Follow-Up Status -->
      <FormControl
        type="select"
        label="Follow-Up Status"
        v-model="followupData.followup_status"
        :options="statusOptions"
        @change="saveFollowUp"
      />
      
      <!-- Follow-Up Notes -->
      <FormControl
        type="textarea"
        label="Follow-Up Notes"
        v-model="followupData.followup_notes"
        @change="saveFollowUp"
        :rows="4"
      />
      
      <!-- Last Follow-Up Date (Read-only) -->
      <div v-if="followupData.last_followup_date" class="text-sm text-ink-gray-6">
        Last Follow-Up: {{ formatDate(followupData.last_followup_date) }}
      </div>
      
      <!-- Quick Actions -->
      <div class="flex gap-2 mt-4">
        <Button
          label="Mark as Done"
          variant="solid"
          @click="markAsDone"
          :disabled="!followupData.next_followup_date"
        />
        <Button
          label="Reschedule"
          @click="showRescheduleModal = true"
          :disabled="!followupData.next_followup_date"
        />
        <Button
          label="Cancel Follow-Up"
          @click="cancelFollowUp"
          :disabled="!followupData.next_followup_date"
        />
      </div>
      
      <!-- Status Badge -->
      <div v-if="followupData.followup_status" class="flex items-center gap-2 mt-2">
        <span class="text-sm font-medium">Current Status:</span>
        <Badge
          :label="followupData.followup_status"
          :variant="getStatusVariant(followupData.followup_status)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { createResource, FormControl, Badge, call, toast } from 'frappe-ui'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'

const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  docname: {
    type: String,
    required: true,
  },
})

const loading = ref(true)
const showRescheduleModal = ref(false)

const followupData = ref({
  next_followup_date: null,
  next_followup_time: null,
  followup_status: null,
  followup_notes: null,
  last_followup_date: null,
})

const statusOptions = [
  { label: 'Planned', value: 'Planned' },
  { label: 'Pending', value: 'Pending' },
  { label: 'Done', value: 'Done' },
  { label: 'Missed', value: 'Missed' },
  { label: 'Rescheduled', value: 'Rescheduled' },
  { label: 'Cancelled', value: 'Cancelled' },
]

onMounted(async () => {
  await loadFollowUpData()
})

async function loadFollowUpData() {
  loading.value = true
  try {
    const doc = await call('frappe.client.get', {
      doctype: props.doctype,
      name: props.docname,
      fields: ['next_followup_date', 'next_followup_time', 'followup_status', 'followup_notes', 'last_followup_date']
    })
    
    followupData.value = {
      next_followup_date: doc.next_followup_date || null,
      next_followup_time: doc.next_followup_time || null,
      followup_status: doc.followup_status || null,
      followup_notes: doc.followup_notes || null,
      last_followup_date: doc.last_followup_date || null,
    }
  } catch (error) {
    console.error('Error loading follow-up data:', error)
  } finally {
    loading.value = false
  }
}

async function saveFollowUp() {
  try {
    // Save each field individually to ensure they're all updated
    await call('frappe.client.set_value', {
      doctype: props.doctype,
      name: props.docname,
      fieldname: {
        next_followup_date: followupData.value.next_followup_date,
        next_followup_time: followupData.value.next_followup_time,
        followup_status: followupData.value.followup_status,
        followup_notes: followupData.value.followup_notes,
      }
    })
    toast.success('Follow-up updated successfully')
    console.log('Follow-up saved:', followupData.value)
  } catch (error) {
    console.error('Error saving follow-up:', error)
    toast.error('Failed to save follow-up')
  }
}

async function markAsDone() {
  try {
    await call('crm.api.followup.mark_followup_done', {
      lead_name: props.docname,
    })
    await loadFollowUpData()
  } catch (error) {
    console.error('Error marking as done:', error)
  }
}

async function cancelFollowUp() {
  try {
    await call('crm.api.followup.cancel_followup', {
      lead_name: props.docname,
      reason: followupData.value.followup_notes || 'Cancelled by user',
    })
    await loadFollowUpData()
  } catch (error) {
    console.error('Error cancelling follow-up:', error)
  }
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}

function getStatusVariant(status) {
  const variantMap = {
    'Planned': 'blue',
    'Pending': 'orange',
    'Done': 'green',
    'Missed': 'red',
    'Rescheduled': 'purple',
    'Cancelled': 'gray',
  }
  return variantMap[status] || 'gray'
}
</script>
