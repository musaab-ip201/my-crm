<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">System Configuration</h1>

      <p class="mb-6 leading-relaxed">
        System Configuration controls how IP CRM behaves across your entire organization. These settings are managed by administrators and affect all users. Access them via your avatar → <strong>Settings → System Configuration</strong>.
      </p>

      <!-- FORECASTING -->
      <h2 id="forecasting" class="text-2xl font-semibold mt-10 mb-4">Forecasting</h2>

      <img
        src="@/assets/settings-forecasting.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Forecasting Settings"
      />

      <p class="mb-4 leading-relaxed">
        Configure the forecasting feature to help predict sales performance and growth. When enabled, certain deal fields become mandatory to ensure accurate forecasting data.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Enable Forecasting</h3>
      <p class="mb-4 leading-relaxed">
        Turning this on makes <strong>Expected Closure Date</strong> and <strong>Expected Deal Value</strong> mandatory fields on every deal. This ensures your pipeline data is complete enough to generate meaningful forecasts.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Auto Update Expected Deal Value</h3>
      <p class="mb-4 leading-relaxed">
        When enabled, the Expected Deal Value on a deal is automatically updated based on the total value of products associated with that deal. This removes the need for agents to manually update deal values.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Configure Forecasting</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Go to <strong>Settings → System Configuration → Forecasting</strong></li>
        <li>Toggle <strong>Enable forecasting</strong> on to make closure date and deal value mandatory</li>
        <li>Toggle <strong>Auto update expected deal value</strong> on if your deals have associated products</li>
        <li>Click <strong>Update</strong> to save changes</li>
      </ul>

      <!-- CURRENCY & EXCHANGE RATE -->
      <h2 id="currency" class="text-2xl font-semibold mt-10 mb-4">Currency & Exchange Rate</h2>

      <img
        src="@/assets/settings-currency.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Currency and Exchange Rate Settings"
      />

      <p class="mb-4 leading-relaxed">
        Configure the currency and exchange rate provider for your CRM. This affects how all monetary values are displayed across leads, deals, and reports.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Currency</h3>
      <p class="mb-4 leading-relaxed">
        Set the default currency for all monetary values in the CRM — for example <strong>INR</strong> for Indian Rupee. Once set, this cannot be edited, so choose carefully before saving.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Exchange Rate Provider</h3>
      <p class="mb-4 leading-relaxed">
        Select the provider used to fetch live exchange rates — for example <strong>Frankfurter</strong>. This is used when your team works with deals in multiple currencies and needs automatic conversion.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Configure Currency</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Go to <strong>Settings → System Configuration → Currency & Exchange Rate</strong></li>
        <li>Select your default <strong>Currency</strong> from the dropdown — note this cannot be changed later</li>
        <li>Select your preferred <strong>Exchange Rate Provider</strong></li>
        <li>Click <strong>Update</strong> to save</li>
      </ul>

      <!-- BRAND SETTINGS -->
      <h2 id="brand-settings" class="text-2xl font-semibold mt-10 mb-4">Brand Settings</h2>

      <img
        src="@/assets/settings-brand.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Brand Settings"
      />

      <p class="mb-4 leading-relaxed">
        Customize IP CRM with your company's brand name, logo, and favicon. These changes reflect across the entire interface for all users.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Brand Name</h3>
      <p class="mb-4 leading-relaxed">
        Set the name that appears in the CRM interface — for example <strong>IP CRM</strong>. This is shown in the browser tab and various places across the UI.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Brand Logo</h3>
      <p class="mb-4 leading-relaxed">
        Upload your company logo. It appears in the left sidebar next to the CRM name. Recommended size is <strong>32x32 px</strong> in PNG or SVG format.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Favicon</h3>
      <p class="mb-4 leading-relaxed">
        Upload a favicon that appears next to the title in your browser tab. Recommended size is <strong>32x32 px</strong> in PNG or ICO format.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Update Brand Settings</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Go to <strong>Settings → System Configuration → Brand Settings</strong></li>
        <li>Enter your <strong>Brand name</strong> in the text field</li>
        <li>Click <strong>Change</strong> next to Brand logo to upload your logo image</li>
        <li>Click <strong>Change</strong> next to Favicon to upload your favicon</li>
        <li>Click <strong>Remove</strong> next to either image to revert to default</li>
        <li>Click <strong>Update</strong> to apply all changes</li>
      </ul>

      <!-- CALENDAR -->
      <h2 id="calendar" class="text-2xl font-semibold mt-10 mb-4">Calendar</h2>

      <img
        src="@/assets/settings-calendar.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Calendar Settings"
      />

      <p class="mb-4 leading-relaxed">
        Configure your calendar settings including the default view and event notifications. These settings affect how all users see and interact with the Calendar section of IP CRM.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Default View</h3>
      <p class="mb-4 leading-relaxed">
        Select the default view when users open the Calendar — options include <strong>Daily</strong>, <strong>Weekly</strong>, or <strong>Monthly</strong>. Weekly is the recommended default for most sales teams.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Event Notifications</h3>
      <p class="mb-4 leading-relaxed">
        Set reminders that are sent to users <strong>before an event starts</strong>. Click <strong>+ Add Notification</strong> to configure how many minutes or hours before the event the reminder should be sent.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">All Day Event Notifications</h3>
      <p class="mb-4 leading-relaxed">
        For all-day events, set a specific time to send the reminder. Click <strong>+ Add Notification</strong> and set the time at which users should be notified on the day of the event.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Configure Calendar Settings</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Go to <strong>Settings → System Configuration → Calendar</strong></li>
        <li>Select your preferred <strong>Default view</strong> from the dropdown</li>
        <li>Click <strong>+ Add Notification</strong> under Event notifications to add a reminder time</li>
        <li>Click <strong>+ Add Notification</strong> under All day event notifications to set a reminder time for full-day events</li>
        <li>Click <strong>Update</strong> to save all changes</li>
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
<style>html { scroll-behavior: smooth; }</style>
