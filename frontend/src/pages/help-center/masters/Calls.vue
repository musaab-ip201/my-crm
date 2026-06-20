<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Call Logs</h1>

      <p class="mb-6 leading-relaxed">
        Every call made or received through IP CRM is automatically recorded as a Call Log. View all
        call history from <strong>Call Logs</strong> in the sidebar, or inside any lead or deal under
        the Activity tab.
      </p>

      <h2 id="viewing-calls" class="text-2xl font-semibold mt-10 mb-4">Viewing Call Logs</h2>
      <p class="mb-4 leading-relaxed">
        Click <strong>Call Logs</strong> in the sidebar. The list shows every call with the following
        columns: <strong>Caller</strong>, <strong>Receiver</strong>, <strong>Type</strong>,
        <strong>Status</strong>, <strong>Duration</strong>, <strong>From (number)</strong>,
        <strong>To (number)</strong>, and <strong>Created On</strong>. You can filter by
        Telephony Medium and Type at the top, and use <strong>Filter</strong>, <strong>Sort</strong>,
        and <strong>Columns</strong> to customize the view.
      </p>

      <img
        src="@/assets/calllogs-list.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="Call Logs List"
      />

      <h2 id="new-call-log" class="text-2xl font-semibold mt-10 mb-4">Creating a Call Log Manually</h2>
      <p class="mb-4 leading-relaxed">
        Click <strong>+ Create</strong> at the top right to manually log a call. The New Call Log form
        includes:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Type</strong> — Incoming or Outgoing</li>
        <li><strong>To</strong> — the number or contact called</li>
        <li><strong>From</strong> — the number the call was made from</li>
        <li><strong>Status</strong> — Completed, Missed, No Answer, Busy, etc.</li>
        <li><strong>Duration</strong> — call duration in seconds</li>
      </ul>
      <p class="mb-6 leading-relaxed">
        The field layout can be customized using the <strong>Edit fields layout</strong> option. Click
        <strong>Create</strong> to save the log.
      </p>

      <h2 id="call-details" class="text-2xl font-semibold mt-10 mb-4">Call Details</h2>
      <p class="mb-4 leading-relaxed">
        Click any call log to open its <strong>Call Details</strong> panel. It shows:
      </p>
      <ul class="list-disc ml-6 mb-4 space-y-2 marker:text-pink-500">
        <li>Call type — Incoming or Outgoing</li>
        <li>Caller and receiver with their names</li>
        <li>Date and time of the call</li>
        <li>Duration of the call</li>
        <li>Current status — Ringing, Completed, Missed, etc.</li>
      </ul>
      <p class="mb-4 leading-relaxed">
        From the <strong>...</strong> menu inside Call Details you can quickly <strong>Add note</strong>
        or <strong>Add task</strong> linked to this call. If the caller is not yet in the system, a
        <strong>Create lead</strong> button appears at the bottom to convert the unknown caller into a
        new lead instantly.
      </p>

      <img
        src="@/assets/calllogs-detail.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="Call Details"
      />

      <h2 id="inbound-calls" class="text-2xl font-semibold mt-10 mb-4">Inbound Calls (Customers Calling You)</h2>
      <p class="mb-4 leading-relaxed">
        When a customer calls your company number via TATA Tele (Smartflo), the system automatically:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Creates a call log with the customer number</li>
        <li>Links the call to the matching Lead, Deal, or Contact by phone number</li>
        <li>Updates call status in real time — Ringing, In Progress, Completed</li>
        <li>Saves the recording URL once the call ends</li>
      </ul>
      <p class="mb-6 leading-relaxed">
        The call appears in the Activity tab of the linked lead or deal automatically — no manual
        action needed.
      </p>

      <h2 id="outbound-calls" class="text-2xl font-semibold mt-10 mb-4">Outbound Calls (You Calling a Lead)</h2>
      <p class="mb-4 leading-relaxed">
        Open a lead and click the phone icon next to their mobile number. A call popup appears showing:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Call status — Calling, In Progress, Ended</li>
        <li>Live call duration timer</li>
        <li>Option to add notes during the call</li>
        <li>Option to add a task during the call</li>
        <li>Minimize button to keep working while on the call</li>
      </ul>
      <p class="mb-6 leading-relaxed">
        Once the call ends, the log is saved automatically and appears in the lead Activity timeline.
      </p>

      <h2 id="call-statuses" class="text-2xl font-semibold mt-10 mb-4">Call Statuses Explained</h2>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Initiated</strong> — call request sent</li>
        <li><strong>Ringing</strong> — phone is ringing on the other end</li>
        <li><strong>In Progress</strong> — call is connected and active</li>
        <li><strong>Completed</strong> — call ended normally</li>
        <li><strong>No Answer</strong> — the other party did not pick up</li>
        <li><strong>Busy</strong> — the line was busy</li>
        <li><strong>Failed</strong> — call could not connect</li>
        <li><strong>Cancelled</strong> — call was cancelled before connecting</li>
      </ul>

      <h2 id="call-insights" class="text-2xl font-semibold mt-10 mb-4">Call Insights on Dashboard</h2>
      <p class="mb-4 leading-relaxed">
        The Dashboard has a <strong>Call Insights</strong> card showing total calls, incoming vs
        outgoing counts, status breakdown, and total talk time. Click any status box to jump to the
        filtered call log list.
      </p>

      <h2 id="recordings" class="text-2xl font-semibold mt-10 mb-4">Call Recordings</h2>
      <p class="mb-4 leading-relaxed">
        If your telephony setup supports recordings, a play button appears in the call log. Click it
        to listen directly in the browser. Recordings are stored by TATA Tele and linked automatically.
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
  const headings = document.querySelectorAll('.help-content h2,.help-content h3')
  toc.value = Array.from(headings).map((h) => ({ id: h.id, text: h.innerText }))
})
</script>

<style>
html { scroll-behavior: smooth; }
</style>
