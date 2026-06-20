<template>
  <div class="flex">
    <div class=" help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Notes</h1>

      <p class="mb-6 leading-relaxed">
        Notes let you capture important information about a lead, deal, or contact. They're
        <strong>internal</strong> means only your team can see them, not the customer. Use notes to keep
        context alive across your team so nothing important gets lost between conversations.
      </p>

      <h2 id="viewing-notes" class="text-2xl font-semibold mt-10 mb-4">Viewing Notes</h2>
      <p class="mb-4 leading-relaxed">
        Click <strong>Notes</strong> in the sidebar to see all standalone notes in a card-style view.
        Each card shows the note's <strong>Title</strong> and a preview of its <strong>Content</strong>,
        along with who last edited it and when. Use <strong>Filter</strong> and <strong>Sort</strong>
        at the top right to find notes quickly.
      </p>

      <h2 id="creating-a-note" class="text-2xl font-semibold mt-10 mb-4">Creating a Note</h2>
      <p class="mb-4 leading-relaxed">
        There are two ways to create a note:
      </p>
      <ul class="list-disc ml-6 mb-4 space-y-2 marker:text-pink-500">
        <li>
          <strong>From the sidebar</strong> — click <strong>Notes → + Create</strong> to create a
          standalone note not tied to any specific record
        </li>
        <li>
          <strong>From inside a Lead or Deal</strong> — click the <strong>Notes</strong> tab and add
          a note directly linked to that record
        </li>
      </ul>
      <p class="mb-6 leading-relaxed">
        Each note requires a <strong>Title</strong> and <strong>Content</strong>. Click
        <strong>Create</strong> to save it.
      </p>

      <img
        src="@/assets/notes-create.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="Create Note Form"
      />

      <h2 id="rich-text-editor" class="text-2xl font-semibold mt-10 mb-4">Rich Text Editor</h2>
      <p class="mb-4 leading-relaxed">
        Notes support rich text formatting — <strong>bold</strong>, <em>italic</em>, bullet lists,
        headings, links,background colour and more. Use the toolbar at the top of the editor to format your note content
        exactly the way you need it.
      </p>

      <h2 id="tips-for-notes" class="text-2xl font-semibold mt-10 mb-4">Tips for Using Notes</h2>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>After every call, add a quick note summarizing what was discussed</li>
        <li>Use notes to record customer preferences, objections, or special requirements</li>
        <li>Notes appear in the <strong>Activity</strong> timeline so your whole team stays informed</li>
        <li>Pin important notes so they're easy to find later</li>
      </ul>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
        <p class="text-sm text-blue-800 dark:text-blue-200">
          <strong>Tip:</strong> Notes created from inside a Lead or Deal are linked to that record and
          show up in its activity timeline. Standalone notes from the sidebar are global and not tied
          to any specific lead or deal.
        </p>
      </div>
    </div>

    <aside class="w-64 hidden xl:block px-6">
      <div class="sticky top-24">
        <h3 class="text-sm font-semibold text-gray-500 mb-3">On this page</h3>
        <ul class="space-y-2 text-sm">
          <li v-for="item in toc" :key="item.id">
            <a :href="'#' + item.id" class="text-gray-600 hover:text-pink-500">{{ item.text }}</a>
          </li>
        </ul>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const toc = ref([])
onMounted(() => {
  const headings = document.querySelectorAll('.help-content h2, .help-content h3')
  toc.value = Array.from(headings).map((h) => ({ id: h.id, text: h.innerText }))
})
</script>

<style>
html { scroll-behavior: smooth; }
</style>
