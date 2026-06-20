<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Deals</h1>

      <p class="mb-6 leading-relaxed">
        A <strong>Deal</strong> is a qualified sales opportunity. Once a lead is ready to buy, you convert
        it to a Deal and track it through your sales pipeline until it's won or lost. The Deals page shows
        each deal's <strong>Organization</strong> and <strong>Last Modified</strong> date, and supports
        bulk data import/export, custom column arrangement, and direct deal creation.
      </p>

      <h2 id="creating-a-deal" class="text-2xl font-semibold mt-10 mb-4">Creating a New Deal</h2>
      <p class="mb-4 leading-relaxed">
        Click Deals in the sidebar. Click <strong>+ Create</strong> at the top right of the Deals page. The Create Deal form lets you
        either link an existing organization and contact using the toggles at the top, or fill in details
        from scratch:
      </p>
      <ul class="list-disc ml-6 mb-4 space-y-2 marker:text-pink-500">
        <li><strong>Organization Name</strong>, <strong>Website</strong>, <strong>No. of Employees</strong></li>
        <li><strong>Territory</strong>, <strong>Annual Revenue</strong>, <strong>Industry</strong></li>
        <li><strong>Salutation</strong>, <strong>First Name</strong>, <strong>Last Name</strong></li>
        <li><strong>Primary Email</strong>, <strong>Primary Mobile No</strong>, <strong>Gender</strong></li>
        <li><strong>Status</strong> — defaults to <em>Qualification</em></li>
        <li><strong>Deal Owner</strong> — the agent responsible for this deal</li>
      </ul>
      <p class="mb-4 leading-relaxed">
        The field layout can be customized using the <strong>Edit fields layout</strong> option at the top
        right of the form. Click <strong>Create</strong> to save.
      </p>

      <img
        src="@/assets/deals-create.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="Create Deal Form"
      />

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-8">
        <p class="text-sm text-blue-800 dark:text-blue-200">
          <strong>Recommended:</strong> Create deals by converting a Lead rather than manually — this
          automatically carries over the contact information and keeps your data consistent.
        </p>
      </div>

      <h2 id="pipeline-stages" class="text-2xl font-semibold mt-10 mb-4">Deal Stages (Pipeline)</h2>
      <p class="mb-4 leading-relaxed">
        Deals move through pipeline stages that reflect where the opportunity stands. Common stages include:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Qualification</strong> — confirming the deal is real and worth pursuing</li>
        <li><strong>Demo / Meeting</strong> — presenting your product or service</li>
        <li><strong>Proposal</strong> — sending a quote or formal proposal</li>
        <li><strong>Negotiation</strong> — discussing terms and pricing</li>
        <li><strong>Closed Won</strong> — deal is successfully closed</li>
        <li><strong>Closed Lost</strong> — deal did not go through</li>
      </ul>
      <p class="mb-6 leading-relaxed">
        Your administrator may have customized these stages.</p>

      <h2 id="managing-a-deal" class="text-2xl font-semibold mt-10 mb-4">Managing an Individual Deal</h2>
          <p class="mb-4 leading-relaxed">
        Click any deal to open its detail page. The left side shows the full activity timeline and tabs,
        while the right panel displays deal-specific details — the deal's unique ID (e.g. CRM-DEAL-2026-00001),
        linked contacts, organization details, probability, next step, and deal owner. All fields are editable inline.
      </p>

      <img
        src="@/assets/deals-detail.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="Deal Detail Page"
      />

      <p class="mb-4 leading-relaxed">
        The right panel is organized into sections:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Contacts</strong> — linked contacts for this deal; add multiple contacts using the + button</li>
        <li><strong>Organization Details</strong> — organization name, website, territory, and annual revenue</li>
        <li><strong>Probability</strong> — likelihood of closing, used in forecasting</li>
        <li><strong>Next Step</strong> — a free-text field to note what action comes next</li>
        <li><strong>Deal Owner</strong> — the agent responsible for closing this deal</li>
      </ul>

      <p class="mb-4 leading-relaxed">
        The top right shows the current pipeline stage (e.g. <em>Qualification</em>) with a dropdown to
        move it forward, and an <strong>Assign to</strong> button for quick reassignment. The
        <strong>+ New</strong> dropdown in the activity area lets you log calls, send emails, add notes,
        schedule events, create tasks, upload attachments, and send WhatsApp messages, all linked directly
        to this deal.
      </p>

      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Activity</strong> — full timeline of all interactions and changes</li>
        <li><strong>Emails</strong> — all email threads related to this deal</li>
        <li><strong>Comments</strong> — internal team comments</li>
        <li><strong>Data</strong> — raw field data and custom fields</li>
        <li><strong>Events</strong> — scheduled meetings and events</li>
        <li><strong>Calls</strong> — inbound and outbound call history</li>
        <li><strong>Tasks</strong> — to-do items linked to this deal</li>
        <li><strong>Notes</strong> — internal notes about this deal</li>
        <li><strong>Follow Up</strong> — reminders and follow-up schedules</li>
        <li><strong>Attachments</strong> — files and documents linked to this deal</li>
        <li><strong>WhatsApp</strong> — WhatsApp conversation history (if enabled)</li>
      </ul>

      <h2 id="deal-value" class="text-2xl font-semibold mt-10 mb-4">Deal Value & Close Date</h2>
      <p class="mb-4 leading-relaxed">
        Always fill in the <strong>Deal Value</strong> (expected revenue) and <strong>Expected Close Date</strong>
        when working on a deal. These two fields power the dashboard forecasting charts and help managers
        prioritize which deals need attention.
      </p>
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
