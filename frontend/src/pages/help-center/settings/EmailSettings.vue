<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Email Settings</h1>

      <p class="mb-6 leading-relaxed">
        Configure how IP CRM sends and receives emails on behalf of your team. Access via <strong>Settings → Email Settings</strong>. You can connect email accounts and create reusable templates for common communications.
      </p>

      <!-- EMAIL ACCOUNTS -->
      <h2 id="email-accounts" class="text-2xl font-semibold mt-10 mb-4">Email Accounts</h2>

      <img
        src="@/assets/email-accounts.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Email Accounts"
      />

      <p class="mb-4 leading-relaxed">
        The Email Accounts page lets you manage all email accounts connected to IP CRM. You can add multiple accounts and set one as the default for sending and receiving emails. Connected accounts are used when agents send emails from inside leads and deals.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Buttons & Actions</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>+ Add Account</strong> (top right, black button) — opens the Setup Email dialog to connect a new email account</li>
        <li><strong>Default Sending and Inbox</strong> badge — shown next to the account set as the primary outgoing and incoming account for the whole team</li>
        <li>Each account shows the provider icon, account name, and email address</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Setup Email — Choose Provider</h3>
      <p class="mb-4 leading-relaxed">
        When you click <strong>+ Add Account</strong>, you are asked to choose your email service provider. IP CRM supports:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>GMail</strong> — connect your Google Workspace or personal Gmail account</li>
        <li><strong>Outlook</strong> — connect your Microsoft Outlook or Office 365 account</li>
        <li><strong>Sendgrid</strong> — transactional email service for high-volume sending</li>
        <li><strong>SparkPost</strong> — email delivery service with analytics</li>
        <li><strong>Yahoo</strong> — connect your Yahoo Mail account</li>
        <li><strong>Yandex</strong> — connect your Yandex Mail account</li>
        <li><strong>Frappe Mail</strong> — use Frappe's built-in mail service</li>
      </ul>
      <p class="mb-4 leading-relaxed">
        Select your provider and follow the on-screen steps to enter your credentials and authorize the connection.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Add an Email Account</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Go to <strong>Settings → Email Settings → Email Accounts</strong></li>
        <li>Click <strong>+ Add Account</strong></li>
        <li>Select your email provider from the list</li>
        <li>Enter your email address and credentials</li>
        <li>Set as <strong>Default Sending and Inbox</strong> if this should be the primary account</li>
        <li>Save to connect the account</li>
      </ul>

      <!-- EMAIL TEMPLATES -->
      <h2 id="email-templates" class="text-2xl font-semibold mt-10 mb-4">Email Templates</h2>

      <p class="mb-4 leading-relaxed">
        Email Templates let you create and manage reusable email messages for common CRM communications — such as follow-ups, payment reminders, meeting confirmations, or introductions. Agents can pick a template when composing an email from inside any lead or deal, saving time and keeping communication consistent.
      </p>

      <img
        src="@/assets/email-new-template.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="New Email Template"
      />

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Fields in the New Template Form</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Name</strong> (required) — the internal label for this template, visible to agents when selecting a template. Example: "Payment Reminder"</li>
        <li><strong>For</strong> — select whether this template is for a <strong>Lead</strong> or a <strong>Deal</strong>. This controls which variables are available</li>
        <li><strong>Subject</strong> (required) — the email subject line. You can use variables here, for example: Payment Reminder from IP CRM</li>
        <li><strong>Content Type</strong> — choose <strong>Rich Text</strong> for formatted emails with bold, lists, and links, or <strong>Markdown</strong> for plain text formatting</li>
        <li><strong>Content</strong> (required) — the body of the email. Use variables like lead_name to personalize the message automatically</li>
        <li><strong>Enabled</strong> toggle (top right) — turn this on to make the template available for agents to use. Disabled templates are hidden from the template picker</li>
        <li><strong>+ Create</strong> (top right, black button) — saves and creates the template</li>
        <li><strong>← back arrow</strong> (top left) — goes back to the templates list without saving</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Using Variables in Templates</h3>
      <p class="mb-4 leading-relaxed">
        Variables auto-fill with real data when the email is sent. Common variables:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>lead_name</strong> — the lead's full name</li>
        <li><strong>name</strong> — the record ID or deal name</li>
        <li><strong>email</strong> — the lead's email address</li>
        <li><strong>mobile_no</strong> — the lead's phone number</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Create an Email Template</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Go to <strong>Settings → Email Settings → Email Templates</strong></li>
        <li>Click <strong>+ Add New</strong></li>
        <li>Enter a <strong>Name</strong> for the template</li>
        <li>Select <strong>Lead</strong> or <strong>Deal</strong> in the <strong>For</strong> field</li>
        <li>Enter the <strong>Subject</strong> line — add variables if needed</li>
        <li>Select <strong>Content Type</strong> — Rich Text or Markdown</li>
        <li>Write the email <strong>Content</strong> — use variables to personalize</li>
        <li>Toggle <strong>Enabled</strong> on so agents can use it</li>
        <li>Click <strong>+ Create</strong> to save</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Use a Template When Sending Email</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Open any Lead or Deal</li>
        <li>Click the <strong>Emails</strong> tab</li>
        <li>Click <strong>New Email</strong></li>
        <li>Click <strong>Select Template</strong> and pick from your saved templates</li>
        <li>The subject and body auto-fill — edit if needed before sending</li>
        <li>Click <strong>Send</strong></li>
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
