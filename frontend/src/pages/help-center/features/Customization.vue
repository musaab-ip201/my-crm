<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">

      <h1 class="text-3xl font-bold mb-6">Customization</h1>

      <p class="mb-4 leading-relaxed">
        IP Frappe CRM provides several customization options that allow businesses to adapt the system
        to their specific workflows and data requirements. These features help teams capture additional
        information, automate actions, and modify the interface to better match their sales processes.
      </p>

      <p class="mb-4 leading-relaxed">Common customization options in Frappe CRM include:</p>
      <ul class="list-disc ml-6 mb-8 space-y-2 marker:text-pink-500">
        <li>Custom Fields</li>
        <li>Custom Actions</li>
        <li>Custom Statuses</li>
        <li>Custom List Actions</li>
        <li>Quick Entry Layout Builder</li>
      </ul>

      <!-- Custom Fields -->
      <h2 id="custom-fields" class="text-2xl font-semibold mt-10 mb-4">1. Custom Fields</h2>
      <p class="mb-4 leading-relaxed">
        Custom Fields allow you to capture additional information that is not included in the default
        Lead or Deal forms. For example, you may want to store details such as Lead Source Category,
        Customer Priority, or Product Interest that are specific to your business.
      </p>

      <img
        src="@/assets/custom-field.png"
        alt="Custom Fields Layout Builder"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
      />

      <h3 id="adding-custom-fields" class="text-xl font-semibold mt-6 mb-3">Adding Custom Fields</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Navigate to a Lead or Deal page on IP CRM.</li>
        <li>Click the edit icon on the first section header in the side panel.</li>
        <li>The <strong>Fields Layout Builder</strong> will open.</li>
        <li>Use the layout builder to:
          <ul class="list-disc ml-6 mt-2 space-y-1 marker:text-pink-300">
            <li>Add new fields or sections.</li>
            <li>Drag and drop fields to rearrange them.</li>
          </ul>
        </li>
        <li>(Optional) Click <strong>Show Preview</strong> to review the layout.</li>
        <li>Save the changes.</li>
      </ul>

      <h3 id="custom-fields-notes" class="text-xl font-semibold mt-6 mb-3">Important Notes</h3>
      <ul class="list-disc ml-6 mb-10 space-y-2 marker:text-pink-500">
        <li>Section labels can be edited, but field labels cannot be changed from the layout builder.</li>
        <li>Some sections (such as Contacts in Deals) cannot be removed.</li>
        <li>Certain field types may appear as basic data fields in the current UI.</li>
      </ul>

      <!-- Custom Actions -->
      <h2 id="custom-actions" class="text-2xl font-semibold mt-10 mb-4">2. Custom Actions</h2>
      <p class="mb-4 leading-relaxed">
        Custom Actions allow you to add buttons or actions directly on Lead or Deal pages to perform
        specific tasks. These actions can automate workflows such as creating documents, updating
        statuses, or integrating with other systems. Custom actions are created using
        <strong>Form Scripts</strong> in IP Desk.
      </p>

      <img
        src="@/assets/custom-action.png"
        alt="Custom Actions on CRM Form Script configuration page"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
      />

      <h3 id="creating-custom-actions" class="text-xl font-semibold mt-6 mb-3">Creating Custom Actions</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Navigate to <strong>IP Desk →</strong> Search for<strong> CRM Form Script List → </strong> Click on <strong> + Add CRM Form Scripte </strong> button.</li>
        <li>Fill in the form:
    <ul class="list-disc ml-6 mt-2 space-y-1 marker:text-pink-300">
      <li><strong>Name:</strong> Enter a descriptive name for your action (e.g., "Send Email Action").</li>
      <li><strong>DocType:</strong> Select <strong>CRM Lead</strong> or <strong>CRM Deal</strong>.</li>
      <li><strong>Apply To:</strong> Select <strong>Form</strong> from the dropdown.</li>
    </ul>
  </li>
  <li>In the <strong>Script</strong> editor, write JavaScript code to define your custom action.</li>
  <li>Click <strong>Save</strong> to apply the changes.</li>
  <li>The custom action will now appear on the Lead or Deal form page.</li>
</ul>

<p class="mb-10 leading-relaxed">
  Custom actions can be implemented as single buttons, grouped actions in a menu, or dropdown actions.
  These actions can interact with the current record, call APIs, update fields, or navigate to other pages.
</p>
      <p class="mb-4 leading-relaxed">Custom actions can be implemented in different ways:</p>
      <ul class="list-disc ml-6 mb-10 space-y-2 marker:text-pink-500">
        <li><strong>Single Button</strong> – Adds one action button to the page.</li>
        <li><strong>Grouped Actions</strong> – Multiple actions inside a menu.</li>
        <li><strong>Dropdown Actions</strong> – Actions grouped under a labeled button.</li>
      </ul>

      <!-- Custom Statuses -->
      <h2 id="custom-statuses" class="text-2xl font-semibold mt-10 mb-4">3. Custom Statuses</h2>
      <p class="mb-4 leading-relaxed">
        Custom Statuses allow you to define your own workflow stages for Leads or Deals. This helps
        organizations reflect their actual sales pipeline instead of relying only on default status options.
      </p>

      <img
        src="@/assets/custom-status.png"
        alt="Custom Statuses configuration"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
      />

      <h3 id="adding-custom-statuses" class="text-xl font-semibold mt-6 mb-3">Adding Custom Statuses</h3>
      <ul class="list-disc ml-6 mb-10 space-y-2 marker:text-pink-500">
        <li>Navigate to <strong>IP Desk → </strong> Search for <strong> CRM Deal Status List →</strong> Click on <strong> + Add CRM Deal Status </strong> </li>
         <li><strong>Status:</strong> Enter the name of your custom status (e.g., "Negotiation", "Pending Approval").</li>
      <li><strong>Type:</strong> Select the status type from the dropdown (e.g., "Open", "Closed").</li>
      <li><strong>Color:</strong> Choose a color to visually identify this status.</li>
      <li><strong>Probability:</strong> (Optional) Set the probability percentage for deal forecasting.</li>
      <li><strong>Position:</strong> Set the order in which this status appears in the dropdown.</li>
  <li>Click <strong>Save</strong>.</li></ul>

<p class="mb-10 leading-relaxed">
  Once saved, the new status will appear in the status dropdown on Lead or Deal forms, allowing
  your team to track records through your custom workflow stages.
</p>

      <!-- Custom List Actions -->
      <h2 id="custom-list-actions" class="text-2xl font-semibold mt-10 mb-4">4. Custom List Actions</h2>
      <p class="mb-4 leading-relaxed">
        Custom List Actions allow you to perform tasks directly from the list view without opening
        individual records. These actions help automate repetitive operations on multiple records.
      </p>

      <img
        src="@/assets/custom-list-action.png"
        alt="Custom List Actions in list view"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
      />

      <h3 id="types-of-list-actions" class="text-xl font-semibold mt-6 mb-3">Types of List Actions</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>
          <strong>Actions</strong> – Appear as buttons in the list view header. Perform actions such
          as deleting records or triggering workflows.
        </li>
        <li>
          <strong>Bulk Actions</strong> – Work on multiple selected rows in the list view. Useful for
          updating statuses, sending notifications, or performing batch operations.
        </li>
      </ul>

      <h3 id="adding-list-actions" class="text-xl font-semibold mt-6 mb-3">Adding Custom List Actions</h3>
      <ul class="list-disc ml-6 mb-10 space-y-2 marker:text-pink-500">
        <li>Navigate to <strong>IP Desk →</strong> Search for<strong> CRM Form Script List → </strong> Click on <strong> + Add CRM Form Scripte </strong> button.</li>
       <li>Search for <strong>CRM Form Script</strong> in the search bar.</li>
  <li>Click <strong>Add CRM Form Script</strong>.</li>
  <li>Fill in the form:
    <ul class="list-disc ml-6 mt-2 space-y-1 marker:text-pink-300">
      <li><strong>Name:</strong> Enter a name for your list action (e.g., "Bulk Assign to Team").</li>
      <li><strong>DocType:</strong> Select <strong>CRM Lead</strong> or <strong>CRM Deal</strong>.</li>
      <li><strong>Apply To:</strong> Select <strong>List</strong> from the dropdown.</li>
     </ul>
        </li>
         <li>In the <strong>Script</strong> editor, define your actions using JavaScript:
    <ul class="list-disc ml-6 mt-2 space-y-1 marker:text-pink-300">
      <li>Use <code class="bg-gray-100 dark:bg-gray-800 px-1 rounded text-pink-600 text-sm">actions</code> array for header buttons.</li>
      <li>Use <code class="bg-gray-100 dark:bg-gray-800 px-1 rounded text-pink-600 text-sm">bulk_actions</code> array for operations on selected records.</li>
    </ul>
  </li>
  <li>Click <strong>Save</strong>.</li>
  <li>The actions will now appear in the <strong>Actions</strong> dropdown in the list view.</li>
 </ul>

<p class="mb-10 leading-relaxed">
  These actions can interact with list data, call Frappe APIs, and perform operations on single
  or multiple records at once.
</p>
      <!-- Quick Entry Layout Builder -->
      <h2 id="quick-entry-layout-builder" class="text-2xl font-semibold mt-10 mb-4">5. Quick Entry Layout Builder</h2>
      <p class="mb-4 leading-relaxed">
        The Quick Entry Layout Builder allows you to customize the layout of quick entry forms used
        when creating new Leads or Deals. This helps you control which fields appear when users create
        records quickly.
      </p>

      <img
        src="@/assets/leads-quick-entry-layout.png"
        alt="Quick Entry Layout Builder"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
      />

      <h3 id="customizing-quick-entry" class="text-xl font-semibold mt-6 mb-3">Customizing Quick Entry Forms</h3>
      <ul class="list-disc ml-6 mb-10 space-y-2 marker:text-pink-500">
        <li>Navigate to Lead or Deal List View in IP CRM .</li>
        <li>Click <strong>Create</strong> to open the quick entry form.</li>
        <li>Click the edit icon.</li>
        <li>The <strong>Quick Entry Layout Builder</strong> will open.</li>
        <li>Use the builder to:
          <ul class="list-disc ml-6 mt-2 space-y-1 marker:text-pink-300">
            <li>Add new sections.</li>
            <li>Add or rearrange fields.</li>
            <li>Drag and drop fields between sections.</li>
          </ul>
        </li>
        <li>Use <strong>Show Preview</strong> to review the layout.</li>
        <li>Save the changes.</li>
      </ul>

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
  const headings = document.querySelectorAll('.help-content h2')
  toc.value = Array.from(headings).map((h) => ({ id: h.id, text: h.innerText }))
})
</script>

<style>
html { scroll-behavior: smooth; }
</style>
