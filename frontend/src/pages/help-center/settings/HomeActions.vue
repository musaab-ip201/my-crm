<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Customization: Home Actions</h1>

      <p class="mb-6 leading-relaxed">
        Home Actions let you configure the shortcuts that appear in the home dropdown menu of IP CRM. You can add, edit, reorder, and remove actions to match your team's daily workflow. Access via <strong>Settings → Customization → Home Actions</strong>.
      </p>

      <!-- EDIT GRID FIELDS LAYOUT -->
      <h2 id="edit-grid-fields-layout" class="text-2xl font-semibold mt-10 mb-4">Edit Grid Fields Layout</h2>

      <img
        src="@/assets/homeactions-grid-layout.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Edit Grid Fields Layout"
      />

      <p class="mb-4 leading-relaxed">
        The Home Actions page shows all configured actions in a grid with columns: <strong>No</strong>, <strong>Label</strong>, <strong>Type</strong>, <strong>Route</strong>, and <strong>Hidden</strong>. You can customize which columns are shown and in what order using the <strong>Edit Grid Fields Layout</strong> dialog.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Opening Edit Grid Fields Layout</h3>
      <p class="mb-4 leading-relaxed">
        Click the <strong>⚙ gear icon</strong> at the top right of the grid to open this dialog. It controls which columns appear in the grid and their display order.
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Fields Order</strong> — lists all visible columns: Label, Type, Route, Hidden</li>
        <li><strong>Drag handle (⠿)</strong> — drag rows up or down to reorder the columns in the grid</li>
        <li><strong>Number field</strong> — set the width or order number for each column</li>
        <li><strong>✕ next to each field</strong> — removes that column from the grid view</li>
        <li><strong>+ Add Field</strong> — adds a new column to the grid from available fields</li>
        <li><strong>Save</strong> — applies the layout changes to the grid</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Grid Columns Explained</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>No</strong> — the row number showing the order actions appear in the dropdown</li>
        <li><strong>Label</strong> — the display name of the action shown to users in the dropdown</li>
        <li><strong>Type</strong> — either <strong>Route</strong> (navigates to a page) or <strong>Separator</strong> (adds a divider line between actions)</li>
        <li><strong>Route</strong> — the URL or path the action navigates to when clicked</li>
        <li><strong>Hidden</strong> — checkbox to hide this action from the dropdown without deleting it</li>
        <li><strong>✎ edit icon</strong> (right of each row) — opens the Editing Row dialog for that action</li>
        <li><strong>Checkbox</strong> (left of each row) — select one or more rows to delete them</li>
      </ul>

      <!-- ADD ROW -->
      <h2 id="add-row" class="text-2xl font-semibold mt-10 mb-4">Add Row</h2>

      <p class="mb-4 leading-relaxed">
        Click <strong>+ Add Row</strong> at the bottom of the grid to add a new action to the home dropdown. A new empty row is added to the grid. Click the <strong>✎ edit icon</strong> on the new row to configure it.
      </p>

      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Set the <strong>Type</strong> to <strong>Route</strong> to create a navigation shortcut</li>
        <li>Set the <strong>Type</strong> to <strong>Separator</strong> to add a divider between groups of actions</li>
        <li>Fill in the <strong>Label</strong>, <strong>Icon</strong>, and <strong>Route</strong> fields</li>
        <li>Toggle <strong>Hidden</strong> off so the action is visible to users</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Deleting Rows</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Check the <strong>checkbox</strong> on the left of one or more rows to select them</li>
        <li>A delete option appears — click it to remove the selected rows</li>
        <li>Standard system actions cannot be permanently deleted — use <strong>Hidden</strong> to hide them instead</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Saving Changes</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>After making all changes to the grid, click <strong>Update</strong> (top right, black button) to save and apply all changes</li>
        <li>Changes take effect immediately for all users after saving</li>
      </ul>

      <!-- EDITING A ROW -->
      <h2 id="editing-row" class="text-2xl font-semibold mt-10 mb-4">Editing a Row</h2>

      <img
        src="@/assets/homeactions-editing-row.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Editing Row"
      />

      <p class="mb-4 leading-relaxed">
        Click the <strong>✎ edit icon</strong> on any row to open the Editing Row dialog. This lets you configure every detail of that action.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Fields in the Editing Row Dialog</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Name</strong> — the internal system name for this action, e.g. "logout". Not shown to users</li>
        <li><strong>Icon</strong> — the icon displayed next to the action label. Add SVG code or use Feather icon names, e.g. "settings", "log-out", "home"</li>
        <li><strong>Label</strong> (required) — the text shown to users in the dropdown, e.g. "Log out"</li>
        <li><strong>Type</strong> — select the action type:
          <ul class="list-disc ml-6 mt-2 space-y-1 marker:text-pink-300">
            <li><strong>Route</strong> — navigates to a specific page or URL when clicked</li>
            <li><strong>Separator</strong> — adds a visual divider line between actions in the dropdown</li>
          </ul>
        </li>
        <li><strong>Route</strong> (required when Type is Route) — the path or URL to navigate to, e.g. "#" or "/crm/leads"</li>
        <li><strong>Open in new window</strong> — when checked, the route opens in a new browser tab</li>
        <li><strong>Hidden</strong> — when checked, this action is hidden from the dropdown without being deleted</li>
        <li><strong>Is Standard</strong> — indicates this is a built-in system action. Standard actions cannot be fully deleted</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Edit Grid Row Fields Layout</h3>

      <img
        src="@/assets/homeactions-edit-row-fields.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Edit Grid Row Fields Layout"
      />

      <p class="mb-4 leading-relaxed">
        Inside the Editing Row dialog, click the <strong>✎ edit icon</strong> at the top right to open the <strong>Edit Grid Row Fields Layout</strong> dialog. This lets you customize which fields appear in the row editing form and how they are arranged.
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Show preview</strong> — toggle to see a live preview of how the form will look</li>
        <li><strong>+ Add Tab</strong> — add a new tab to organize fields into groups</li>
        <li><strong>Left column</strong> — shows fields currently in the left side of the form: Name, Label, Type, Route, Open in new window, Hidden, Is Standard</li>
        <li><strong>Right column</strong> — shows fields in the right side: Icon</li>
        <li><strong>Drag handle (⠿)</strong> next to each field — drag to reorder fields within a column</li>
        <li><strong>✕ next to each field</strong> — removes that field from the form layout</li>
        <li><strong>+ Add Field</strong> — adds a field to that column from available options</li>
        <li><strong>+ Add Section</strong> — adds a new section divider within the form</li>
        <li><strong>Reset</strong> — resets the layout back to the default arrangement</li>
        <li><strong>Save</strong> — saves the custom layout</li>
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
