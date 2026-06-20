<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">

      <h1 class="text-3xl font-bold mb-6">Custom Script</h1>

      <p class="mb-4 leading-relaxed">
        In IP Frappe CRM, you can automate lead creation using the <strong>Server Script</strong> feature.
        The Server Script DocType allows you to write server-side Python code without creating a custom app
        or deploying anything.
      </p>

      <p class="mb-4 leading-relaxed">There are four types of Server Scripts, but for this guide we'll focus on:</p>
      <ul class="list-disc ml-6 mb-8 space-y-2 marker:text-pink-500">
        <li>DocType Event</li>
        <li>API</li>
        <li>Scheduler Event</li>
      </ul>

      <!-- Section 1 -->
      <h2 id="doctype-event" class="text-2xl font-semibold mt-10 mb-4">
        1. Create Lead When an Email is Received (DocType Event)
      </h2>
      <p class="mb-4 leading-relaxed">
        Let's say you want to create a Lead whenever an incoming email is received.
      </p>

      <h3 id="doctype-event-step1" class="text-xl font-semibold mt-6 mb-3">Step 1: Go to Server Script</h3>
      <p class="mb-4 leading-relaxed">
        Navigate to: <strong>Desk → Search "Server Script" → Add Server Script</strong>
      </p>
      <img
        src="@/assets/server-script-list.png"
        alt="Server Script list view showing existing scripts"
        class="rounded-lg border border-gray-200 dark:border-gray-700 mb-6 w-full"
      />

      <h3 id="doctype-event-step2" class="text-xl font-semibold mt-6 mb-3">Step 2: Fill in the following</h3>
      <img
        src="@/assets/server-script-new.png"
        alt="New Server Script form with DocType Event selected"
        class="rounded-lg border border-gray-200 dark:border-gray-700 mb-8 w-full"
      />

      <!-- Section 2 -->
      <h2 id="api-script" class="text-2xl font-semibold mt-10 mb-4">
        2. Create Lead via Custom API (API Script)
      </h2>
      <p class="mb-4 leading-relaxed">
        Sometimes you want to allow external systems to create leads by calling an API endpoint.
      </p>

      <h3 id="api-step1" class="text-xl font-semibold mt-6 mb-3">Step 1: Go to Server Script</h3>
      <p class="mb-4 leading-relaxed">
        Navigate to: <strong>Desk → Search "Server Script" → Add Server Script</strong>
      </p>

      <h3 id="api-step2" class="text-xl font-semibold mt-6 mb-3">Step 2: Fill in the following</h3>
      <p class="mb-8 leading-relaxed">
        Set the <strong>Script Type</strong> to <strong>API</strong>, give it a name and write your
        Python logic to create a CRM Lead document via <code class="bg-gray-100 dark:bg-gray-800 px-1 rounded text-pink-600 text-sm">frappe.get_doc()</code>.
      </p>

      <!-- Section 3 -->
      <h2 id="scheduler-event" class="text-2xl font-semibold mt-10 mb-4">
        3. Create Lead via Scheduled Job (Scheduler Event)
      </h2>
      <p class="mb-4 leading-relaxed">
        You may want to create leads periodically based on some logic — for example, leads from another
        table, or inactive users.
      </p>

      <h3 id="scheduler-step1" class="text-xl font-semibold mt-6 mb-3">Step 1: Go to Server Script</h3>
      <p class="mb-4 leading-relaxed">
        Navigate to: <strong>Desk → Search "Server Script" → Add Server Script</strong>
      </p>

      <h3 id="scheduler-step2" class="text-xl font-semibold mt-6 mb-3">Step 2: Fill in the following</h3>
      <p class="mb-8 leading-relaxed">
        Set the <strong>Script Type</strong> to <strong>Scheduler Event</strong>, choose the frequency
        (e.g., Daily), and write your Python logic to create leads on schedule.
      </p>

      <!-- Permission Query -->
      <h2 id="permission-query" class="text-2xl font-semibold mt-10 mb-4">
        Permission Query (Skipped)
      </h2>
      <p class="mb-8 leading-relaxed">
        The <strong>Permission Query</strong> type is used to control record visibility dynamically.
        It's not used for lead creation, so we're skipping it in this guide.
      </p>

      <!-- Tips -->
      <h2 id="tips" class="text-2xl font-semibold mt-10 mb-4">📌 Tips</h2>
      <ul class="list-disc ml-6 mb-8 space-y-2 marker:text-pink-500">
        <li>Always test your script in a <strong>Test Site</strong> before using it in production.</li>
        <li>Use <code class="bg-gray-100 dark:bg-gray-800 px-1 rounded text-pink-600 text-sm">ignore_permissions=True</code> cautiously.</li>
        <li>Use <code class="bg-gray-100 dark:bg-gray-800 px-1 rounded text-pink-600 text-sm">frappe.throw()</code> for input validation in API scripts.</li>
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
