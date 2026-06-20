<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Tasks</h1>

      <p class="mb-6 leading-relaxed">
        Tasks are action items you need to complete like sending a proposal, scheduling a demo, or
        following up on a document. They can be linked to a Lead or Deal and assigned to a team member.
      </p>

      <h2 id="creating-task" class="text-2xl font-semibold mt-10 mb-4">Creating a Task</h2>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>From the sidebar</strong> — click <strong>Tasks → + Create</strong> to create a standalone task</li>
        <li><strong>From inside a Lead or Deal</strong> — click the <strong>Tasks</strong> tab → <strong>+ New Task</strong></li>
        <li><strong>During a call</strong> — use the "Add Task" button in the call popup to create a task on the spot</li>
      </ul>

      <h2 id="task-fields" class="text-2xl font-semibold mt-10 mb-4">Task Fields</h2>
      <p class="mb-4 leading-relaxed">
        When creating a task, fill in the following:
      </p>
      <ul class="list-disc ml-6 mb-4 space-y-2 marker:text-pink-500">
        <li><strong>Title</strong> — what needs to be done</li>
        <li><strong>Description</strong> — additional context or details</li>
        <li><strong>Status</strong> — defaults to <em>Backlog</em>; can be moved to In Progress or Completed</li>
        <li><strong>Assigned To</strong> — which team member is responsible</li>
        <li><strong>Due Date</strong> — when it should be completed</li>
        <li><strong>Priority</strong> — Low, Medium, or High</li>
      </ul>

      <img
        src="@/assets/tasks-create.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="Create Task Form"
      />

      <h2 id="calendar" class="text-2xl font-semibold mt-10 mb-4">Tasks on the Calendar</h2>
      <p class="mb-4 leading-relaxed">
        All tasks with due dates appear on the <strong>Calendar</strong> page. This gives you a visual
        overview of what's due when across your team.
      </p>

      <h2 id="completing-task" class="text-2xl font-semibold mt-10 mb-4">Completing a Task</h2>
      <p class="mb-4 leading-relaxed">
        Open the task and change the status to <strong>Completed</strong>, or check the checkbox next
        to it in the list view. Completed tasks are moved out of the active view automatically.
      </p>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
        <p class="text-sm text-blue-800 dark:text-blue-200">
          <strong>Tip:</strong> Tasks created from inside a Lead or Deal are linked to that record and
          appear in its activity timeline, keeping all follow-up actions visible to your whole team.
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
