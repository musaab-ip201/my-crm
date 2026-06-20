<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Setting Up</h1>

      <p class="mb-6 leading-relaxed">
        This guide will walk you through the setup process for your IP CRM after installation. You'll learn how to configure essential elements, import data, and access your IP CRM portal.
      </p>

      <h2 id="navigating" class="text-2xl font-semibold mt-10 mb-4">Navigating Your Workspace</h2>
      <p class="mb-4 leading-relaxed">
        Once you've set up your CRM, you'll land on the IP CRM workspace. This central hub provides easy access to all the essential setup tools:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>
          <strong>Master Data</strong> — manage core IP CRM elements like Leads, Deals, Organizations, and Contacts. Create and customize these masters to fit your specific sales process.
        </li>
        <li>
          <strong>SLA and Assignment Rules</strong> — define Service Level Agreements (SLAs) for timely lead and deal follow-up. Set up assignment rules to automatically assign leads and deals to the appropriate sales representatives.
        </li>
        <li>
          <strong>Dependent Meta</strong> — configure additional details related to your masters, such as Lead Statuses, Deal Statuses, and Lead Sources. These help categorize and track progress through your sales pipeline.
        </li>
      </ul>

      <h2 id="data-population" class="text-2xl font-semibold mt-10 mb-4">Data Population</h2>
      <p class="mb-4 leading-relaxed">There are two ways to populate your IP CRM with data:</p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>
          <strong>Manual Entry</strong> — manually add data for each master record directly within the system.
        </li>
        <li>
          <strong>Data Import</strong> — utilize the framework's data import feature to efficiently import data from Excel or CSV files. This saves time and ensures accuracy.
        </li>
      </ul>

      <h2 id="adding-users" class="text-2xl font-semibold mt-10 mb-4">Adding Users</h2>
      <p class="mb-4 leading-relaxed">
        Create user accounts from the <strong>User Master</strong> section. This grants access to your IP CRM to team members who will be using the system. Each user should be assigned to a Shift, Department, and Team so they can access their leads and use the auto-dialer during their shift hours.
      </p>

      <h2 id="crm-portal" class="text-2xl font-semibold mt-10 mb-4">Accessing Your CRM Portal</h2>
      <p class="mb-4 leading-relaxed">
        The <strong>IP CRM Portal Page</strong> link provides access to your agent and salesperson-facing portal. Here, agents and salespersons can work on their leads and deals, creating a seamless sales experience.
      </p>

      <h2 id="profile" class="text-2xl font-semibold mt-10 mb-4">Your Profile</h2>
      <p class="mb-4 leading-relaxed">
        Click your name or avatar at the top of the sidebar to access your profile. From here you can:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Update your display name and profile picture</li>
        <li>Change your password</li>
        <li>Set your language and timezone preferences</li>
      </ul>

      <h2 id="notifications" class="text-2xl font-semibold mt-10 mb-4">Notifications</h2>
      <p class="mb-4 leading-relaxed">
        The bell icon at the top of the sidebar shows your notifications. A red dot or badge means you have unread notifications. Click it to open the notifications panel and see updates about leads assigned to you, follow-up reminders, and system alerts.
      </p>

      <h2 id="shift" class="text-2xl font-semibold mt-10 mb-4">Your Shift Assignment</h2>
      <p class="mb-4 leading-relaxed">
        Your administrator assigns you to a <strong>Shift → Department → Team</strong>. This determines:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Which leads you can see and work on</li>
        <li>When you can use the auto-dialer (only during your active shift hours)</li>
        <li>Which team members you can see in the hierarchy</li>
      </ul>
      <p class="mb-6 leading-relaxed">
        If you are not assigned to a shift or your shift is not active, some features like the auto-dialer will be blocked. Contact your manager (Administrator) if you believe your shift assignment is incorrect.
      </p>

      <h2 id="collapse-sidebar" class="text-2xl font-semibold mt-10 mb-4">Collapsing the Sidebar</h2>
      <p class="mb-4 leading-relaxed">
        Click the <strong>Collapse</strong> button at the bottom of the sidebar to hide the labels and get more screen space. Click <strong>Expand</strong> to bring it back.
      </p>

      <h2 id="start" class="text-2xl font-semibold mt-10 mb-4">Start Your Sales Journey</h2>
      <p class="mb-6 leading-relaxed">
        With your IP CRM set up, you're now ready to manage leads, track deals, make calls, send WhatsApp messages, and collaborate with your team to achieve your sales goals.
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
