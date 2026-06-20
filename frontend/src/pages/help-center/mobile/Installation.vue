<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">

      <h1 class="text-3xl font-bold mb-6">Mobile Installation</h1>

      <p class="mb-6 leading-relaxed">
        IP CRM offers a mobile-friendly interface through a Progressive Web App (PWA). This means you
        can access all the CRM functionalities directly on your phone.
      </p>

      <img
        src="@/assets/installation.png"
        alt="IP CRM Mobile Installation"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
      />

      <h2 id="supported-devices-and-browsers" class="text-2xl font-semibold mt-10 mb-4">
        Supported Devices and Browsers
      </h2>
      <p class="mb-4 leading-relaxed">
        The IP CRM PWA works on most modern smartphones and tablets. Here's a quick note about
        browser compatibility:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Android:</strong> Chrome is recommended for the best experience.</li>
        <li><strong>iOS:</strong> Safari is recommended.</li>
      </ul>

      <div class="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 rounded p-4 mb-8 text-sm leading-relaxed">
        <strong>Note:</strong> Firefox currently doesn't support PWA installation without additional plugins.
      </div>

      <h2 id="how-to-install" class="text-2xl font-semibold mt-10 mb-4">How to Install</h2>

      <h3 id="devices" class="text-xl font-semibold mt-6 mb-3">Devices</h3>

      <h3 id="android" class="text-xl font-semibold mt-6 mb-3">Android</h3>
      <ul class="list-disc ml-6 mb-8 space-y-2 marker:text-pink-500">
        <li>Open IP CRM in <strong>Chrome</strong>.</li>
        <li>Tap the three-dot menu in the top right corner.</li>
        <li>Select <strong>Add to Home Screen</strong>.</li>
        <li>Confirm by tapping <strong>Add</strong>.</li>
        <li>IP CRM will now appear as an app icon on your home screen.</li>
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
