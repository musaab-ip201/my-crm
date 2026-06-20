<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Automation & Rules</h1>

      <p class="mb-6 leading-relaxed">
        Automation & Rules help you eliminate repetitive manual work and enforce consistent processes across your sales team. Access via <strong>Settings → Automation & Rules</strong>.
      </p>

      <!-- ASSIGNMENT RULES -->
      <h2 id="assignment-rules" class="text-2xl font-semibold mt-10 mb-4">Assignment Rules</h2>

      <p class="mb-4 leading-relaxed">
        Assignment Rules automatically assign a lead or deal to the right sales user based on predefined conditions. When a new lead is created, the system checks your rules in priority order and assigns it accordingly — ensuring no lead goes unattended.
      </p>

      <img
        src="@/assets/automation-assignment-rule.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="New Assignment Rule"
      />

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Fields in the New Assignment Rule Form</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Name</strong> (required) — a descriptive name for this rule, e.g. "Assign Mumbai Leads to Team A"</li>
        <li><strong>Priority</strong> — set the priority level (Low-Medium, etc.). Rules with higher priority are checked first. If multiple rules match a lead, the highest priority rule wins</li>
        <li><strong>Description</strong> (required) — a brief explanation of what this rule does, for your team's reference</li>
        <li><strong>Apply on</strong> — select <strong>Lead</strong> or <strong>Deal</strong> to define which record type this rule applies to</li>
        <li><strong>Enabled</strong> toggle (top right) — turn on to activate the rule. Disabled rules are ignored during assignment</li>
        <li><strong>Save</strong> (top right, black button) — saves the rule</li>
        <li><strong>← back arrow</strong> (top left) — goes back to the rules list without saving</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Assignment Condition</h3>
      <p class="mb-4 leading-relaxed">
        Defines which leads are affected by this rule. Click <strong>+ Add a condition</strong> to add one or more conditions. Each condition checks a lead field against a value — for example: Lead Source = Website, or City = Mumbai. All conditions must match for the rule to apply.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Unassignment Condition</h3>
      <p class="mb-4 leading-relaxed">
        Defines when a lead should be automatically unassigned. Click <strong>+ Add a condition</strong> to set the criteria. For example, if a lead's status changes to Lost, it can be automatically unassigned from the agent.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Assignment Schedule</h3>
      <p class="mb-4 leading-relaxed">
        Choose the days of the week when this rule should be active. Toggle each day on or off:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday</li>
        <li>Only leads created on active days will be processed by this rule</li>
        <li>Useful for rules that should only apply during business days</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Assignee Rules</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Lead Routing</strong> — choose how leads are distributed among the selected assignees, for example round-robin (equal distribution) or load-based</li>
        <li><strong>Assignees</strong> — select the sales users who will receive leads from this rule. Click <strong>Add Assignee</strong> to add team members</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Create an Assignment Rule</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Go to <strong>Settings → Automation & Rules → Assignment Rules</strong></li>
        <li>Click <strong>+ New</strong></li>
        <li>Enter a <strong>Name</strong> and <strong>Description</strong></li>
        <li>Set the <strong>Priority</strong> and select <strong>Apply on</strong> — Lead or Deal</li>
        <li>Click <strong>+ Add a condition</strong> to define which leads this rule applies to</li>
        <li>Optionally add an <strong>Unassignment condition</strong></li>
        <li>Set the <strong>Assignment Schedule</strong> — active days of the week</li>
        <li>Set <strong>Lead Routing</strong> and add <strong>Assignees</strong></li>
        <li>Toggle <strong>Enabled</strong> on and click <strong>Save</strong></li>
      </ul>

      <!-- SLA POLICIES -->
      <h2 id="sla-policies" class="text-2xl font-semibold mt-10 mb-4">SLA Policies</h2>

      <p class="mb-4 leading-relaxed">
        SLA (Service Level Agreement) Policies define how quickly a lead must be responded to after it is created or updated. If an agent does not respond within the defined time, the system flags the lead — keeping your team accountable and response times fast.
      </p>

      <img
        src="@/assets/automation-sla-policy.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="New SLA Policy"
      />

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Fields in the New SLA Policy Form</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Name</strong> (required) — a descriptive name for this policy, e.g. "24 Hour Response Policy"</li>
        <li><strong>Apply on</strong> (required) — select <strong>Lead</strong> or <strong>Deal</strong></li>
        <li><strong>Rolling responses</strong> — when checked, the SLA restarts each time the customer replies (status changes to Open) and is fulfilled when marked as Replied. Useful for ongoing conversations</li>
        <li><strong>Enabled</strong> toggle (top right) — activate or deactivate this policy</li>
        <li><strong>Save</strong> (top right, black button) — saves the policy</li>
        <li><strong>← back arrow</strong> (top left) — goes back without saving</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Assignment Conditions</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Set as default SLA</strong> — check this to apply this policy to all leads that don't match any other SLA condition</li>
        <li><strong>+ Add a custom condition</strong> — add conditions to target specific leads, e.g. only leads from a certain source or with a certain priority</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Valid From</h3>
      <p class="mb-4 leading-relaxed">
        Set the date range during which this SLA policy is active:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Start date</strong> — the date from which this policy becomes active</li>
        <li><strong>End date</strong> — the date after which this policy expires. Leave blank for an ongoing policy</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Response and Follow Up</h3>
      <p class="mb-4 leading-relaxed">
        Add time targets around support milestones like first response:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Priority</strong> — set the priority level this response target applies to</li>
        <li><strong>First response time</strong> — the maximum time allowed before the first response must be sent</li>
        <li><strong>Default priority</strong> — set response time targets for Open and Replied statuses</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Work Schedule and Holidays</h3>
      <p class="mb-4 leading-relaxed">
        Define when the SLA clock runs. This ensures agents are not penalized for leads that come in outside working hours:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Select holiday list</strong> — choose a predefined holiday schedule so SLA does not count on holidays</li>
        <li><strong>Day</strong> — select which days of the week are working days (Monday through Sunday)</li>
        <li><strong>Start time / End time</strong> — set working hours for each day, e.g. 09:00 AM to 05:00 PM</li>
        <li>Only time within the defined working hours counts toward the SLA response time</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Create an SLA Policy</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Go to <strong>Settings → Automation & Rules → SLA Policies</strong></li>
        <li>Click <strong>+ New</strong></li>
        <li>Enter a <strong>Name</strong> and select <strong>Apply on</strong> — Lead or Deal</li>
        <li>Check <strong>Rolling responses</strong> if needed</li>
        <li>Add <strong>Assignment conditions</strong> or check <strong>Set as default SLA</strong></li>
        <li>Set the <strong>Valid from</strong> start and end dates</li>
        <li>Add <strong>Response and Follow Up</strong> time targets</li>
        <li>Configure <strong>Work schedule</strong> — select working days and hours</li>
        <li>Toggle <strong>Enabled</strong> on and click <strong>Save</strong></li>
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
