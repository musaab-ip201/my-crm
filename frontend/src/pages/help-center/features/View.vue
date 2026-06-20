<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">

      <h1 class="text-3xl font-bold mb-6">Views</h1>

      <p class="mb-4 leading-relaxed">
        Views allow you to customize how data appears in list views by applying filters, sorting records,
        and selecting the columns you want to display. This helps you quickly access frequently used data
        configurations without needing to reconfigure them every time.
      </p>

      <img
        src="@/assets/views.png"
        alt="Views dropdown showing Saved Views and Create View options"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
      />

      <h2 id="what-is-a-view" class="text-2xl font-semibold mt-10 mb-4">What is a View?</h2>
      <p class="mb-4 leading-relaxed">A View is a combination of:</p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Filters</strong> – Show only records that match specific conditions.</li>
        <li><strong>Sorting</strong> – Arrange records in a particular order (ascending or descending).</li>
        <li><strong>Columns</strong> – Choose which fields appear in the list view.</li>
      </ul>
      <p class="mb-8 leading-relaxed">
        Views help users organize CRM data according to their workflow.
      </p>

      <h2 id="types-of-views" class="text-2xl font-semibold mt-10 mb-4">Types of Views</h2>
      <p class="mb-4 leading-relaxed">There are three types of views available in the CRM:</p>
      <ul class="list-disc ml-6 mb-8 space-y-2 marker:text-pink-500">
        <li>Saved Views</li>
        <li>Public Views</li>
        <li>Pinned Views</li>
      </ul>

      <h2 id="saved-views" class="text-2xl font-semibold mt-10 mb-4">1. Saved Views</h2>
      <p class="mb-4 leading-relaxed">
        Saved Views allow users to store customized list configurations for personal use.
        By default, saved views are private and only visible to the user who created them.
      </p>

      <h3 id="creating-saved-view" class="text-xl font-semibold mt-6 mb-3">Creating a Saved View</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Navigate to the list view (Leads, Deals, Contacts, etc.).</li>
        <li>Apply your desired filters, sorting, and column selections.</li>
        <li>Click the three-dot menu <strong>(⋯)</strong> in the list view header.</li>
        <li>Select <strong>Duplicate</strong>.</li>
        <li>Enter a name for the view and click <strong>Duplicate</strong>.</li>
        <li>The new view will appear in the view dropdown menu.</li>
      </ul>

      <h3 id="managing-saved-views" class="text-xl font-semibold mt-6 mb-3">Managing Saved Views</h3>
      <p class="mb-4 leading-relaxed">From the three-dot menu you can:</p>
      <ul class="list-disc ml-6 mb-8 space-y-2 marker:text-pink-500">
        <li><strong>Edit</strong> – Change the name or icon.</li>
        <li><strong>Delete</strong> – Remove the saved view.</li>
        <li><strong>Pin View</strong> – Add it to the sidebar for quick access.</li>
        <li><strong>Make Public</strong> – Share it with other users.</li>
      </ul>

      <h2 id="public-views" class="text-2xl font-semibold mt-10 mb-4">2. Public Views</h2>
      <p class="mb-4 leading-relaxed">
        Public Views are shared views that are accessible to all users in the CRM system.
        They are useful when teams need to work with the same data layout or filters.
      </p>

      <h3 id="public-views-examples" class="text-xl font-semibold mt-6 mb-3">Examples of Public Views</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Leads filtered by a specific industry or source</li>
        <li>High-value deals requiring attention</li>
        <li>Views showing specific customer details for sales teams</li>
      </ul>

      <h3 id="who-can-create-public-views" class="text-xl font-semibold mt-6 mb-3">Who Can Create Public Views?</h3>
      <p class="mb-6 leading-relaxed">
        Only users with the <strong>Sales Manager</strong> role can create Public Views.
      </p>

      <h3 id="creating-public-view" class="text-xl font-semibold mt-6 mb-3">Creating a Public View</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Navigate to the desired list view.</li>
        <li>Create or select an existing saved view.</li>
        <li>Click the three-dot menu <strong>(⋯)</strong> for that view.</li>
        <li>Select <strong>Make Public</strong>.</li>
        <li>The view will now appear under Public Views for all users.</li>
      </ul>

      <h3 id="making-public-view-private" class="text-xl font-semibold mt-6 mb-3">Making a Public View Private</h3>
      <ul class="list-disc ml-6 mb-8 space-y-2 marker:text-pink-500">
        <li>Open the three-dot menu <strong>(⋯)</strong>.</li>
        <li>Select <strong>Make Private</strong>.</li>
      </ul>

      <h2 id="pinned-views" class="text-2xl font-semibold mt-10 mb-4">3. Pinned Views</h2>
      <p class="mb-4 leading-relaxed">
        Pinned Views allow you to quickly access frequently used views directly from the sidebar.
      </p>

      <h3 id="pinning-a-view" class="text-xl font-semibold mt-6 mb-3">Pinning a View</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Navigate to the list view.</li>
        <li>Create or select an existing saved view.</li>
        <li>Click the three-dot menu <strong>(⋯)</strong>.</li>
        <li>Select <strong>Pin View</strong>.</li>
        <li>The view will appear in the <strong>Pinned Views</strong> section in the sidebar.</li>
      </ul>

      <h3 id="unpinning-a-view" class="text-xl font-semibold mt-6 mb-3">Unpinning a View</h3>
      <ul class="list-disc ml-6 mb-8 space-y-2 marker:text-pink-500">
        <li>Open the three-dot menu <strong>(⋯)</strong> for the pinned view.</li>
        <li>Select <strong>Unpin View</strong>.</li>
        <li>The view will return to a regular saved view.</li>
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

<style>
html { scroll-behavior: smooth; }
</style>
