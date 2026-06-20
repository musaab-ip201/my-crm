<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Integrations</h1>

      <p class="mb-6 leading-relaxed">
        Connect IP CRM with external tools and services your team already uses. Access via <strong>Settings → Integrations</strong>. Each integration has an <strong>Enable</strong> toggle to turn it on to activate and then fill in the required credentials.
      </p>

      <!-- TELEPHONY -->
      <h2 id="telephony" class="text-2xl font-semibold mt-10 mb-4">Telephony</h2>

      <img
        src="@/assets/integrations-telephony.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Telephony Settings"
      />

      <p class="mb-4 leading-relaxed">
        The Telephony settings page lets you configure your calling provider for IP CRM. Click any provider row to open its configuration form.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Default Medium</h3>
      <p class="mb-6 leading-relaxed">
        Use the <strong>Default medium</strong> dropdown to select which calling provider is used by default for all logged-in users. Agents can override this from their own profile if multiple providers are enabled.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Twilio</h3>

      <img
        src="@/assets/integrations-twilio.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Twilio Settings"
      />

      <p class="mb-4 leading-relaxed">
        Click <strong>Twilio</strong> to open its configuration form. Fill in:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Enabled</strong> — check to activate Twilio calling in IP CRM</li>
        <li><strong>Record Calls</strong> — check to automatically record all calls made via Twilio</li>
        <li><strong>Account SID</strong> (required) — your Twilio Account SID from the Twilio Console dashboard</li>
        <li><strong>Auth Token</strong> (required) — your Twilio Auth Token from the Twilio Console dashboard. Click the eye icon to reveal</li>
        <li><strong>TwiML SID</strong> — the TwiML App SID that handles call routing logic in Twilio</li>
        <li><strong>Update</strong> (top right) — saves all Twilio settings</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Exotel</h3>

      <img
        src="@/assets/integrations-exotel.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Exotel Settings"
      />

      <p class="mb-4 leading-relaxed">
        Click <strong>Exotel</strong> to open its configuration form. Fill in:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Enabled</strong> — check to activate Exotel calling in IP CRM</li>
        <li><strong>Record Outgoing Calls</strong> — check to record all outbound calls made via Exotel</li>
        <li><strong>Account SID</strong> (required) — your Exotel Account SID</li>
        <li><strong>Webhook Verify Token</strong> (required) — token used to verify incoming webhooks from Exotel</li>
        <li><strong>Subdomain</strong> (required) — your Exotel account subdomain</li>
        <li><strong>API Key</strong> (required) — your Exotel API Key</li>
        <li><strong>API Token</strong> (required) — your Exotel API Token. Click the eye icon to reveal</li>
        <li><strong>Not Saved</strong> label — appears next to the title when there are unsaved changes. Click <strong>Update</strong> to save</li>
        <li><strong>Update</strong> (top right) — saves all Exotel settings</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Tata Teleservices</h3>

      <img
        src="@/assets/integrations-tata.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Tata Teleservices Settings"
      />

      <p class="mb-4 leading-relaxed">
        Click <strong>Tata Teleservices</strong> to open its configuration form. This is the primary telephony integration used by IP CRM for inbound and outbound calls via Smartflo. The form has three sections:
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">API Configuration</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Enabled</strong> — check to activate TATA Tele calling</li>
        <li><strong>API Endpoint</strong> (required) — the API endpoint URL for click-to-call requests, provided by Tata Teleservices</li>
        <li><strong>API Token</strong> (required) — authentication token for the Tata Teleservices API</li>
        <li><strong>Webhook Token</strong> — token used to validate incoming webhooks from Tata Teleservices</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Account Configuration</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Account ID</strong> (required) — your Tata Teleservices Account ID</li>
        <li><strong>Phone Number</strong> — the default phone number to use for outgoing calls</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Agent Configuration</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Agent Number</strong> (required) — your virtual number (agent number) from Tata Teleservices. This is the number assigned to the agent in Smartflo</li>
        <li><strong>Caller ID</strong> — the number that will appear on the recipient's phone when a call is made</li>
        <li><strong>Update</strong> (top right) — saves all TATA Tele settings</li>
      </ul>

      <!-- WHATSAPP -->
      <h2 id="whatsapp" class="text-2xl font-semibold mt-10 mb-4">WhatsApp</h2>

      <p class="mb-4 leading-relaxed">
        Connect your Interakt account to enable WhatsApp messaging directly from lead pages in IP CRM. Once enabled, agents can send and receive WhatsApp messages from inside any lead without leaving the CRM.
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Enabled</strong> — toggle on to activate WhatsApp messaging via Interakt</li>
        <li><strong>API Key</strong> (required) — your Interakt API Key from the Interakt dashboard</li>
        <li><strong>Default Country Code</strong> — set the default country code for phone numbers, e.g. +91 for India</li>
        <li><strong>Send Welcome on Lead Create</strong> — when enabled, a welcome WhatsApp message is automatically sent to a lead when they are first created in the CRM</li>
        <li><strong>Update</strong> — saves all WhatsApp settings</li>
      </ul>

      <!-- ERPNEXT -->
      <h2 id="erpnext" class="text-2xl font-semibold mt-10 mb-4">ERPNext</h2>

      <img
        src="@/assets/integrations-erpnext.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="ERPNext Settings"
      />

      <p class="mb-4 leading-relaxed">
        Link IP CRM with ERPNext to extend your sales process into accounting and invoicing. Converted deals can flow directly into ERPNext as sales orders or quotations, eliminating double data entry.
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Enabled</strong> — check to activate the ERPNext integration</li>
        <li><strong>Is ERPNext installed on a different site?</strong> — check this if your ERPNext instance runs on a separate URL from your CRM</li>
        <li><strong>Company in ERPNext Site</strong> (required) — the company name as it appears in your ERPNext instance</li>
        <li><strong>ERPNext Site URL</strong> (required) — the URL of your ERPNext instance, e.g. https://yourcompany.erpnext.com</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">ERPNext Site APIs</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>API Key</strong> (required) — the API Key from your ERPNext user account</li>
        <li><strong>API Secret</strong> (required) — the API Secret from your ERPNext user account. Click the eye icon to reveal</li>
        <li><strong>Create customer on status change</strong> — when checked, a customer record is automatically created in ERPNext when a deal status changes to the configured deal status</li>
        <li><strong>Deal Status</strong> (required) — select which deal status triggers the customer creation in ERPNext, e.g. "Won"</li>
        <li><strong>Update</strong> (top right) — saves all ERPNext settings</li>
      </ul>

      <!-- HELPDESK -->
      <h2 id="helpdesk" class="text-2xl font-semibold mt-10 mb-4">Helpdesk</h2>

      <img
        src="@/assets/integrations-helpdesk.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Helpdesk Settings"
      />

      <p class="mb-4 leading-relaxed">
        Connect with Frappe Helpdesk to link customer support tickets to IP CRM contacts and deals. This gives your sales team visibility into open support issues before they call a customer.
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Enabled</strong> — check to activate the Helpdesk integration</li>
        <li><strong>Is Helpdesk installed on a different site?</strong> — check this if your Helpdesk instance runs on a separate URL from your CRM</li>
        <li><strong>Helpdesk Site URL</strong> (required) — the URL of your Frappe Helpdesk instance</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Helpdesk Site APIs</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>API Key</strong> (required) — the API Key from your Helpdesk user account</li>
        <li><strong>API Secret</strong> (required) — the API Secret from your Helpdesk user account. Click the eye icon to reveal</li>
        <li><strong>Update</strong> (top right) — saves all Helpdesk settings</li>
      </ul>

      <!-- LEAD SYNCING -->
      <h2 id="lead-syncing" class="text-2xl font-semibold mt-10 mb-4">Lead Syncing</h2>

      <p class="mb-4 leading-relaxed">
        Configure automatic lead syncing from external sources such as web forms, landing pages, or third-party lead generation platforms. The Lead Sources page lets you add, edit, and manage all sync sources. Synced leads are automatically assigned based on your assignment rules.
      </p>

      <img
        src="@/assets/integrations-leadsync-new.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="New Lead Sync Source"
      />

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">New Lead Sync Source Form</h3>
      <p class="mb-4 leading-relaxed">
        Click <strong>+ New Lead Sync Source</strong> to add a new source. Fill in the Details tab:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Enabled</strong> toggle (top right) — turn on to activate this sync source immediately after creating it</li>
        <li><strong>Source Type</strong> (required) — select the type of external source from the dropdown, e.g. web form, API, or third-party platform</li>
        <li><strong>Source Name</strong> (required) — a descriptive name for this source, e.g. "Facebook Ads Leads" or "Website Contact Form"</li>
        <li><strong>Background Sync Frequency</strong> (required) — how often the system checks for new leads from this source. Default is <strong>Hourly</strong></li>
        <li><strong>Access Token</strong> (required) — the authentication token provided by the external source to authorize IP CRM to pull leads</li>
        </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How Lead Syncing Works</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>IP CRM checks the external source at the configured frequency, e.g. every hour</li>
        <li>New leads found are automatically created in the IP CRM</li>
        <li>Assignment Rules are applied immediately to assign the lead to the right agent or team</li>
        <li>The lead appears in the Leads list with the source name tagged</li>
        <li>If a lead with the same phone or email already exists, it is updated rather than duplicated</li>
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
