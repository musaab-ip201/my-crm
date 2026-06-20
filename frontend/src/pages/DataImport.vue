<template>
  <DataImport
    :doctype="route.params.doctype"
    :importName="route.params.importName"
    :doctypeMap="doctypeMap"
  />

  <!-- Progress bar — shown as a sticky top bar when import is running -->
  <Teleport to="body">
    <div
      v-if="importing"
      class="fixed top-0 left-0 right-0 z-[9999] flex flex-col"
    >
      <!-- Thin animated top bar -->
      <div class="h-1 bg-surface-gray-2 w-full">
        <div
          class="h-1 bg-blue-500 transition-all duration-500 ease-out"
          :style="{ width: progressPercent + '%' }"
        />
      </div>

      <!-- Toast-style banner below the bar -->
      <div class="flex items-center justify-center gap-3 bg-blue-600 text-white text-sm font-medium py-2 px-4 shadow-md">
        <!-- Spinner -->
        <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
        </svg>
        <span>{{ progressMessage || __('Importing… please wait') }}</span>
        <span class="opacity-75">{{ progressPercent }}%</span>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { usePageMeta, toast, call } from 'frappe-ui'
import { DataImport } from 'frappe-ui/frappe'
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted, onBeforeUnmount } from 'vue'

const route = useRoute()
const router = useRouter()

const importing = ref(false)
const progressPercent = ref(0)
const progressMessage = ref('')

let pollTimer = null
let pollCount = 0
const MAX_POLLS = 300 // 10 minutes max

function startPolling(importName) {
  stopPolling()
  importing.value = true
  progressPercent.value = 5
  progressMessage.value = __('Import started…')
  pollCount = 0
  console.log('[DataImport] Polling started for:', importName)
  pollTimer = setInterval(() => pollImportStatus(importName), 2000)
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

async function pollImportStatus(importName) {
  pollCount++

  // Animate progress bar 5% → 90% while waiting
  if (progressPercent.value < 90) {
    progressPercent.value = Math.min(90, 5 + pollCount * 3)
  }

  if (pollCount > MAX_POLLS) {
    stopPolling()
    importing.value = false
    toast.error(__('Import timed out. Please check the import status manually.'))
    return
  }

  try {
    const result = await call('frappe.client.get_value', {
      doctype: 'Data Import',
      filters: { name: importName },
      fieldname: 'status',
    })

    const status = result?.status || ''
    console.log('[DataImport] Poll', pollCount, '— status:', status)

    if (status === 'Pending' || status === '') {
      progressMessage.value = __('Waiting for import to start…')
      return
    }

    if (status === 'Success') {
      stopPolling()
      progressPercent.value = 100
      progressMessage.value = __('Done!')
      setTimeout(() => {
        importing.value = false
        toast.success(__('Imported successfully'))
        const importName = route.params.importName
        redirectAfterImport(importName)
      }, 600)
    } else if (status === 'Partial Success') {
      stopPolling()
      progressPercent.value = 100
      setTimeout(() => {
        importing.value = false
        toast.warning(__('Import completed with some errors. Click to view details.'))
        const importName = route.params.importName
        redirectAfterImport(importName)
      }, 600)
    } else if (status === 'Error') {
      stopPolling()
      importing.value = false

      try {
        const logs = await call('frappe.client.get_list', {
          doctype: 'Data Import Log',
          filters: { data_import: importName },
          fields: ['messages', 'exception'],
          order_by: 'creation desc',
          limit_page_length: 1,
        })

        let errorMessage = __('Import failed')

        if (logs && logs.length) {
          const log = logs[0]

          // Try parsing user-friendly messages
          if (log.messages) {
            const msgs = JSON.parse(log.messages)
            if (msgs.length && msgs[0].message) {
              errorMessage = msgs[0].message
            }
          }
          // fallback to exception
          else if (log.exception) {
            errorMessage = log.exception.split('\n')[0]
          }
        }

        toast.error(errorMessage)
      } catch (e) {
        toast.error(__('Import failed. Please check logs.'))
      }
    } else {
      // In Progress
      progressMessage.value = __('Importing rows…')
    }
  } catch (e) {
    console.warn('[DataImport] Poll error (will retry):', e)
  }
}

// Redirect to the correct list after import based on the doctype
async function redirectAfterImport(importName) {
  try {
    const result = await call('frappe.client.get_value', {
      doctype: 'Data Import',
      filters: { name: importName },
      fieldname: 'reference_doctype',
    })
    const doctype = result?.reference_doctype || ''
    const listRoute = doctypeMap[doctype]?.listRoute
    if (listRoute) {
      // listRoute is like '/crm/leads' — strip the '/crm' prefix for router.push
      router.push(listRoute.replace('/crm', '') || '/leads')
    } else {
      router.push('/leads')
    }
  } catch (_) {
    router.push('/leads')
  }
}

// Intercept clicks on the Import / Retry button inside the frappe-ui component
function handleDocumentClick(e) {
  // Walk up from the clicked element to find a button
  let el = e.target
  while (el && el !== document.body) {
    if (el.tagName === 'BUTTON') {
      const label = el.textContent?.trim()
      console.log('[DataImport] Button clicked:', label)
      if (label === 'Import' || label === 'Retry') {
        const importName = route.params.importName
        console.log('[DataImport] Import button detected, importName:', importName)
        if (importName) {
          setTimeout(() => startPolling(importName), 800)
        }
      }
      break
    }
    el = el.parentElement
  }
}

onMounted(() => {
  document.addEventListener('click', handleDocumentClick, true)
})

onBeforeUnmount(() => {
  stopPolling()
  document.removeEventListener('click', handleDocumentClick, true)
})

const doctypeMap = {
  'CRM Lead': {
    title: 'Leads',
    listRoute: '/crm/leads',
    pageRoute: `/crm/leads/docname`,
  },
  'CRM Deal': {
    title: 'Deals',
    listRoute: '/crm/deals',
    pageRoute: `/crm/deals/docname`,
  },
  Contact: {
    title: 'Contacts',
    listRoute: '/crm/contacts',
    pageRoute: `/crm/contacts/docname`,
  },
  'CRM Task': {
    title: 'Tasks',
    listRoute: '/crm/tasks',
  },
  'CRM Organization': {
    title: 'Organizations',
    listRoute: '/crm/organizations',
    pageRoute: `/crm/organizations/docname`,
  },
  'CRM Call Log': {
    title: 'Call Log',
    listRoute: '/crm/call-logs',
  },
}

usePageMeta(() => {
  return {
    title: __('Data Import'),
  }
})
</script>