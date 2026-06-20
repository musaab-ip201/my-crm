<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">

      <h1 class="text-3xl font-bold mb-6">Notifications</h1>

      <p class="mb-6 leading-relaxed">
        Stay informed about important activities within your CRM system using the Notifications feature.
        This page serves as a central hub for all your IP CRM-related alerts and updates.
      </p>

      <img
        src="@/assets/notification.png"
        alt="Notifications Panel"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
      />

      <h2 id="accessing-notifications" class="text-2xl font-semibold mt-10 mb-4">Accessing Notifications</h2>
      <ul class="list-disc ml-6 mb-8 space-y-2 marker:text-pink-500">
        <li>Locate the <strong>Notifications</strong> option in the sidebar.</li>
        <li>Click to open the <strong>Notifications Panel</strong>.</li>
      </ul>

      <h2 id="understanding-notifications" class="text-2xl font-semibold mt-10 mb-4">Understanding Notifications</h2>
      <p class="mb-4 leading-relaxed">
        The Notifications Panel displays a list of alerts related to your CRM activities.
        These alerts currently include:
      </p>
      <ul class="list-disc ml-6 mb-8 space-y-2 marker:text-pink-500">
        <li>Mentions in comments</li>
        <li>Task assignments / unassignment (changing assigned user)</li>
        <li>Lead / Deal assignments / unassignment</li>
      </ul>

      <h2 id="managing-notifications" class="text-2xl font-semibold mt-10 mb-4">Managing Notifications</h2>
      <p class="mb-4 leading-relaxed">
        Within the Notifications Panel, you can perform the following actions:
      </p>
      <ul class="list-disc ml-6 mb-8 space-y-2 marker:text-pink-500">
        <li>
          <strong>Open a Notification:</strong> Click on an individual notification to view the specific
          comment or activity it refers to. This action will also mark the notification as read.
        </li>
        <li>
          <strong>Mark All as Read:</strong> Click the dedicated button at the top of the panel to mark
          all your current notifications as read.
        </li>
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
  const headings = document.querySelectorAll('.help-content h2, .help-content h3')
  toc.value = Array.from(headings).map((h) => ({ id: h.id, text: h.innerText }))
})
</script>

<style>
html { scroll-behavior: smooth; }
</style>
