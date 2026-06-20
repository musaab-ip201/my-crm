<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Organizations</h1>

      <p class="mb-6 leading-relaxed">
        An <strong>Organization</strong> is a company or business entity. You can link multiple Contacts
        to one Organization, giving you a complete view of all your interactions with that company in one
        place. The Organizations list shows each company's <strong>Organization</strong> name,
        <strong>Website</strong>, <strong>Industry</strong>, <strong>Annual Revenue</strong>, and
        <strong>Last Modified</strong> date.
      </p>

      <h2 id="viewing-organizations" class="text-2xl font-semibold mt-10 mb-4">Viewing Organizations</h2>
      <p class="mb-4 leading-relaxed">
        Click <strong>Organizations</strong> in the sidebar. You'll see a list of all companies with their
        key details. Use <strong>Filter</strong>, <strong>Sort</strong>, and <strong>Columns</strong> at
        the top right to organize the view. Data can also be imported or exported in bulk.
      </p>

      <h2 id="creating-an-organization" class="text-2xl font-semibold mt-10 mb-4">Creating an Organization</h2>
      <p class="mb-4 leading-relaxed">
        Click <strong>+ Create</strong> at the top right. The New Organization form includes:
      </p>
      <ul class="list-disc ml-6 mb-4 space-y-2 marker:text-pink-500">
        <li><strong>Organization Name</strong></li>
        <li><strong>Website</strong> and <strong>Annual Revenue</strong></li>
        <li><strong>Territory</strong></li>
        <li><strong>No. of Employees</strong> and <strong>Industry</strong></li>
        <li><strong>Address</strong></li>
      </ul>
      <p class="mb-6 leading-relaxed">
        Click <strong>Create</strong> to save the organization.
      </p>

      <img
        src="@/assets/organizations-create.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="New Organization Form"
      />

      <h2 id="inside-an-organization" class="text-2xl font-semibold mt-10 mb-4">Inside an Organization</h2>
      <p class="mb-4 leading-relaxed">
        Click any organization from the list to open its detail page. The left panel shows all editable
        organization details like name, website, territory, industry, number of employees, and address.
        The right side is organized into two tabs:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Deals</strong> — all deals linked to this organization, with a count badge</li>
        <li><strong>Contacts</strong> — all contacts belonging to this company, with a count badge</li>
      </ul>
      <p class="mb-6 leading-relaxed">
        From here you can see every deal and contact associated with the company at a glance. The
        <strong>Delete</strong> and <strong>link</strong> actions are available at the top left of the panel.
      </p>

      <img
        src="@/assets/organizations-detail.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="Organization Detail Page"
      />

      <h2 id="linking-contacts" class="text-2xl font-semibold mt-10 mb-4">Linking Contacts to an Organization</h2>
      <p class="mb-4 leading-relaxed">
        When creating or editing a Contact, select the Organization from the Company Name dropdown. This
        links them together so you can see all company-level activity across all contacts and deals in one place inside the organization record.
      </p>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
        <p class="text-sm text-blue-800 dark:text-blue-200">
          <strong>Tip:</strong> Always link contacts and deals to an organization when possible. It gives
          managers a company-wide view of all ongoing opportunities and communication history without
          having to search through individual records.
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
