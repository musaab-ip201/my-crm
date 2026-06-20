<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Lead History</h1>

      <p class="mb-6 leading-relaxed">
        <strong>Lead History</strong> gives you a complete audit trail of every change made to a lead —
        who changed what, and when. This transparency keeps your team accountable and helps managers
        understand exactly how a lead progressed through the pipeline.
      </p>

      <h2 id="viewing-history" class="text-2xl font-semibold mt-10 mb-4">Viewing Lead History</h2>
      <p class="mb-4 leading-relaxed">
        Open any lead and scroll to the <strong>Activity</strong> tab. The history log shows all field
        changes in chronological order, including:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Field name</strong> — which field was changed</li>
        <li><strong>Old value</strong> — what it was before</li>
        <li><strong>New value</strong> — what it was changed to</li>
        <li><strong>Changed by</strong> — the user who made the change</li>
        <li><strong>Timestamp</strong> — the exact date and time of the change</li>
      </ul>
      <p class="mb-6 leading-relaxed">
        Each change is logged automatically no manual tracking needed. The history appears inline
        with other activity like calls, emails, and notes, giving you a complete timeline of everything
        that happened with the lead.
      </p>

      <img
        src="@/assets/leadhistory.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="Lead History in Activity Timeline"
      />

      <h2 id="why-it-matters" class="text-2xl font-semibold mt-10 mb-4">Why It Matters</h2>
      <p class="mb-4 leading-relaxed">
        Lead history helps managers track progress, resolve disputes, and understand how a lead moved
        through the pipeline. It also provides accountability across your sales team everyone can
        see who made what changes and when.
      </p>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
        <p class="text-sm text-blue-800 dark:text-blue-200">
          <strong>Tip:</strong> If a lead's status changed unexpectedly or a field was updated by
          mistake, check the history log to see exactly what happened and who made the change. This
          makes troubleshooting and training much easier.
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
