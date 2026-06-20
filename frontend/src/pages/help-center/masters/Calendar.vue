<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Calendar</h1>

      <p class="mb-6 leading-relaxed">
        The Calendar in IP CRM gives you a visual overview of all your scheduled tasks, follow-ups,
        and activities across leads and deals all in one place.
      </p>

      <h2 id="viewing-calendar" class="text-2xl font-semibold mt-10 mb-4">Viewing the Calendar</h2>
      <p class="mb-4 leading-relaxed">
        Click <strong>Calendar</strong> in the sidebar to open the calendar view. Use the view switcher
        at the top to choose between:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Month View</strong> — see all events for the current month</li>
        <li><strong>Week View</strong> — a detailed view of the current week with time slots</li>
        <li><strong>Day View</strong> — focus on a single day's schedule hour by hour</li>
      </ul>
      <p class="mb-6 leading-relaxed">
        You can also filter events by agent using the <strong>Administrator</strong> dropdown at the top,
        making it easy for managers to check any team member's schedule.
      </p>

      <img
        src="@/assets/calendar-view.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="Calendar View"
      />

      <h2 id="creating-event" class="text-2xl font-semibold mt-10 mb-4">Creating a New Event</h2>
      <p class="mb-4 leading-relaxed">
        Click <strong>+ Create</strong> at the top right or click directly on a time slot in the calendar
        to open the <strong>New Event</strong> panel. Fill in the following:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Event title</strong> — name of the event</li>
        <li><strong>Color</strong> — pick a color dot to visually categorize the event on the calendar</li>
        <li><strong>All day</strong> — toggle on if the event spans the full day with no specific time</li>
        <li><strong>Date</strong> — the scheduled date (e.g. Apr 1, 2026)</li>
        <li><strong>Start time and End time</strong> — the time range for the event</li>
        <li><strong>Add notification</strong> — set a reminder before the event</li>
        <li><strong>Add attendee</strong> — invite team members to the event</li>
        <li><strong>Add location</strong> — physical or virtual meeting location</li>
        <li><strong>Add description</strong> — any additional context or agenda</li>
        <li><strong>Linked with</strong> — link the event to a specific Lead or Deal so it appears in that record's activity timeline</li>
        <li><strong>Private</strong> — under More options, mark the event as private if it should only be visible to you</li>
      </ul>
      <p class="mb-6 leading-relaxed">
        Click <strong>Create event</strong> to save it to the calendar.
      </p>

      <h2 id="calendar-events" class="text-2xl font-semibold mt-10 mb-4">Calendar Events</h2>
      <p class="mb-4 leading-relaxed">
        Events on the calendar are pulled from tasks, follow-ups, and manually created events linked
        to your leads and deals. Each event shows:
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Title</strong> — the event or task name</li>
        <li><strong>Due Date</strong> — when it's scheduled</li>
        <li><strong>Linked Record</strong> — the lead or deal it belongs to</li>
        <li><strong>Assigned To</strong> — the agent responsible</li>
      </ul>

      <h2 id="navigating" class="text-2xl font-semibold mt-10 mb-4">Navigating the Calendar</h2>
      <p class="mb-4 leading-relaxed">
        Use the <strong>arrow buttons</strong> at the top to move forward or backward in time. Click
        <strong>Today</strong> to jump back to the current date instantly. Click any event on the
        calendar to open the linked lead or deal directly.
      </p>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
        <p class="text-sm text-blue-800 dark:text-blue-200">
          <strong>Tip:</strong> Always link events to a Lead or Deal using the <strong>Linked with</strong>
          field. This keeps the event visible in that record's activity timeline so your whole team
          has context without needing to check the calendar separately.
        </p>
      </div>
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
