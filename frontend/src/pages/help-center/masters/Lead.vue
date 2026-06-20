<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Leads</h1>

      <p class="mb-6 leading-relaxed">
        The Leads page displays all your potential customers in one place. Each lead entry shows key details like the 
        <strong>Name</strong>, <strong>Organization</strong>, <strong>Status</strong>, <strong>Email</strong>,
        <strong>Mobile No</strong>, <strong>Assigned To</strong>, and <strong>Last Modified</strong> giving
        your team a quick snapshot without opening individual records. Leads can be viewed in
        <strong>List</strong>, <strong>Kanban</strong>, or <strong>Group By</strong> views. Data can be
        imported or exported in bulk, columns can be organized in a custom manner, and new leads can be
        created and managed directly from this page.
      </p>

      <h2 id="creating-a-lead" class="text-2xl font-semibold mt-10 mb-4">Creating a New Lead</h2>
      <p class="mb-4 leading-relaxed">
        Click the <strong>+ Create</strong> button at the top right of the Leads page. A quick entry form
        appears with the following fields:
      </p>
      <ul class="list-disc ml-6 mb-4 space-y-2 marker:text-pink-500">
        <li><strong>Salutation</strong> — title such as Mr, Mrs, Dr, etc.</li>
        <li><strong>First Name</strong> and <strong>Last Name</strong></li>
        <li><strong>Email, Mobile No., Gender</strong></li>
        <li><strong>Organization</strong>, <strong>Website</strong>, <strong>No. of Employees</strong></li>
        <li><strong>Territory</strong>, <strong>Annual Revenue</strong>, <strong>Industry</strong></li>
        <li><strong>Status</strong> — defaults to <em>New</em></li>
        <li><strong>Lead Owner</strong> — the agent responsible for this lead</li>
      </ul>

      <img
        src="@/assets/leads-create.png"
        class="rounded-lg shadow-md mb-4 w-full object-contain"
        alt="Create Lead Form"
      />

      <p class="mb-6 leading-relaxed">
        The quick entry layout can be customized means the fields can be added, removed, or rearranged using the
        <strong>Edit Quick Entry Layout</strong> option. Once done, click <strong>Create</strong> to save the lead.
      </p>

      <img
        src="@/assets/leads-quick-entry-layout.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="Edit Quick Entry Layout"
      />

      <h2 id="managing-a-lead" class="text-2xl font-semibold mt-10 mb-4">Managing an Individual Lead</h2>
      <p class="mb-4 leading-relaxed">
        Click on any lead from the list to open its detail page. At the top you'll find the lead's name,
        current status, a <strong>Convert to Deal</strong> button, and quick action icons for calling,
        emailing, linking, and deleting. The right panel shows all lead details like organization, territory,
        industry, job title, source, and lead owner which can be edited inline.
      </p>
      <p class="mb-4 leading-relaxed">
        The <strong>+ New</strong> dropdown at the top of the activity area lets you quickly:
      </p>
      <ul class="list-disc ml-6 mb-4 space-y-2 marker:text-pink-500">
        <li>Send a <strong>New Email</strong></li>
        <li>Add a <strong>New Comment</strong></li>
        <li><strong>Schedule an Event</strong></li>
        <li><strong>Log a Call</strong> or <strong>Make a Call</strong></li>
        <li>Add a <strong>New Note</strong> or <strong>New Task</strong></li>
        <li><strong>Upload Attachment</strong></li>
        <li>Send a <strong>New WhatsApp Message</strong></li>
      </ul>

      <img
        src="@/assets/leads-detail.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="Lead Detail Page"
      />

      <h2 id="activity-tabs" class="text-2xl font-semibold mt-10 mb-4">Activity Tabs</h2>
      <p class="mb-4 leading-relaxed">
        The lead detail page is organized into tabs so all related information stays in one place:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Activity</strong> — full timeline of all interactions and changes</li>
        <li><strong>Emails</strong> — all email threads with this lead</li>
        <li><strong>Comments</strong> — internal team comments</li>
        <li><strong>Data</strong> — raw field data and custom fields</li>
        <li><strong>Events</strong> — scheduled meetings and events</li>
        <li><strong>Calls</strong> — inbound and outbound call history</li>
        <li><strong>Tasks</strong> — to-do items linked to this lead</li>
        <li><strong>Notes</strong> — internal notes about this lead</li>
        <li><strong>Follow Up</strong> — reminders and follow-up schedules</li>
        <li><strong>Attachments</strong> — files and documents linked to this lead</li>
        <li><strong>WhatsApp</strong> — WhatsApp conversation history (if enabled)</li>
      </ul>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
        <p class="text-sm text-blue-800 dark:text-blue-200">
          <strong>Tip:</strong> Once a lead is qualified and ready to move forward, click
          <strong>Convert to Deal</strong> at the top right of the lead page. This creates a new Deal
          pre-filled with the lead's information.
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
  const headings = document.querySelectorAll('.help-content h2,.help-content h3')
  toc.value = Array.from(headings).map((h) => ({ id: h.id, text: h.innerText }))
})
</script>

<style>
html { scroll-behavior: smooth; }
</style>
