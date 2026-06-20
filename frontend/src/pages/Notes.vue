<template>
  <LayoutHeader>
    <template #left-header>
      <ViewBreadcrumbs v-model="viewControls" routeName="Notes" />
    </template>
    <template #right-header>
      <Button
        variant="solid"
        :label="__('Create')"
        iconLeft="plus"
        @click="createNote"
      />
    </template>
  </LayoutHeader>

  <ViewControls
    ref="viewControls"
    v-model="notes"
    v-model:loadMore="loadMore"
    v-model:updatedPageCount="updatedPageCount"
    doctype="FCRM Note"
    :options="{
      hideColumnsButton: true,
      defaultViewName: __('Notes View'),
      fields: [
        'name',
        'title',
        'content',
        'owner',
        'creation',
        'background_color',
      ],
      rows: [
        'name',
        'title',
        'content',
        'owner',
        'creation',
        'background_color',
      ],
    }"
  />
  <div class="flex-1 overflow-y-auto bg-white dark:bg-black p-4">
    <div
      v-if="notes.data?.data?.length"
      class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
    >
      <div
        v-for="note in notes.data.data"
        :key="note.name"
        :style="{ backgroundColor: note.background_color || '' }"
        :class="[
          'group relative flex h-64 cursor-pointer flex-col justify-between overflow-hidden rounded-xl border p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl',

          note.background_color
            ? 'border-black/5 text-gray-900'
            : 'bg-white dark:bg-[#1a1a1a] border-gray-200 dark:border-gray-800 text-gray-900 dark:text-white',
        ]"
        @click="editNote(note)"
      >
        <div
          v-if="!note.background_color"
          class="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-purple-400 to-indigo-500 opacity-0 transition-opacity group-hover:opacity-100"
        ></div>

        <div class="flex flex-col gap-3">
          <div class="flex items-start justify-between">
            <h3
              :class="[
                'line-clamp-2 text-lg font-bold leading-tight',
                note.background_color
                  ? 'text-gray-900'
                  : 'text-gray-900 dark:text-gray-100',
              ]"
            >
              {{ note.title }}
            </h3>

            <div @click.stop>
              <Dropdown :options="getDropdownOptions(note)">
                <template #trigger="{ toggle }">
                  <Button
                    icon="more-horizontal"
                    variant="ghost"
                    :class="[
                      'hover:text-gray-900 dark:hover:text-white',
                      note.background_color
                        ? 'text-gray-600 dark:text-gray-200'
                        : 'text-gray-400 dark:text-gray-300',
                    ]"
                    @click.stop="toggle"
                  />
                </template>
              </Dropdown>
            </div>
          </div>

          <div class="relative max-h-32 overflow-hidden">
            <TextEditor
              v-if="note.content"
              :content="note.content"
              :editable="false"
              :editor-class="[
                'prose-sm max-w-none',
                note.background_color
                  ? 'text-gray-800'
                  : 'text-gray-700 dark:text-gray-300',
              ]"
            />
          </div>
        </div>

        <div
          :class="[
            'mt-4 flex items-center justify-between border-t pt-4',
            note.background_color
              ? 'border-black/5'
              : 'border-gray-100 dark:border-white/5',
          ]"
        >
          <div class="flex items-center gap-2">
            <UserAvatar :user="note.owner" size="sm" />
            <span
              :class="[
                'text-xs font-medium',
                note.background_color
                  ? 'text-gray-700'
                  : 'text-gray-600 dark:text-gray-400',
              ]"
            >
              {{ getUser(note.owner).full_name.split(' ')[0] }}
            </span>
          </div>
          <div
            :class="[
              'text-xs',
              note.background_color ? 'text-gray-500' : 'text-gray-400',
            ]"
          >
            {{ __(timeAgo(note.creation)) }}
          </div>
        </div>
      </div>
    </div>

    <div v-else class="flex h-full items-center justify-center">
      <div
        class="flex flex-col items-center gap-3 text-xl font-medium text-gray-400"
      >
        <NoteIcon class="h-12 w-12 opacity-50" />
        <span>{{ __('No Notes Found') }}</span>
        <Button :label="__('Create')" iconLeft="plus" @click="createNote" />
      </div>
    </div>
  </div>

  <NoteModal
    v-model="showNoteModal"
    v-model:reloadNotes="notes"
    :note="currentNote"
  />
</template>

<script setup>
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import NoteModal from '@/components/Modals/NoteModal.vue'
import ViewControls from '@/components/ViewControls.vue'
import { usersStore } from '@/stores/users'
import { timeAgo, formatDate } from '@/utils'
import {
  TextEditor,
  call,
  Dropdown,
  Tooltip,
  Button,
  FeatherIcon,
  ListFooter,
} from 'frappe-ui'
import { ref, watch, h } from 'vue'

const { getUser } = usersStore()
const showNoteModal = ref(false)
const currentNote = ref(null)
const notes = ref({})
const loadMore = ref(1)
const updatedPageCount = ref(20)
const viewControls = ref(null)

const colorPalette = [
  { name: 'Neutral', value: '#fef3c7' }, // light yellow
  { name: 'Positive', value: '#dcfce7' }, // light green
  { name: 'Negative', value: '#fecaca' }, // light red
  { name: 'Idea', value: '#f3e8ff' }, // light purple
  { name: 'Info', value: '#dbeafe' }, // light blue
]
function getDropdownOptions(note) {
  return [
    {
      group: __('Background Color'),
      hideLabel: false,
      items: colorPalette.map((color) => ({
        label: color.name,
        component: () =>
          h(
            'div',
            {
              class:
                'flex items-center gap-2 px-2 py-1 cursor-pointer rounded hover:bg-gray-100 dark:hover:bg-gray-700',
              onClick: (e) => {
                e.stopPropagation()
                updateNoteColor(note, color.value)
              },
            },
            [
              h('div', {
                class:
                  'w-5 h-5 rounded-full border border-gray-200 flex items-center justify-center',
                style: { backgroundColor: color.value },
              }),

              h(
                'span',
                { class: 'text-sm text-gray-700 dark:text-gray-200' },
                color.name,
              ),

              note.background_color === color.value
                ? h(FeatherIcon, {
                    name: 'check',
                    class: 'w-3 h-3 ml-auto text-gray-600 dark:text-gray-300',
                  })
                : null,
            ],
          ),
      })),
    },
    {
      label: __('Default Color'),
      icon: 'x',
      onClick: (e) => {
        if (e?.stopPropagation) e.stopPropagation()
        updateNoteColor(note, '')
      },
    },
    {
      label: __('Delete'),
      icon: 'trash-2',
      class: 'text-red-600',
      onClick: (e) => {
        if (e?.stopPropagation) e.stopPropagation()
        deleteNote(note.name)
      },
    },
  ]
}

async function updateNoteColor(note, color) {
  const originalColor = note.background_color
  note.background_color = color
  try {
    await call('crm.api.doc.update_note_color', {
      name: note.name,
      color: color,
    })
    // reload without resetting order — modified timestamp was not changed
    notes.value?.reload()
  } catch (e) {
    note.background_color = originalColor
    console.error('Failed to update color', e)
  }
}

watch(
  () => notes.value?.data?.page_length_count,
  (val, old_value) => {
    openNoteFromURL()
    if (!val || val === old_value) return
    updatedPageCount.value = val
  },
)

function createNote() {
  currentNote.value = {
    title: '',
    content: '',
  }
  showNoteModal.value = true
}

function editNote(note) {
  currentNote.value = note
  showNoteModal.value = true
}

async function deleteNote(name) {
  await call('frappe.client.delete', {
    doctype: 'FCRM Note',
    name,
  })
  notes.value.reload()
}

const openNoteFromURL = () => {
  const searchParams = new URLSearchParams(window.location.search)
  const noteName = searchParams.get('open')

  if (noteName && notes.value?.data?.data) {
    const foundNote = notes.value.data.data.find(
      (note) => note.name === noteName,
    )
    if (foundNote) {
      editNote(foundNote)
    }
    searchParams.delete('open')
    window.history.replaceState(null, '', window.location.pathname)
  }
}
</script>
