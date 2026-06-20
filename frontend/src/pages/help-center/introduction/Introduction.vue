<template>
  <div class="flex">
  <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">

      <h1 class="text-3xl font-bold mb-6">Welcome to IP CRM</h1>

      <p class="mb-6 leading-relaxed">
        IP CRM is your team's central hub for managing leads, tracking deals, communicating with customers, and staying on top of follow-ups, all in one place. Whether you're a sales agent making calls or a manager reviewing team performance, this guide will walk you through everything you need to know.
      </p>

      <h2 id="what-is-ip-crm" class="text-2xl font-semibold mt-10 mb-4">What is IP CRM?</h2>
      <p class="mb-4 leading-relaxed">
        IP CRM is a customized Customer Relationship Management system built for internal sales teams at IPShopy. It helps you:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Capture and manage leads from multiple sources</li>
        <li>Track deals through your sales pipeline</li>
        <li>Make and receive calls directly from the IP CRM.</li>
        <li>Send WhatsApp messages to leads</li>
        <li>Set follow-up reminders and never miss a callback</li>
        <li>View your team's performance on the dashboard</li>
        <li>Work within your assigned shift, department, and team structure.</li>
      </ul>

      <h2 id="who-uses-it" class="text-2xl font-semibold mt-10 mb-4">Who Uses IP CRM?</h2>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Sales Agents</strong> — to manage their assigned leads, make calls, set follow-ups.</li>
        <li><strong>Team Leaders</strong> —to monitor team members and their leads.</li>
        <li><strong>Department Heads</strong> — to oversee all teams in their department.</li>
        <li><strong>Managers / Admins</strong> —they have full access to all data, settings, and reports.</li>
      </ul>

      <h2 id="navigation" class="text-2xl font-semibold mt-10 mb-4">Navigating the CRM</h2>
      <p class="mb-4 leading-relaxed">
        The left sidebar is your main navigation. It contains:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Notifications</strong> — to get latest updates and events.</li>
        <li><strong>Dashboard</strong> — it is an overview of your leads, follow-ups, and call stats.</li>
        <li><strong>Leads</strong> — list of all potential customers.</li>
        <li><strong>Deals</strong> — active sales opportunities.</li>
        <li><strong>Contacts</strong> — individual people you interact with.</li>
        <li><strong>Organizations</strong> — companies linked to your contacts.</li>
        <li><strong>Notes</strong> — quick notes across leads and deals.</li>
        <li><strong>Tasks</strong> — to-do items linked to leads or deals.</li>
        <li><strong>Calendar</strong> — view scheduled events and tasks.</li>
        <li><strong>Call Logs</strong> — history of all inbound and outbound calls.</li>
        <li><strong>Help</strong> — this help center.</li>
      </ul>
      <p class="mb-6 leading-relaxed">
        You can collapse the sidebar by clicking the arrow at the bottom to get more screen space.
      </p>

      <h2 id="hierarchy" class="text-2xl font-semibold mt-10 mb-4">Your Shift & Team</h2>
      <p class="mb-6 leading-relaxed">
        IP CRM organizes users into a hierarchy: <strong>Shift → Department → Team → Agent</strong>. Your access to leads and the auto-dialer depends on your assigned shift being active. You can see your current shift status in the sidebar under the hierarchy menu.
      </p>

      <h2 id="getting-started" class="text-2xl font-semibold mt-10 mb-4">Getting Started</h2>
      <p class="mb-4 leading-relaxed">Use the sidebar on the left to explore each section of this Help Center. We recommend starting with:</p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Setting Up your profile</li>
        <li>Understanding Leads and how to manage them</li>
        <li>Learning about Follow-Ups to never miss a callback</li>
        <li>Exploring the Dashboard to track your performance</li>
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
<style>html { scroll-behavior: smooth; }</style>
