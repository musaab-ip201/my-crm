<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Settings</h1>

      <p class="mb-6 leading-relaxed">
        The Settings panel gives administrators full control over IP CRM. Access it by clicking your avatar at the top of the sidebar. This guide covers every section available to admins.
      </p>

      <img
        src="@/assets/settings-profile.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="IP CRM Settings"
      />

      <!-- PROFILE -->
      <h2 id="profile" class="text-2xl font-semibold mt-10 mb-4">Profile</h2>
      <p class="mb-4 leading-relaxed">
        Manage your personal information and preferences. Keep your profile up-to-date for better collaboration with your team.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Personal Information</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Full name and display name</li>
        <li>Email address for notifications</li>
        <li>Profile picture for easy identification</li>
        <li>Contact number for team communication</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Password Management</h3>
      <p class="mb-6 leading-relaxed">
        Click <strong>Change Password</strong> in the top right of the Profile page. Use a strong password with a mix of letters, numbers, and special characters.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Timezone & Preferences</h3>
      <p class="mb-6 leading-relaxed">
        Set your local timezone to ensure accurate timestamps for call logs, meetings, and task reminders. Also customize your interface language and date format.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Update Your Profile</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Click your avatar or name at the top of the sidebar to open Settings</li>
        <li>Navigate to <strong>Settings → Profile</strong></li>
        <li>Update your First or Last name if needed</li>
        <li>Click <strong>Edit profile photo</strong> to update your avatar</li>
        <li>Enter a new password to change it</li>
        <li>Click <strong>Update</strong> to apply all changes</li>
      </ul>

      <!-- SYSTEM CONFIGURATION -->
      <h2 id="system-configuration" class="text-2xl font-semibold mt-10 mb-4">System Configuration</h2>
      <p class="mb-4 leading-relaxed">
        Core system-level settings that control how IP CRM behaves across the entire organization.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Forecasting</h3>
      <p class="mb-6 leading-relaxed">
        Configure sales forecasting settings. Define forecast periods and targets so managers can track expected revenue against actual deal closures on the dashboard.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Currency & Exchange Rate</h3>
      <p class="mb-6 leading-relaxed">
        Set the default currency for deal values and configure exchange rates if your team works with multiple currencies. This ensures consistent reporting across all deals.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Brand Settings</h3>
      <p class="mb-6 leading-relaxed">
        Customize the CRM with your company logo and brand colors. Changes here reflect across the entire interface for all users.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Calendar</h3>
      <p class="mb-6 leading-relaxed">
        Configure working days, holidays, and default event durations. This affects task due dates and shift scheduling across the system.
      </p>

      <!-- USER MANAGEMENT -->
      <h2 id="user-management" class="text-2xl font-semibold mt-10 mb-4">User Management</h2>
      <p class="mb-4 leading-relaxed">
        Manage who has access to IP CRM and what they can do.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Users</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>View and manage all active users and their roles</li>
        <li>Assign users to a Shift, Department, and Team</li>
        <li>Enable or disable user accounts</li>
        <li>Change user roles — Agent, Team Leader, Manager, Admin</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Invite User</h3>
      <p class="mb-6 leading-relaxed">
        Send an email invitation to a new team member. They receive a link to set up their account and password. Once they log in, assign them to their Shift, Department, and Team so they can start working on leads.
      </p>

      <!-- EMAIL SETTINGS -->
      <h2 id="email-settings" class="text-2xl font-semibold mt-10 mb-4">Email Settings</h2>
      <p class="mb-4 leading-relaxed">
        Configure how IP CRM sends and receives emails on behalf of your team.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Email Accounts</h3>
      <p class="mb-6 leading-relaxed">
        Connect your company email accounts — Gmail, Outlook, or custom SMTP. Emails sent from leads and deals will use these accounts. You can set a default outgoing email account for the whole team.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Email Templates</h3>
      <p class="mb-6 leading-relaxed">
        Create reusable email templates for common messages like follow-ups, introductions, or proposals. Templates support variables that auto-fill with the lead's name and your name when used. Agents can pick a template when composing an email from inside a lead or deal.
      </p>

      <!-- AUTOMATION & RULES -->
      <h2 id="automation" class="text-2xl font-semibold mt-10 mb-4">Automation & Rules</h2>
      <p class="mb-4 leading-relaxed">
        Automate repetitive tasks and enforce consistent processes across your sales team.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Assignment Rules</h3>
      <p class="mb-6 leading-relaxed">
        Define rules to automatically assign incoming leads to the right agent or team. Rules can be based on lead source, location, product interest, or round-robin distribution. This ensures no lead goes unattended.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">SLA Policies</h3>
      <p class="mb-6 leading-relaxed">
        Set Service Level Agreement policies to define how quickly leads must be contacted after creation. If an agent does not respond within the defined time, the system flags the lead — keeping your team accountable and response times fast.
      </p>

      <!-- CUSTOMIZATION -->
      <h2 id="customization" class="text-2xl font-semibold mt-10 mb-4">Customization</h2>
      <p class="mb-4 leading-relaxed">
        Tailor IP CRM to match your team's exact workflow.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Home Actions</h3>
      <p class="mb-6 leading-relaxed">
        Configure the quick action buttons that appear on the dashboard home screen. Add shortcuts to the most common actions your team performs daily such as creating a new lead or starting the auto-dialer.
      </p>

      <!-- INTEGRATIONS -->
      <h2 id="integrations" class="text-2xl font-semibold mt-10 mb-4">Integrations</h2>
      <p class="mb-4 leading-relaxed">
        Connect IP CRM with external tools and services your team already uses.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Telephony</h3>
      <p class="mb-4 leading-relaxed">Configure your calling provider. IP CRM supports:</p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>TATA Tele (Smartflo)</strong> — primary integration for inbound and outbound calls with auto call logging</li>
        <li><strong>Twilio</strong> — make and receive calls with recording support</li>
        <li><strong>Exotel</strong> — mobile-based calling for agents</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">WhatsApp</h3>
      <p class="mb-6 leading-relaxed">
        Connect your Interakt account to enable WhatsApp messaging directly from lead pages. Enter your Interakt API key, set the default country code (+91), and optionally enable automatic welcome messages when a new lead is created.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">ERPNext</h3>
      <p class="mb-6 leading-relaxed">
        Link IP CRM with ERPNext to extend your sales process into accounting and invoicing. Converted deals can flow directly into ERPNext as sales orders or quotations.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Helpdesk</h3>
      <p class="mb-6 leading-relaxed">
        Connect with Frappe Helpdesk to link customer support tickets to CRM contacts and deals. This gives your sales team visibility into open support issues before they call a customer.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Lead Syncing</h3>
      <p class="mb-6 leading-relaxed">
        Configure automatic lead syncing from external sources such as web forms, landing pages, or third-party lead generation platforms. Synced leads are automatically assigned based on your assignment rules.
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
  const headings = document.querySelectorAll('.help-content h2')
  toc.value = Array.from(headings).map((h) => ({ id: h.id, text: h.innerText }))
})
</script>
<style>html { scroll-behavior: smooth; }</style>
