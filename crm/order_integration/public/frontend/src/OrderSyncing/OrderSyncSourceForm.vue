<template>
  <div class="flex h-full flex-col text-ink-gray-8">
    <div class="flex justify-between px-2 pt-2">
      <div class="flex gap-1 -ml-4 w-7/12">
        <Button
          variant="ghost"
          icon-left="chevron-left"
          :label="isNew ? __('New Order Sync Source') : (syncSource.source_name || syncSource.name)"
          size="md"
          @click="emit('updateStep', 'source-list')"
          class="cursor-pointer font-semibold text-xl hover:opacity-70 !pr-0 !max-w-96 !justify-start"
        />
      </div>
      <div class="flex items-center space-x-3 w-5/12 justify-end">
        <Button
          :label="__('Setup Statuses')"
          variant="ghost"
          icon-left="settings"
          :loading="isSettingUp"
          @click="setupStatuses"
          title="Create CRM Lead Status values for order syncing"
        />
        <Button
          :label="__('Test Connection')"
          variant="outline"
          icon-left="check-circle"
          :loading="isTesting"
          @click="testConnection"
        />
        <Button
          v-if="!isNew"
          :label="__('Sync Now')"
          variant="outline"
          icon-left="refresh-cw"
          :loading="isSyncing"
          @click="syncNow"
        />
        <Button
          :label="isNew ? __('Create') : __('Update')"
          variant="solid"
          :loading="loading"
          @click="save"
        />
      </div>
    </div>

    <div class="mt-6 grid grid-cols-2 gap-4 px-2">
      <FormControl
        type="data"
        required
        v-model="syncSource.source_name"
        :label="__('Source Name')"
        :placeholder="__('e.g. My Store')"
      />

      <FormControl
        type="data"
        required
        v-model="syncSource.api_key"
        :label="__('API Key')"
        :placeholder="__('e.g. ipshopy')"
      />

      <FormControl
        type="select"
        required
        v-model="syncSource.sync_frequency"
        :options="frequencyOptions"
        :label="__('Sync Frequency')"
      />

      <FormControl
        type="password"
        v-model="syncSource.access_token"
        :label="__('Access Token')"
        :placeholder="isNew ? __('Enter access token') : __('Leave blank to keep existing')"
      />

      <FormControl
        type="data"
        required
        v-model="syncSource.api_url"
        :label="__('API URL')"
        :placeholder="__('https://api.yourstore.com')"
        class="col-span-2"
      />

      <div v-if="!isNew && syncSource.last_synced_at" class="col-span-2 text-sm text-ink-gray-5">
        {{ __('Last synced') }}: {{ formatDate(syncSource.last_synced_at) }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button, FormControl, toast } from 'frappe-ui'

const props = defineProps({
  sourceData: { type: Object, default: () => ({}) },
})
const emit = defineEmits(['updateStep'])

const isNew = ref(true)
const loading = ref(false)
const isSyncing = ref(false)
const isTesting = ref(false)
const isSettingUp = ref(false)

const sourceTypeOptions = ['ipshopy.com', 'Shop.com', 'Manual']
const frequencyOptions = ['Every 5 Minutes', 'Every 10 Minutes', 'Hourly', 'Daily']

const syncSource = ref({
  name: '',
  source_name: '',
  api_key: '',
  sync_frequency: 'Every 5 Minutes',
  access_token: '',
  api_url: '',
  last_synced_at: null,
})

function formatDate(dt) {
  return dt ? new Date(dt).toLocaleString() : ''
}

onMounted(() => {
  if (props.sourceData?.name) {
    Object.assign(syncSource.value, props.sourceData)
    isNew.value = false
  }
})

function save() {
  if (!syncSource.value.source_name || !syncSource.value.api_url) {
    toast.error(__('Please fill in all required fields'))
    return
  }
  if (isNew.value && !syncSource.value.access_token) {
    toast.error(__('Access token is required for new sources'))
    return
  }

  loading.value = true
  
  console.log('\n\n' + '='.repeat(80))
  console.log('SAVE CLICKED')
  console.log('='.repeat(80))
  console.log('Is New:', isNew.value)
  console.log('Source Data:', JSON.stringify(syncSource.value, null, 2))
  console.log('='.repeat(80) + '\n')
  
  frappe.call({
    method: 'order_integration.order_integration.doctype.order_sync_source.order_sync_source.save_order_source',
    args: {
      doc: syncSource.value,
      is_edit: !isNew.value
    },
    freeze: true,
    freeze_message: __('Saving...'),
    callback: function(r) {
      console.log('\n' + '='.repeat(80))
      console.log('SAVE CALLBACK')
      console.log('='.repeat(80))
      console.log('Response:', r)
      console.log('Message:', r.message)
      console.log('='.repeat(80) + '\n')
      
      if (r.message) {
        const result = r.message
        if (result.status === 'success') {
          toast.success(isNew.value ? __('Source created') : __('Source updated'))
          emit('updateStep', 'source-list')
        } else {
          toast.error(result.message || __('Error saving source'))
        }
      }
    },
    error: function(r) {
      console.error('\n' + '='.repeat(80))
      console.error('SAVE ERROR')
      console.error('='.repeat(80))
      console.error('Error:', r)
      console.error('='.repeat(80) + '\n')
      toast.error(r.message || __('Error saving source'))
    },
    always: function() {
      loading.value = false
    }
  })
}

function syncNow() {
  console.log('\n\n' + '='.repeat(80))
  console.log('SYNC NOW CLICKED')
  console.log('='.repeat(80))
  console.log('Source Name:', syncSource.value.name)
  console.log('API URL:', syncSource.value.api_url)
  console.log('='.repeat(80) + '\n')
  
  isSyncing.value = true
  
  frappe.call({
    method: 'order_integration.order_integration.doctype.order_sync_source.order_sync_source.sync_orders_now',
    args: {
      source_name: syncSource.value.name
    },
    freeze: true,
    freeze_message: __('Syncing orders...'),
    callback: function(r) {
      console.log('\n\n' + '='.repeat(80))
      console.log('SYNC RESPONSE RECEIVED')
      console.log('='.repeat(80))
      console.log('Full Response:', r)
      console.log('Message:', r.message)
      console.log('='.repeat(80) + '\n')
      
      if (r.message) {
        const result = r.message
        
        console.log('\n' + '='.repeat(80))
        console.log('SYNC RESULT')
        console.log('='.repeat(80))
        console.log('Status:', result.status)
        console.log('Message:', result.message)
        console.log('Orders Fetched:', result.orders ? result.orders.length : 0)
        console.log('Leads Created:', result.leads_created ? result.leads_created.length : 0)
        console.log('='.repeat(80) + '\n')
        
        if (result.orders && result.orders.length > 0) {
          console.log('\n' + '='.repeat(80))
          console.log('ORDERS FROM API')
          console.log('='.repeat(80))
          result.orders.forEach((order, idx) => {
            console.log(`\nOrder ${idx + 1}:`)
            console.log(JSON.stringify(order, null, 2))
          })
          console.log('='.repeat(80) + '\n')
        }
        
        if (result.leads_created && result.leads_created.length > 0) {
          console.log('\n' + '='.repeat(80))
          console.log('LEADS CREATED')
          console.log('='.repeat(80))
          result.leads_created.forEach((lead, idx) => {
            console.log(`\nLead ${idx + 1}:`)
            console.log(JSON.stringify(lead, null, 2))
          })
          console.log('='.repeat(80) + '\n')
        }
        
        if (result.status === 'success') {
          console.log('\n' + '='.repeat(80))
          console.log('✅ SYNC SUCCESS')
          console.log('='.repeat(80))
          console.log('Message:', result.message)
          console.log('='.repeat(80) + '\n')
          toast.success(result.message)
          frappe.call({
            method: 'order_integration.api.lead_list_dynamic_columns_api.get_dynamic_columns_data',
            args: {
              source_name: syncSource.value.name,
              data_type: 'cart_data', // or dynamic value
              lead_names: result.leads_created.map(l => l.name)
            },
            callback: function(res) {
          
              console.log('DYNAMIC COLUMNS RESPONSE', res)
          
              if (res.message?.status === 'success') {
          
                console.log('Columns:', res.message.columns)
                console.log('Rows:', res.message.rows)
          
                // store columns
                dynamicColumns.value = res.message.columns || []
          
                // store rows
                dynamicRows.value = res.message.rows || {}
          
                // OPTIONAL:
                // refresh list/table
                refreshLeadList()
              }
            }
          })
        } else {
          console.error('\n' + '='.repeat(80))
          console.error('❌ SYNC ERROR')
          console.error('='.repeat(80))
          console.error('Message:', result.message)
          console.error('='.repeat(80) + '\n')
          toast.error(result.message)
        }
      }
    },
    error: function(r) {
      console.error('\n\n' + '='.repeat(80))
      console.error('SYNC CALL ERROR')
      console.error('='.repeat(80))
      console.error('Error:', r)
      console.error('='.repeat(80) + '\n')
      toast.error('Sync failed: ' + (r.message || 'Unknown error'))
    },
    always: function() {
      isSyncing.value = false
    }
  })
}

function setupStatuses() {
  console.log('\n\n' + '='.repeat(80))
  console.log('SETUP STATUSES CLICKED')
  console.log('='.repeat(80))
  console.log('Creating CRM Lead Status values...')
  console.log('='.repeat(80) + '\n')
  
  isSettingUp.value = true
  
  frappe.call({
    method: 'order_integration.order_integration.doctype.order_sync_source.setup_statuses.setup_crm_lead_statuses',
    freeze: true,
    freeze_message: __('Setting up statuses...'),
    callback: function(r) {
      console.log('\n' + '='.repeat(80))
      console.log('SETUP STATUSES RESPONSE')
      console.log('='.repeat(80))
      console.log('Response:', r)
      console.log('Message:', r.message)
      console.log('='.repeat(80) + '\n')
      
      if (r.message) {
        const result = r.message
        
        console.log('Status:', result.status)
        console.log('Message:', result.message)
        console.log('Created:', result.created)
        console.log('Already Exist:', result.already_exist)
        if (result.errors && result.errors.length > 0) {
          console.error('Errors:', result.errors)
        }
        
        if (result.status === 'success' || result.status === 'partial') {
          toast.success(result.message)
        } else {
          toast.error(result.message)
        }
      }
    },
    error: function(r) {
      console.error('\n' + '='.repeat(80))
      console.error('SETUP STATUSES ERROR')
      console.error('='.repeat(80))
      console.error('Error:', r)
      console.error('='.repeat(80) + '\n')
      toast.error(__('Failed to setup statuses'))
    },
    always: function() {
      isSettingUp.value = false
    }
  })
}

function testConnection() {
  if (!syncSource.value.api_url || !syncSource.value.access_token) {
    toast.error(__('Please fill in API URL and Access Token'))
    return
  }

  isTesting.value = true
  
  console.log('\n\n' + '='.repeat(80))
  console.log('TEST CONNECTION CLICKED')
  console.log('='.repeat(80))
  console.log('API URL:', syncSource.value.api_url)
  console.log('API Key:', syncSource.value.api_key)
  console.log('Token:', syncSource.value.access_token)
  console.log('='.repeat(80) + '\n')
  
  frappe.call({
    method: 'order_integration.order_integration.doctype.order_sync_source.order_sync_source.test_api_connection',
    args: {
      api_url: syncSource.value.api_url,
      access_token: syncSource.value.access_token,
      api_key: syncSource.value.api_key
    },
    freeze: true,
    freeze_message: __('Testing connection...'),
    callback: function(r) {
      console.log('\n' + '='.repeat(80))
      console.log('TEST CONNECTION CALLBACK')
      console.log('='.repeat(80))
      console.log('Response:', r)
      console.log('Message:', r.message)
      console.log('='.repeat(80) + '\n')
      
      if (r.message) {
        const result = r.message
        
        console.log('Status:', result.status)
        console.log('Message:', result.message)
        if (result.sample_record) {
          console.log('Sample Record:', JSON.stringify(result.sample_record, null, 2))
        }
        
        if (result.status === 'success') {
          toast.success(result.message)
        } else if (result.status === 'warning') {
          toast.warning(result.message)
        } else {
          toast.error(result.message)
        }
      }
    },
    error: function(r) {
      console.error('\n' + '='.repeat(80))
      console.error('TEST CONNECTION ERROR')
      console.error('='.repeat(80))
      console.error('Error:', r)
      console.error('='.repeat(80) + '\n')
      toast.error(__('Connection test failed'))
    },
    always: function() {
      isTesting.value = false
    }
  })
}
</script>
