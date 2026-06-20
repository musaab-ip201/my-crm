<template>
  <LayoutHeader>
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs">
        <template #prefix="{ item }">
          <Icon v-if="item.icon" :icon="item.icon" class="mr-2 h-4" />
        </template>
      </Breadcrumbs>
    </template>
    <template v-if="!errorTitle" #right-header>
      <CustomActions
        v-if="document._actions?.length"
        :actions="document._actions"
      />
      <CustomActions
        v-if="document.actions?.length"
        :actions="document.actions"
      />

      <!-- Lead Routing Buttons -->
      <div v-if="doc.current_department" class="flex gap-2">
        <Dropdown :options="routingOptions" placement="right">
          <template #default="{ open }">
            <Button
              :label="__('Lead Routing')"
              :iconRight="open ? 'chevron-up' : 'chevron-down'"
              variant="outline"
            >
              <template #prefix>
                <Icon icon="route" class="h-4 w-4" />
              </template>
            </Button>
          </template>
        </Dropdown>
      </div>

      <AssignTo v-model="assignees.data" doctype="CRM Lead" :docname="leadId" />
      <Dropdown
        v-if="doc && document.statuses"
        :options="statuses"
        placement="right"
      >
        <template #default="{ open }">
          <Button
            v-if="doc.status"
            :label="doc.status"
            :iconRight="open ? 'chevron-up' : 'chevron-down'"
          >
            <template #prefix>
              <IndicatorIcon :class="getLeadStatus(doc.status).color" />
            </template>
          </Button>
        </template>
      </Dropdown>

      <Button
        :label="__('Convert to Deal')"
        variant="solid"
        @click="showConvertToDealModal = true"
      />
    </template>
  </LayoutHeader>
  <div v-if="doc.name" class="flex h-full overflow-hidden">
    <Tabs
      v-model="tabIndex"
      :tabs="tabs"
      class="flex flex-1 overflow-hidden flex-col [&_[role='tab']]:px-0 [&_[role='tablist']]:px-5 [&_[role='tablist']]:gap-7.5 [&_[role='tabpanel']:not([hidden])]:flex [&_[role='tabpanel']:not([hidden])]:grow"
    >
      <template #tab-panel>
        <Activities
          ref="activities"
          doctype="CRM Lead"
          :docname="leadId"
          :tabs="tabs"
          v-model:reload="reload"
          v-model:tabIndex="tabIndex"
          @beforeSave="saveChanges"
          @afterSave="reloadAssignees"
        />
      </template>
    </Tabs>
    <Resizer class="flex flex-col justify-between border-l" side="right">
      <div
        class="flex h-[45px] cursor-copy items-center border-b px-5 py-2.5 text-lg font-medium text-ink-gray-9"
        @click="copyToClipboard(leadId)"
      >
        {{ __(leadId) }}
      </div>

      <!-- Department Routing Info -->
      <div v-if="doc.current_department" class="border-b px-5 py-3">
        <div class="text-sm font-medium text-ink-gray-7 mb-2">
          {{ __('Department Routing') }}
        </div>
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="text-xs text-ink-gray-5">{{
              __('Current Department')
            }}</span>
            <span class="text-xs font-medium text-ink-gray-9">{{
              doc.current_department
            }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-xs text-ink-gray-5">{{ __('Status') }}</span>
            <span
              class="text-xs font-medium"
              :class="getDepartmentStatusColor(doc.department_status)"
            >
              {{ doc.department_status || '—' }}
            </span>
          </div>
          <div
            v-if="doc.current_shift"
            class="flex items-center justify-between"
          >
            <span class="text-xs text-ink-gray-5">{{ __('Shift') }}</span>
            <span class="text-xs font-medium text-ink-gray-9">{{
              doc.current_shift
            }}</span>
          </div>
        </div>
      </div>
      <FileUploader
        @success="(file) => updateField('image', file.file_url)"
        :validateFile="validateIsImageFile"
      >
        <template #default="{ openFileSelector, error }">
          <div class="flex items-center justify-start gap-5 border-b p-5">
            <div class="group relative size-12">
              <Avatar
                size="3xl"
                class="size-12"
                :label="title"
                :image="doc.image"
              />
              <component
                :is="doc.image ? Dropdown : 'div'"
                v-bind="
                  doc.image
                    ? {
                        options: [
                          {
                            icon: 'upload',
                            label: doc.image
                              ? __('Change image')
                              : __('Upload image'),
                            onClick: openFileSelector,
                          },
                          {
                            icon: 'trash-2',
                            label: __('Remove image'),
                            onClick: () => updateField('image', ''),
                          },
                        ],
                      }
                    : { onClick: openFileSelector }
                "
                class="!absolute bottom-0 left-0 right-0"
              >
                <div
                  class="z-1 absolute bottom-0.5 left-0 right-0.5 flex h-9 cursor-pointer items-center justify-center rounded-b-full bg-black bg-opacity-40 pt-3 opacity-0 duration-300 ease-in-out group-hover:opacity-100"
                  style="
                    -webkit-clip-path: inset(12px 0 0 0);
                    clip-path: inset(12px 0 0 0);
                  "
                >
                  <CameraIcon class="size-4 cursor-pointer text-white" />
                </div>
              </component>
            </div>
            <div class="flex flex-col gap-2.5 truncate">
              <Tooltip :text="doc.lead_name || __('Set first name')">
                <div class="truncate text-2xl font-medium text-ink-gray-9">
                  {{ title }}
                </div>
              </Tooltip>
              <div class="flex gap-1.5">
                <Button
                  v-if="callEnabled"
                  :tooltip="__('Make a call')"
                  :loading="store.callLoading"
                  :icon="PhoneIcon"
                  @click="
                    () =>
                      doc.mobile_no
                        ? store.makeCall(doc.mobile_no)
                        : toast.error(__('No phone number set'))
                  "
                />

                <Button
                  :tooltip="__('Send an email')"
                  :icon="Email2Icon"
                  @click="
                    doc.email ? openEmailBox() : toast.error(__('No email set'))
                  "
                />
                <Button
                  :tooltip="__('Go to website')"
                  :icon="LinkIcon"
                  @click="
                    doc.website
                      ? openWebsite(doc.website)
                      : toast.error(__('No website set'))
                  "
                />

                <Button
                  :tooltip="__('Attach a file')"
                  :icon="AttachmentIcon"
                  @click="showFilesUploader = true"
                />

                <Button
                  v-if="canDelete"
                  :tooltip="__('Delete')"
                  variant="subtle"
                  theme="red"
                  icon="trash-2"
                  @click="deleteLead"
                />
              </div>
              <ErrorMessage :message="__(error)" />
            </div>
          </div>
        </template>
      </FileUploader>
      <SLASection
        v-if="doc.sla_status"
        v-model="doc"
        @updateField="updateField"
      />
      <div
        v-if="sections.data"
        class="flex flex-1 flex-col justify-between overflow-hidden"
      >
        <SidePanelLayout
          :sections="sections.data"
          doctype="CRM Lead"
          :docname="leadId"
          @reload="sections.reload"
          @afterFieldChange="reloadAssignees"
        />
      </div>
    </Resizer>
    <Dialog
      v-model="showTransferModal"
      :options="{
        title: __('Add Transfer Notes'),
        size: 'sm',
      }"
    >
      <template #body-content>
        <div class="p-4 flex flex-col gap-4">
          <p class="text-sm text-gray-600">
            {{ __('Selected Department:') }}
            <strong>{{ transferData.target }}</strong>
          </p>
          <FormControl
            type="textarea"
            :label="__('Reason / Notes (optional)')"
            v-model="transferData.notes"
            variant="outline"
            placeholder="Enter notes here if any..."
            rows="4"
          />
        </div>
      </template>
      <template #actions>
        <div class="flex justify-end gap-2 p-3 border-t">
          <Button variant="ghost" @click="showTransferModal = false">
            {{ __('Back') }}
          </Button>
          <Button variant="solid" theme="gray" @click="executeTransfer">
            {{ __('Transfer Now') }}
          </Button>
        </div>
      </template>
    </Dialog>
  </div>
  <ErrorPage
    v-else-if="errorTitle"
    :errorTitle="errorTitle"
    :errorMessage="errorMessage"
  />
  <ConvertToDealModal
    v-if="showConvertToDealModal"
    v-model="showConvertToDealModal"
    :lead="doc"
  />
  <FilesUploader
    v-model="showFilesUploader"
    doctype="CRM Lead"
    :docname="leadId"
    @after="
      () => {
        activities?.all_activities?.reload()
        changeTabTo('attachments')
      }
    "
  />
  <DeleteLinkedDocModal
    v-if="showDeleteLinkedDocModal"
    v-model="showDeleteLinkedDocModal"
    :doctype="'CRM Lead'"
    :docname="leadId"
    name="Leads"
  />
</template>
<script setup>
import DeleteLinkedDocModal from '@/components/DeleteLinkedDocModal.vue'
import ErrorPage from '@/components/ErrorPage.vue'
import Icon from '@/components/Icon.vue'
import Resizer from '@/components/Resizer.vue'
import ActivityIcon from '@/components/Icons/ActivityIcon.vue'
import EmailIcon from '@/components/Icons/EmailIcon.vue'
import Email2Icon from '@/components/Icons/Email2Icon.vue'
import CommentIcon from '@/components/Icons/CommentIcon.vue'
import DetailsIcon from '@/components/Icons/DetailsIcon.vue'
import EventIcon from '@/components/Icons/EventIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import TaskIcon from '@/components/Icons/TaskIcon.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import WhatsAppIcon from '@/components/Icons/WhatsAppIcon.vue'
import IndicatorIcon from '@/components/Icons/IndicatorIcon.vue'
import CameraIcon from '@/components/Icons/CameraIcon.vue'
import LinkIcon from '@/components/Icons/LinkIcon.vue'
import BellIcon from '@/components/Icons/BellIcon.vue'
import AttachmentIcon from '@/components/Icons/AttachmentIcon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Activities from '@/components/Activities/Activities.vue'
import AssignTo from '@/components/AssignTo.vue'
import FilesUploader from '@/components/FilesUploader/FilesUploader.vue'
import SidePanelLayout from '@/components/SidePanelLayout.vue'
import SLASection from '@/components/SLASection.vue'
import CustomActions from '@/components/CustomActions.vue'
import ConvertToDealModal from '@/components/Modals/ConvertToDealModal.vue'
import {
  openWebsite,
  setupCustomizations,
  copyToClipboard,
  validateIsImageFile,
} from '@/utils'
import { getView } from '@/utils/view'
import { getSettings } from '@/stores/settings'
import { globalStore } from '@/stores/global'
import { statusesStore } from '@/stores/statuses'
import { getMeta } from '@/stores/meta'
import { useDocument } from '@/data/document'
import { whatsappEnabled, callEnabled } from '@/composables/settings'
import {
  createResource,
  FileUploader,
  Dropdown,
  Tooltip,
  Avatar,
  Tabs,
  Breadcrumbs,
  call,
  usePageMeta,
  toast,
} from 'frappe-ui'
import { ref, computed, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useActiveTabManager } from '@/composables/useActiveTabManager'
import { Dialog, FormControl, Button } from 'frappe-ui'

const { brand } = getSettings()
const store = globalStore()
const { $dialog } = store
const { statusOptions, getLeadStatus } = statusesStore()
const { doctypeMeta } = getMeta('CRM Lead')

const route = useRoute()
const router = useRouter()

const showTransferModal = ref(false)
const transferTargets = ref([])
const transferData = ref({
  target: '',
  notes: '',
})

const props = defineProps({
  leadId: {
    type: String,
    required: true,
  },
})

const reload = ref(false)
const activities = ref(null)
const errorTitle = ref('')
const errorMessage = ref('')
const showDeleteLinkedDocModal = ref(false)
const showConvertToDealModal = ref(false)

const showFilesUploader = ref(false)

const { triggerOnChange, assignees, permissions, document, scripts, error } =
  useDocument('CRM Lead', props.leadId)

const canDelete = computed(() => permissions.data?.permissions?.delete || false)

const doc = computed(() => document.doc || {})

watch(error, (err) => {
  if (err) {
    errorTitle.value = __(
      err.exc_type == 'DoesNotExistError'
        ? 'Document not found'
        : 'Error occurred',
    )
    errorMessage.value = __(err.messages?.[0] || 'An error occurred')
  } else {
    errorTitle.value = ''
    errorMessage.value = ''
  }
})

watch(
  () => document.doc,
  async (_doc) => {
    if (scripts.data?.length) {
      let s = await setupCustomizations(scripts.data, {
        doc: _doc,
        $dialog,
        $socket: store.$socket,
        router,
        toast,
        updateField,
        createToast: toast.create,
        deleteDoc: deleteLead,
        call,
      })
      document._actions = s.actions || []
      document._statuses = s.statuses || []
    }
  },
  { once: true },
)

const breadcrumbs = computed(() => {
  let items = [{ label: __('Leads'), route: { name: 'Leads' } }]

  if (route.query.view || route.query.viewType) {
    let view = getView(route.query.view, route.query.viewType, 'CRM Lead')
    if (view) {
      items.push({
        label: __(view.label),
        icon: view.icon,
        route: {
          name: 'Leads',
          params: { viewType: route.query.viewType },
          query: { view: route.query.view },
        },
      })
    }
  }

  items.push({
    label: title.value,
    route: { name: 'Lead', params: { leadId: props.leadId } },
  })
  return items
})

const title = computed(() => {
  let t = doctypeMeta['CRM Lead']?.title_field || 'name'
  return doc.value?.[t] || props.leadId
})

const statuses = computed(() => {
  let customStatuses = document.statuses?.length
    ? document.statuses
    : document._statuses || []
  return statusOptions('lead', customStatuses, triggerStatusChange)
})

// Lead Routing functionality
const routingOptions = computed(() => {
  if (!doc.value.current_department || doc.value.department_status === 'Done') {
    return []
  }

  const options = []

  // Mark Done button
  options.push({
    label: __('Mark Done'),
    icon: 'check-circle',
    onClick: () => markDepartmentDone(),
  })

  // Send Back button
  options.push({
    label: __('Send Back'),
    icon: 'arrow-left',
    onClick: () => sendBackToDepartment(),
  })

  // Reject to Onboarding button
  options.push({
    label: __('Reject to Onboarding'),
    icon: 'rotate-ccw',
    onClick: () => rejectToOnboarding(),
  })

  // Transfer to Department button
  options.push({
    label: __('Transfer to Department'),
    icon: 'arrow-right',
    onClick: () => showTransferDialog(),
  })

  return options
})

// Routing methods
async function markDepartmentDone() {
  $dialog({
    title: __('Mark Department Done'),
    message: __(
      "Mark this department's work as Done and move lead to the next department?",
    ),
    actions: [
      {
        label: __('Cancel'),
        variant: 'ghost',
      },
      {
        label: __('Mark Done'),
        variant: 'solid',
        theme: 'red',
        onClick: async (close) => {
          try {
            const result = await call(
              'lead_routing.api.lead_transfer.mark_department_done',
              {
                lead_name: props.leadId,
              },
            )

            if (result.status === 'completed') {
              toast.success(__('🎉 Lead lifecycle completed!'))
            } else {
              toast.success(__('✅ Lead moved to {0}', [result.to]))
            }

            // Reload the document and assignees
            document.reload()
            assignees.reload()
            reload.value = true
            close()
          } catch (error) {
            handleRoutingError(error)
          }
        },
      },
    ],
  })
}

async function sendBackToDepartment() {
  $dialog({
    title: __('Send Back'),
    message: __('Send this lead back to its previous department?'),
    actions: [
      {
        label: __('Cancel'),
        variant: 'ghost',
      },
      {
        label: __('Send Back'),
        variant: 'solid',
        theme: 'red',
        onClick: async (close) => {
          try {
            const result = await call(
              'lead_routing.api.lead_transfer.send_back_to_department',
              {
                lead_name: props.leadId,
              },
            )

            toast.success(__('↩️ Lead sent back to {0}', [result.to]))
            document.reload()
            assignees.reload()
            reload.value = true
            close()
          } catch (error) {
            handleRoutingError(error)
          }
        },
      },
    ],
  })
}

async function rejectToOnboarding() {
  $dialog({
    title: __('Reject to Onboarding'),
    message: __(
      'Reject this lead back to Seller Onboarding? This is typically used when the lead needs to restart the process.',
    ),
    actions: [
      {
        label: __('Cancel'),
        variant: 'ghost',
      },
      {
        label: __('Reject'),
        variant: 'solid',
        theme: 'red',
        onClick: async (close) => {
          try {
            const result = await call(
              'lead_routing.api.lead_transfer.reject_to_onboarding',
              {
                lead_name: props.leadId,
              },
            )

            toast.success(__('🔄 Lead rejected back to {0}', [result.to]))
            document.reload()
            assignees.reload()
            reload.value = true
            close()
          } catch (error) {
            handleRoutingError(error)
          }
        },
      },
    ],
  })
}

async function showTransferDialog() {
  try {
    const targets = await call(
      'lead_routing.api.lead_transfer.get_transfer_targets',
      {
        current_department: doc.value.current_department,
      },
    )

    if (!targets || targets.length === 0) {
      toast.error(__('No other departments available.'))
      return
    }

    $dialog({
      title: __('Transfer Lead to Department'),
      message: __('Which department would you like to transfer to?'),
      actions: [
        { label: __('Cancel'), variant: 'ghost' },
        ...targets.map((target) => ({
          label: target.name,
          variant: 'solid',
          theme: 'blue',
          onClick: (close) => {
            transferData.value.target = target.name
            close()
            showTransferModal.value = true
          },
        })),
      ],
    })
  } catch (error) {
    handleRoutingError(error)
  }
}
async function executeTransfer() {
  try {
    await call('lead_routing.api.lead_transfer.manager_override_transfer', {
      lead_name: props.leadId,
      target_stage: transferData.value.target,
      notes: transferData.value.notes || '',
    })

    toast.success(__('⚡ Lead transferred successfully'))
    showTransferModal.value = false
    transferData.value.notes = ''
    document.reload()
  } catch (error) {
    handleRoutingError(error)
  }
}

function handleRoutingError(error) {
  let userMessage = ''
  if (error._server_messages) {
    try {
      const serverMsgs = JSON.parse(error._server_messages)
      const parsedMsg = JSON.parse(serverMsgs[0])
      userMessage = parsedMsg.message
    } catch (e) {}
  }

  if (!userMessage && error.messages && error.messages.length > 0) {
    userMessage = error.messages[0]
  } else if (!userMessage && error.exception) {
    userMessage = error.exception.replace(/^frappe\.exceptions\.\w+:\s*/, '')
  } else if (!userMessage) {
    userMessage = error.message || __('Action failed. Please try again.')
  }

  if (userMessage.includes('Document has been modified')) {
    toast.warning(__('Data is out of date. Refreshing...'))
    document.reload()
  } else {
    toast.error(userMessage)
  }
}

function getDepartmentStatusColor(status) {
  switch (status) {
    case 'Working':
      return 'text-blue-600'
    case 'Done':
      return 'text-green-600'
    case 'Rejected':
      return 'text-red-600'
    default:
      return 'text-ink-gray-9'
  }
}

usePageMeta(() => {
  return { title: title.value, icon: brand.favicon }
})

const tabs = computed(() => {
  let tabOptions = [
    {
      name: 'Activity',
      label: __('Activity'),
      icon: ActivityIcon,
    },
    {
      name: 'Emails',
      label: __('Emails'),
      icon: EmailIcon,
    },
    {
      name: 'Comments',
      label: __('Comments'),
      icon: CommentIcon,
    },
    {
      name: 'Data',
      label: __('Data'),
      icon: DetailsIcon,
    },
    {
      name: 'Events',
      label: __('Events'),
      icon: EventIcon,
    },
    {
      name: 'Calls',
      label: __('Calls'),
      icon: PhoneIcon,
    },
    {
      name: 'Tasks',
      label: __('Tasks'),
      icon: TaskIcon,
    },
    {
      name: 'Notes',
      label: __('Notes'),
      icon: NoteIcon,
    },
    {
      name: 'Follow Up',
      label: __('Follow Up'),
      icon: BellIcon,
    },
    {
      name: 'Attachments',
      label: __('Attachments'),
      icon: AttachmentIcon,
    },
    {
      name: 'WhatsApp',
      label: __('WhatsApp'),
      icon: WhatsAppIcon,
      condition: () => whatsappEnabled.value,
    },
  ]
  return tabOptions.filter((tab) => (tab.condition ? tab.condition() : true))
})

const { tabIndex, changeTabTo } = useActiveTabManager(tabs, 'lastLeadTab')

const sections = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_sidepanel_sections',
  cache: ['sidePanelSections', 'CRM Lead'],
  params: { doctype: 'CRM Lead' },
  auto: true,
})

async function triggerStatusChange(value) {
  await triggerOnChange('status', value)
  document.save.submit()
}

function updateField(name, value) {
  value = Array.isArray(name) ? '' : value
  let oldValues = Array.isArray(name) ? {} : doc.value[name]

  if (Array.isArray(name)) {
    name.forEach((field) => (doc.value[field] = value))
  } else {
    doc.value[name] = value
  }

  document.save.submit(null, {
    onSuccess: () => (reload.value = true),
    onError: (err) => {
      if (Array.isArray(name)) {
        name.forEach((field) => (doc.value[field] = oldValues[field]))
      } else {
        doc.value[name] = oldValues
      }
      toast.error(err.messages?.[0] || __('Error updating field'))
    },
  })
}

function deleteLead() {
  showDeleteLinkedDocModal.value = true
}

function openEmailBox() {
  let currentTab = tabs.value[tabIndex.value]
  if (!['Emails', 'Comments', 'Activities'].includes(currentTab.name)) {
    activities.value.changeTabTo('emails')
  }
  nextTick(() => (activities.value.emailBox.show = true))
}

function saveChanges(data) {
  document.save.submit(null, {
    onSuccess: () => reloadAssignees(data),
  })
}

function reloadAssignees(data) {
  if (data?.hasOwnProperty('lead_owner')) {
    assignees.reload()
  }
}
</script>