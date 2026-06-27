
<template>
  <div class="flex h-full flex-col gap-6 text-ink-gray-8">
    <div class="flex justify-between px-2 pt-2">
      <div class="flex flex-col gap-1 w-9/12">
        <h2 class="flex gap-2 text-xl font-semibold leading-none h-5 items-center">
          {{ __('Order Syncing') }}
          <Badge theme="orange" size="sm">Beta</Badge>
        </h2>
        <p class="text-p-base text-ink-gray-6">
          {{ __('Manage sources for automatic order syncing to your CRM') }}
        </p>
      </div>
      <div class="flex items-center space-x-2 w-3/12 justify-end">
        <Button
          :label="__('Sync All')"
          icon-left="refresh-cw"
          variant="subtle"
          :loading="isSyncingAll"
          @click="syncAllSources"
        />
        <Button
          :label="__('New')"
          icon-left="plus"
          variant="solid"
          @click="emit('updateStep', 'new-order-source')"
        />
      </div>
    </div>

    <div v-if="loading" class="flex mt-28 justify-center w-full">
      <Button :loading="true" variant="ghost" size="2xl" />
    </div>

    <div v-else-if="!sources.length" class="flex justify-center w-full">
      <div class="text-ink-gray-4 border border-dashed rounded w-full flex items-center justify-center min-h-[250px] mx-2">
        {{ __('No order sources found. Click New to add one.') }}
      </div>
    </div>
 <div v-else class="flex flex-1 flex-col overflow-hidden">
      <div class="flex items-center py-2 px-4 text-sm text-ink-gray-5">
        <div class="w-4/6">{{ __('Name') }}</div>
        <div class="w-1/6">{{ __('Type') }}</div>
        <div class="w-1/6">{{ __('Last Synced') }}</div>
      </div>
      <div class="h-px border-t mx-4 border-outline-gray-modals" />
         <div class="flex-1 overflow-y-auto overflow-x-visible min-h-0">
    <ul class="px-2 mt-2 pb-40">
        <template v-for="(source, i) in sources" :key="source.name">
          <li
            class="flex items-center justify-between p-3 cursor-pointer hover:bg-surface-menu-bar rounded"
            @click="emit('updateStep', 'edit-order-source', source)"
          >
            <div class="flex flex-col w-4/6 pr-5">
              <div class="text-p-base font-medium text-ink-gray-7 truncate">
                {{ source.source_name || source.name }}
              </div>
            </div>
            <div class="flex flex-col w-1/6 pr-5">
              <div class="text-p-base text-ink-gray-6 truncate">
                {{ source.source_type }}
              </div>
            </div>
           <div class="flex items-center justify-between w-1/6 relative">
              <div class="text-sm text-ink-gray-5 truncate">
                {{ source.last_synced_at ? formatDate(source.last_synced_at) : __('Never') }}
              </div>
<Dropdown
  :options="getDropdownOptions(source)"
  :placement="i >= sources.length - 2 ? 'top-end' : 'bottom-end'"
  :button="{ icon: 'more-horizontal', variant: 'ghost' }"
  @click.stop
/>
            </div>
          </li>
          <div v-if="i < sources.length - 1" class="h-px border-t mx-2 border-outline-gray-modals" />
        </template>
      </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Dropdown, toast, Badge, Button, call } from 'frappe-ui'

const emit = defineEmits(['updateStep'])

const sources = ref([])
const loading = ref(false)
const isSyncingAll = ref(false)

function formatDate(dt) {
  if (!dt) return ''
  return new Date(dt).toLocaleString()
}

async function loadSources() {
  loading.value = true
  try {
    const data = await call(
      'order_integration.order_integration.doctype.order_sync_source.order_sync_source.get_order_sources'
    )
    sources.value = data || []
  } catch (e) {
    toast.error(__('Failed to load sources'))
  } finally {
    loading.value = false
  }
}

onMounted(loadSources)

async function syncAllSources() {
  isSyncingAll.value = true
  try {
    await call(
      'order_integration.order_integration.doctype.order_sync_source.order_sync_source.trigger_sync_all'
    )
    toast.success(__('Sync queued for all sources'))
  } catch (e) {
    toast.error(__('Failed to queue sync'))
  } finally {
    isSyncingAll.value = false
  }
}

async function deleteSource(sourceName) {
  try {
    await call(
      'order_integration.order_integration.doctype.order_sync_source.order_sync_source.delete_order_source',
      { source_name: sourceName }
    )
    toast.success(__('Source deleted'))
    loadSources()
  } catch (e) {
    toast.error(__('Failed to delete source'))
  }
}

function getDropdownOptions(source) {
  return [
    {
      label: __('Edit'),
      icon: 'edit',
      onClick: () => emit('updateStep', 'edit-order-source', source),
    },
    {
      label: __('Sync Now'),
      icon: 'refresh-cw',
      onClick: () => syncOne(source.name),
    },
    {
      label: __('Delete'),
      icon: 'trash-2',
      onClick: () => deleteSource(source.name),
    },
  ]
}

async function syncOne(sourceName) {
  try {
    await call(
      'order_integration.order_integration.doctype.order_sync_source.order_sync_source.trigger_manual_sync',
      { source_name: sourceName }
    )
    toast.success(__('Sync started'))
  } catch (e) {
    toast.error(__('Sync failed to start'))
  }
}
</script>