<template>
  <div class="flex h-full bg-surface-[#f8f9fb]">
    <aside
      :class="[
        'help-sidebar border-r border-gray-200 bg-white flex flex-col transition-all duration-300 ease-in-out overflow-visible',
        collapsed ? 'w-[70px]' : 'w-[260px]',
        { collapsed },
      ]"
    >
      <!-- HEADER -->
      <div v-if="!collapsed" class="px-5 py-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold">Help Center</h2>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search articles..."
          class="mt-3 w-full px-3 py-2 text-sm border rounded-md"
        />
      </div>

      <!-- SIDEBAR -->
      <div class="flex-1 overflow-y-auto overflow-x-visible">
        <HelpSidebar
          v-model:collapsed="collapsed"
          :search="searchQuery"
          :class="collapsed ? 'mt-4 w-full' : ''"
        />
      </div>

      <!-- TOGGLE -->
      <div
        class="mt-auto flex items-center justify-center px-2 py-3 border-t cursor-pointer hover:bg-gray-100"
        @click="toggleSidebar"
      >
        <span
          class="text-lg transition-transform duration-300"
          :class="{ 'rotate-180': collapsed }"
          >←</span
        >
        <span v-if="!collapsed" class="ml-2 text-sm">Collapse</span>
      </div>
    </aside>

    <main class="flex-1 p-8 overflow-y-auto bg-white">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HelpSidebar from '@/components/help-center/HelpSidebar.vue'

const searchQuery = ref('')
const collapsed = ref(false)

function toggleSidebar() {
  collapsed.value = !collapsed.value
}
</script>
<style scoped>
.help-sidebar.collapsed {
  align-items: center;
}
.help-sidebar.collapsed nav {
  display: flex;
  justify-content: center;
}
.help-sidebar.collapsed ul {
  padding: 0;
}
</style>