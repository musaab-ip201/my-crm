<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Contacts</h1>

      <p class="mb-6 leading-relaxed">
        A <strong>Contact</strong> is an individual person means a customer, prospect, or anyone you interact
        with. Contacts can be linked to Organizations and to Leads or Deals, keeping all your communication
        history tied to the right person.
      </p>

      <h2 id="viewing-contacts" class="text-2xl font-semibold mt-10 mb-4">Viewing Contacts</h2>
      <p class="mb-4 leading-relaxed">
        Click <strong>Contacts</strong> in the sidebar to see your contacts list. Each entry shows the
        contact's <strong>Email</strong> and <strong>Phone</strong> at a glance. You can search by name,
        email, or phone number, and filter by organization or other fields. Use <strong>Sort</strong>,
        <strong>Filter</strong>, and <strong>Columns</strong> at the top right to organize the view to
        your preference.
      </p>

      <h2 id="creating-a-contact" class="text-2xl font-semibold mt-10 mb-4">Creating a Contact</h2>
      <p class="mb-4 leading-relaxed">
        Click <strong>+ Create</strong> at the top right. The New Contact form includes:
      </p>
      <ul class="list-disc ml-6 mb-4 space-y-2 marker:text-pink-500">
        <li><strong>Salutation</strong> — Mr, Mrs, Dr, etc.</li>
        <li><strong>First Name</strong> and <strong>Last Name</strong></li>
        <li><strong>Email Address, Mobile No</strong> and <strong>Gender</strong></li>
        <li><strong>Company Name</strong> — links this contact to an organization</li>
        <li><strong>Designation</strong> — their role or job title</li>
        <li><strong>Address</strong></li>
      </ul>
      <p class="mb-6 leading-relaxed">
        Click <strong>Create</strong> to save the contact.
      </p>

      <img
        src="@/assets/contacts-create.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="New Contact Form"
      />

      <h2 id="inside-a-contact" class="text-2xl font-semibold mt-10 mb-4">Inside a Contact</h2>
      <p class="mb-4 leading-relaxed">
        Click any contact from the list to expand their full detail page. You'll see all their information
        alongside a complete activity timeline like every email, call, note, and task linked to this person.
        The detail page includes the same tabs as Leads and Deals:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Activity</strong> — full interaction timeline</li>
        <li><strong>Emails</strong> — all email threads with this contact</li>
        <li><strong>Comments</strong> — internal team comments</li>
        <li><strong>Data</strong> — all field data and custom fields</li>
        <li><strong>Events</strong> — scheduled meetings and events</li>
        <li><strong>Calls</strong> — call history linked to this contact</li>
        <li><strong>Tasks</strong> — to-do items linked to this contact</li>
        <li><strong>Notes</strong> — internal notes</li>
        <li><strong>Follow Up</strong> — follow-up reminders</li>
        <li><strong>Attachments</strong> — files and documents</li>
        <li><strong>WhatsApp</strong> — WhatsApp conversation history (if enabled)</li>
      </ul>
      <h2 id="calling-a-contact" class="text-2xl font-semibold mt-10 mb-4">Calling a Contact</h2>
      <p class="mb-4 leading-relaxed">
        Click the phone icon next to a contact's mobile number to call them directly from the CRM. The
        call is logged automatically and linked to this contact's activity timeline — no manual entry needed.
      </p>

      <h2 id="contact-vs-lead" class="text-2xl font-semibold mt-10 mb-4">IP CRM Contact vs Lead</h2>
      <p class="mb-4 leading-relaxed">
        A <strong>Lead</strong> is a sales opportunity. A <strong>Contact</strong> is the person behind it.
        When you convert a Lead to a Deal, a Contact is automatically created or linked if one already
        exists with the same phone number or email. This means you never lose the relationship history even
        as the opportunity moves through your pipeline.
      </p>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
        <p class="text-sm text-blue-800 dark:text-blue-200">
          <strong>Tip:</strong> A single Contact can be linked to multiple Deals. If the same person is
          involved in more than one opportunity, you don't need to create duplicate contacts — just link
          them to each deal from the Contacts section inside the deal.
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
