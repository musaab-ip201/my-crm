<template>
  <div class="flex flex-col gap-4 p-4">
    <h4 class="font-bold">Sync Failure Logs</h4>
    <div
      v-for="log in logs"
      :key="log.name"
      class="border-l-4 border-red-500 bg-red-50 p-3 rounded"
    >
      <div class="flex justify-between text-sm">
        <span class="font-bold text-red-700">{{ log.source }}</span>
        <span class="text-gray-500">{{ log.creation }}</span>
      </div>
      <p class="text-sm mt-1">{{ log.message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const logs = ref([])
onMounted(() => {
  frappe
    .call('your_app.api.get_order_logs')
    .then((r) => (logs.value = r.message || []))
})
</script>
