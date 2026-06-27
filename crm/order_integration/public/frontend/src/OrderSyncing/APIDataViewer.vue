<template>
  <div class="flex h-full gap-4 bg-surface-modal">
    <!-- Main Table Area -->
    <div class="flex-1 flex flex-col gap-4 p-4 overflow-auto">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <h2 class="text-xl font-semibold">API Data Viewer</h2>
        <Button
          :label="loading ? 'Loading...' : 'Refresh'"
          icon-left="refresh-cw"
          variant="ghost"
          :loading="loading"
          @click="fetchData"
        />
      </div>

      <!-- Source Selector -->
      <div class="flex gap-3 items-end">
        <FormControl
          type="select"
          v-model="selectedSource"
          :options="sourceOptions"
          :label="'Select API Source'"
          placeholder="Choose a source..."
          @change="onSourceChange"
          class="flex-1"
        />
        <Button
          v-if="selectedSource"
          :label="'Load Data'"
          icon-left="download"
          variant="solid"
          :loading="loading"
          @click="fetchData"
        />
      </div>

      <!-- Schema Info -->
      <div v-if="allFields.length > 0" class="bg-surface-gray-1 p-3 rounded text-sm">
        <div class="font-semibold mb-2">Available Fields ({{ allFields.length }}):</div>
        <div class="flex flex-wrap gap-2">
          <Badge
            v-for="field in allFields"
            :key="field"
            :label="field"
            :theme="visibleColumns.includes(field) ? 'blue' : 'gray'"
            size="sm"
          />
        </div>
      </div>

      <!-- Data Table -->
      <div v-if="records.length > 0" class="flex-1 overflow-auto border rounded bg-white">
        <table class="w-full text-sm">
          <thead class="bg-surface-gray-2 sticky top-0">
            <tr>
              <th v-for="field in visibleColumns" :key="field" class="px-3 py-2 text-left font-semibold whitespace-nowrap">
                {{ field }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(record, idx) in records" :key="idx" class="border-t hover:bg-surface-gray-1">
              <td v-for="field in visibleColumns" :key="field" class="px-3 py-2 truncate max-w-xs text-xs">
                {{ formatValue(record[field]) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty State -->
      <div v-else-if="!loading && selectedSource" class="flex-1 flex items-center justify-center text-ink-gray-5">
        No data loaded. Click "Load Data" to fetch from API.
      </div>

      <!-- Pagination -->
      <div v-if="records.length > 0 && isPaginated" class="flex justify-between items-center">
        <div class="text-sm text-ink-gray-6">
          Page {{ currentPage }} · Total Records: {{ totalRecords }}
        </div>
        <div class="flex gap-2">
          <Button
            :label="'Previous'"
            icon-left="chevron-left"
            variant="ghost"
            :disabled="currentPage === 1"
            @click="previousPage"
          />
          <Button
            :label="'Next'"
            icon-right="chevron-right"
            variant="ghost"
            @click="nextPage"
          />
        </div>
      </div>
    </div>

    <!-- Column Selector Panel -->
    <div class="w-64 bg-surface-gray-1 border-l p-4 overflow-y-auto">
      <div class="font-semibold mb-4">Columns</div>
      
      <!-- Search -->
      <input
        v-model="columnSearch"
        type="text"
        placeholder="Search columns..."
        class="w-full px-2 py-1 mb-3 border rounded text-sm"
      />

      <!-- Column List -->
      <div class="space-y-2">
        <div
          v-for="field in filteredFields"
          :key="field"
          class="flex items-center gap-2 p-2 hover:bg-surface-gray-2 rounded cursor-pointer"
          @click="toggleColumn(field)"
        >
          <input
            type="checkbox"
            :checked="visibleColumns.includes(field)"
            @change="toggleColumn(field)"
            class="w-4 h-4"
          />
          <span class="text-sm flex-1 truncate">{{ field }}</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="mt-4 space-y-2 border-t pt-4">
        <Button
          :label="'Show All'"
          variant="ghost"
          size="sm"
          class="w-full"
          @click="showAllColumns"
        />
        <Button
          :label="'Hide All'"
          variant="ghost"
          size="sm"
          class="w-full"
          @click="hideAllColumns"
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
const allFields = ref([])
const visibleColumns = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)
const isPaginated = ref(false)
const columnSearch = ref('')

const sourceOptions = computed(() => {
  return sources.value.map(s => ({
    label: s.source_name || s.name,
    value: s.name
  }))
})

const filteredFields = computed(() => {
  if (!columnSearch.value) return allFields.value
  return allFields.value.filter(f => 
    f.toLowerCase().includes(columnSearch.value.toLowerCase())
  )
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
      
      // Extract ALL fields from records
      const fieldsSet = new Set()
      records.value.forEach(record => {
        Object.keys(record).forEach(key => {
          // Skip nested objects like 'customer'
          if (typeof record[key] !== 'object' || record[key] === null) {
            fieldsSet.add(key)
          }
        })
      })
      
      allFields.value = Array.from(fieldsSet).sort()
      
      // Show first 10 fields by default
      visibleColumns.value = allFields.value.slice(0, 10)
      
      totalRecords.value = response.message.total_records || 0
      isPaginated.value = response.message.is_paginated || false

      toast({
        title: 'Success',
        description: `Loaded ${records.value.length} records with ${allFields.value.length} fields`,
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

function onSourceChange() {
  currentPage.value = 1
  records.value = []
  allFields.value = []
  visibleColumns.value = []
  columnSearch.value = ''
}

function toggleColumn(field) {
  const idx = visibleColumns.value.indexOf(field)
  if (idx > -1) {
    visibleColumns.value.splice(idx, 1)
  } else {
    visibleColumns.value.push(field)
  }
}

function showAllColumns() {
  visibleColumns.value = [...allFields.value]
}

function hideAllColumns() {
  visibleColumns.value = []
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
