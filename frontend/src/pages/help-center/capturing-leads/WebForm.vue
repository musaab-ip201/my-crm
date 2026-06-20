<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">

      <h1 class="text-3xl font-bold mb-6">Web Forms</h1>

      <p class="mb-6 leading-relaxed">
        Web Forms in IP Frappe CRM let you collect leads directly from your website
        without writing a single line of code. Follow these simple steps to create one:
      </p>

      <h2 id="switch-to-desk" class="text-2xl font-semibold mt-10 mb-4">
        Step 1: Switch to Desk
      </h2>
      <p class="mb-4 leading-relaxed">
        Switch to the desk view by clicking the profile button in the top left corner
        and selecting <strong>Apps > Desk</strong> on IP CRM.
      </p>

      <h2 id="create-web-form" class="text-2xl font-semibold mt-10 mb-4">
        Step 2: Create Web Form
      </h2>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Search for <strong>Web Form List</strong> in the search bar.</li>
        <li>Click on the <strong>"Add Web Form"</strong> button.</li>
        <li>Fill in the basic details:
          <ul class="list-disc ml-6 mt-2 space-y-1 marker:text-pink-300">
            <li><strong>Title:</strong> Give your form a meaningful title (like "Lead Capture Form").</li>
            <li><strong>Route:</strong> Set the URL path for the form (e.g., <code class="bg-gray-100 dark:bg-gray-800 px-1 rounded text-pink-600 text-sm">/lead-capture</code>).</li>
            <li><strong>DocType:</strong> Select <strong>CRM Lead</strong> as the DocType since you're capturing leads.</li>
          </ul>
        </li>
      </ul>

      <img
        src="@/assets/webform.png"
        alt="Web Form creation in Frappe Desk showing Title, Route, DocType fields and Web Form Fields table"
        class="rounded-lg border border-gray-200 dark:border-gray-700 mb-8 w-full"
      />

      <h2 id="customize-fields" class="text-2xl font-semibold mt-10 mb-4">
        Step 3: Customize Form Fields
      </h2>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Click on <strong>Get Fields</strong> to automatically fetch the fields from the CRM Lead DocType.</li>
        <li>You can also manually add more fields if needed or customize the existing ones.</li>
        <li>Adjust labels, set mandatory fields, and add default values as required.</li>
      </ul>

      <h2 id="publish" class="text-2xl font-semibold mt-10 mb-4">
        Step 4: Publish &amp; Access
      </h2>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Make your Web Form live by clicking the <strong>"Publish"</strong> button.</li>
        <li>The URL will be available in the sidebar. Click <strong>"See on Website"</strong> to access your Web Form.</li>
      </ul>
      <p class="mb-6 leading-relaxed">
        That's it! You've now got a live Web Form capturing leads directly into Frappe CRM.
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
