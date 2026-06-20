<template>
  <Dialog v-model="show" :options="{ size: 'xl' }">
    <template #body-title>
      <div class="flex items-center justify-between w-full pr-4">
        <div class="flex items-center gap-3">
          <div
            class="flex items-center justify-center w-10 h-10 rounded-lg bg-gray-50 dark:bg-gray-800 text-ink-gray-7 dark:text-gray-300"
          >
            <span class="text-lg">📝</span>
          </div>
          <h3
            class="text-xl font-bold tracking-tight text-ink-gray-9 dark:text-white"
          >
            {{ editMode ? __('Edit Note') : __('Create Note') }}
          </h3>
        </div>

        <Button
          v-if="_note?.reference_docname"
          variant="ghost"
          class="!text-blue-600 hover:!bg-blue-50 dark:hover:!bg-gray-800"
          size="sm"
          :label="
            _note.reference_doctype == 'CRM Deal'
              ? __('Open Deal')
              : __('Open Lead')
          "
          :iconRight="ArrowUpRightIcon"
          @click="redirect()"
        />
      </div>
    </template>

    <template #body-content>
      <div
        class="flex flex-col gap-6 py-2 rounded-xl p-4 border transition-all duration-200"
        :style="{
          backgroundColor: _note?.background_color
            ? _note.background_color + 'cc'
            : '',
          borderColor: _note?.background_color || '#e5e7eb',
        }"
      >
        <div class="space-y-1">
          <FormControl
            ref="title"
            :label="__('Title')"
            label-class="text-black dark:text-white"
            v-model="_note.title"
            :placeholder="__('e.g. Weekly Sync Call')"
            required
            class="transition-all duration-200"
            :input-props="{
              class:
                'bg-white text-black border border-gray-200 dark:bg-gray-900 dark:text-white dark:border-gray-700 transition-all ',
              style: {
                borderColor: _note?.background_color || '#e5e7eb',
              },
            }"
          />
        </div>

        <div class="flex flex-col">
          <label class="mb-2 text-sm font-medium !text-black dark:!text-white">
            {{ __('Content') }}
          </label>
          <div class="relative group">
            <TextEditor
              variant="outline"
              ref="content"
              editor-class="no-scrollbar overflow-auto min-h-[220px] max-h-96 p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-[#232323] shadow-sm transition-all text-gray-800 dark:!text-white leading-relaxed hover:border-current focus:border-current focus:ring-2 focus:ring-blue-100 dark:focus:ring-blue-900/30"
              :bubbleMenu="true"
              :content="_note.content"
              @change="(val) => (_note.content = val)"
              :placeholder="__('Type your notes here...')"
            />
          </div>
        </div>

        <transition name="fade">
          <ErrorMessage
            class="p-3 rounded-lg bg-red-50 dark:bg-red-900/30 border border-red-100 dark:border-red-800 mt-2"
            v-if="error"
            :message="__(error)"
          />
        </transition>
      </div>
    </template>

    <template #actions>
      <div
        class="flex items-center justify-between w-full pt-4 border-t border-gray-100 dark:border-gray-700"
      >
        <span class="text-xs text-ink-gray-4 dark:text-gray-400 italic"
          >Auto-saves on update</span
        >
        <Button
          :label="editMode ? __('Update Note') : __('Create Note')"
          variant="solid"
          class="!px-6 !py-2.5 !rounded-lg !bg-gray-900 hover:!bg-black dark:!bg-white dark:!text-black transition-colors shadow-md active:scale-95"
          @click="updateNote"
        />
      </div>
    </template>
  </Dialog>
</template>
<script setup>
import ArrowUpRightIcon from '@/components/Icons/ArrowUpRightIcon.vue'
import { capture } from '@/telemetry'
import { TextEditor, call } from 'frappe-ui'
import { useOnboarding } from 'frappe-ui/frappe'
import { ref, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  note: {
    type: Object,
    default: {},
  },
  doctype: {
    type: String,
    default: 'CRM Lead',
  },
  doc: {
    type: String,
    default: '',
  },
})

const show = defineModel()
const notes = defineModel('reloadNotes')

const emit = defineEmits(['after'])

const router = useRouter()

const { updateOnboardingStep } = useOnboarding('frappecrm')

const error = ref(null)
const title = ref(null)
const editMode = ref(false)
let _note = ref({})

async function updateNote() {
  if (_note.value.name) {
    let d = await call('frappe.client.set_value', {
      doctype: 'FCRM Note',
      name: _note.value.name,
      fieldname: _note.value,
    })
    if (d.name) {
      notes.value?.reload()
      emit('after', d)
    }
  } else {
    let d = await call(
      'frappe.client.insert',
      {
        doc: {
          doctype: 'FCRM Note',
          title: _note.value.title,
          content: _note.value.content,
          reference_doctype: props.doctype,
          reference_docname: props.doc || '',
          background_color: _note.value.background_color || '',
        },
      },
      {
        onError: (err) => {
          if (err.error.exc_type == 'MandatoryError') {
            error.value = 'Title is mandatory'
          }
        },
      },
    )
    if (d.name) {
      updateOnboardingStep('create_first_note')
      capture('note_created')
      notes.value?.reload()
      emit('after', d, true)
    }
  }
  show.value = false
}

function redirect() {
  if (!props.note?.reference_docname) return
  let name = props.note.reference_doctype == 'CRM Deal' ? 'Deal' : 'Lead'
  let params = { leadId: props.note.reference_docname }
  if (name == 'Deal') {
    params = { dealId: props.note.reference_docname }
  }
  router.push({ name: name, params: params })
}

watch(
  () => show.value,
  (value) => {
    if (!value) return
    editMode.value = false
    nextTick(() => {
      title.value?.el?.focus()
      _note.value = { ...props.note }
      if (_note.value.title || _note.value.content) {
        editMode.value = true
      }
    })
  },
)
</script>

<style scoped>
/* Custom CSS to hide the scrollbar while allowing scrolling */
:deep(.no-scrollbar::-webkit-scrollbar) {
  display: none;
}

:deep(.no-scrollbar) {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* Fix label color */
:deep(label) {
  color: black !important;
}

.dark :deep(label) {
  color: white !important;
}
</style>
