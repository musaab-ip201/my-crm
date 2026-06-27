<template>
  <div class="flex h-full flex-col gap-4 p-4 bg-surface-modal">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-semibold">{{ __('Dynamic Lead Ingestion') }}</h2>
      <Button
        :label="__('Refresh')"
        icon-left="refresh-cw"
        variant="ghost"
        :loading="loading"
        @click="fetchData"
      />
    </div>

    <!-- Source Filter -->
    <div class="flex gap-3 items-end">
      <FormControl
        type="select"
        v-model="selectedSource"
        :options="sourceOptions"
        :label="__('Select API Source')"
        placeholder="Choose a source..."
        @change="onSourceChange"
        class="flex-1"
      />
      <Button
        v-if="selectedSource"
        :label="__('Load Data')"
        icon-left="download"
        variant="solid"
        :loading="loading"
        @click="fetchData"
      />
    </div>

    <!-- Schema Info -->
    <div v-if="schema && Object.keys(schema).length > 0" class="bg-surface-gray-1 p-3 rounded text-sm">
      <div class="font-semibold mb-2">{{ __('Detected Schema') }}:</div>
      <div class="flex flex-wrap gap-2">
        <Badge
          v-for="(type, field) in schema"
          :key="field"
          :label="`${field}: ${type}`"
          theme="blue"
          size="sm"
        />
      </div>
    </div>

    <!-- Field Mapping -->
    <div v-if="fieldMapping && Object.keys(fieldMapping).length > 0" class="bg-surface-gray-1 p-3 rounded text-sm">
      <div class="font-semibold mb-2">{{ __('Auto-Detected Field Mapping') }}:</div>
      <div class="grid grid-cols-2 gap-2">
        <div v-for="(apiField, crmField) in fieldMapping" :key="crmField" class="text-xs">
          <span class="font-medium">{{ crmField }}</span> ← <span class="text-ink-gray-6">{{ apiField }}</span>
        </div>
      </div>
    </div>

    <!-- Data Table -->
    <div v-if="records.length > 0" class="flex-1 overflow-auto border rounded">
      <table class="w-full text-sm">
        <thead class="bg-surface-gray-2 sticky top-0">
          <tr>
            <th v-for="field in displayableFields" :key="field" class="px-3 py-2 text-left font-semibold">
              {{ field }}
            </th>
            <th class="px-3 py-2 text-left font-semibold">{{ __('Actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(record, idx) in records" :key="idx" class="border-t hover:bg-surface-gray-1">
            <td v-for="field in displayableFields" :key="field" class="px-3 py-2 truncate max-w-xs">
              {{ formatValue(record[field]) }}
            </td>
            <td class="px-3 py-2">
              <Button
                :label="__('Create Lead')"
                icon-left="plus"
                variant="ghost"
                size="sm"
                :loading="creatingLeadIdx === idx"
                @click="createLeadFromRecord(record, idx)"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && selectedSource" class="flex-1 flex items-center justify-center text-ink-gray-5">
      {{ __('No data loaded. Click "Load Data" to fetch from API.') }}
    </div>

    <!-- Pagination -->
    <div v-if="records.length > 0 && isPaginated" class="flex justify-between items-center">
      <div class="text-sm text-ink-gray-6">
        {{ __('Page') }} {{ currentPage }} · {{ __('Total Records') }}: {{ totalRecords }}
      </div>
      <div class="flex gap-2">
        <Button
          :label="__('Previous')"
          icon-left="chevron-left"
          variant="ghost"
          :disabled="currentPage === 1"
          @click="previousPage"
        />
        <Button
          :label="__('Next')"
          icon-right="chevron-right"
          variant="ghost"
          @click="nextPage"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Button, FormControl, Badge, toast } from 'frappe-ui'

const selectedSource = ref('')
const sources = ref([])
const records = ref([])
const schema = ref({})
const fieldMapping = ref({})
const displayableFields = ref([])
const loading = ref(false)
const creatingLeadIdx = ref(null)
const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)
const isPaginated = ref(false)

const sourceOptions = computed(() => {
  return sources.value.map(s => ({
    label: s.source_name || s.name,
    value: s.name
  }))
})

onMounted(async () => {
  await loadSources()
})

async function loadSources() {
  try {
    const response = await frappe.call({
      method: 'order_integration.order_integration.api.dynamic_lead_api.get_api_sources_for_filter'
    })
    sources.value = response.message || []
  } catch (error) {
    toast({
      title: 'Error',
      description: error.message,
      icon: 'alert-circle',
      position: 'top-center'
    })
  }
}

async function fetchData() {
  if (!selectedSource.value) {
    toast({
      title: 'Error',
      description: 'Please select a source',
      icon: 'alert-circle',
      position: 'top-center'
    })
    return
  }

  loading.value = true
  try {
    const response = await frappe.call({
      method: 'order_integration.order_integration.api.dynamic_lead_api.fetch_api_data',
      args: {
        source_name: selectedSource.value,
        page: currentPage.value,
        page_size: pageSize.value
      }
    })

    if (response.message.status === 'success') {
      records.value = response.message.records || []
      schema.value = response.message.schema || {}
      fieldMapping.value = response.message.field_mapping || {}
      displayableFields.value = response.message.displayable_fields || []
      totalRecords.value = response.message.total_records || 0
      isPaginated.value = response.message.is_paginated || false

      toast({
        title: 'Success',
        description: `Loaded ${records.value.length} records`,
        icon: 'check-circle',
        position: 'top-center'
      })
    } else {
      throw new Error(response.message.message || 'Failed to fetch data')
    }
  } catch (error) {
    toast({
      title: 'Error',
      description: error.message,
      icon: 'alert-circle',
      position: 'top-center'
    })
  } finally {
    loading.value = false
  }
}

async function createLeadFromRecord(record, idx) {
  creatingLeadIdx.value = idx
  try {
    const response = await frappe.call({
      method: 'order_integration.order_integration.api.dynamic_lead_api.create_leads_from_api_data',
      args: {
        source_name: selectedSource.value,
        records: [record],
        field_mapping: fieldMapping.value
      }
    })

    if (response.message.status === 'success') {
      toast({
        title: 'Success',
        description: 'Lead created successfully',
        icon: 'check-circle',
        position: 'top-center'
      })
      records.value.splice(idx, 1)
    } else {
      throw new Error(response.message.message || 'Failed to create lead')
    }
  } catch (error) {
    toast({
      title: 'Error',
      description: error.message,
      icon: 'alert-circle',
      position: 'top-center'
    })
  } finally {
    creatingLeadIdx.value = null
  }
}

function onSourceChange() {
  currentPage.value = 1
  records.value = []
  schema.value = {}
  fieldMapping.value = {}
  displayableFields.value = []
}

function formatValue(value) {
  if (value === null || value === undefined) return '-'
  if (typeof value === 'object') return JSON.stringify(value).substring(0, 50)
  return String(value).substring(0, 100)
}

function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchData()
  }
}

function nextPage() {
  currentPage.value++
  fetchData()
}
</script>
