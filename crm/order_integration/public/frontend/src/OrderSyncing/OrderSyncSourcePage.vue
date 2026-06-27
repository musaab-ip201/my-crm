<template>
	<div class="flex-1 p-6">
		<div v-if="step === 'list'" class="flex flex-col gap-4">
			<div class="flex gap-2 mb-4">
				<button 
					@click="viewMode = 'sources'"
					:class="['px-4 py-2 rounded', viewMode === 'sources' ? 'bg-blue-600 text-white' : 'bg-gray-200']"
				>
					Order Sources
				</button>
				<button 
					@click="viewMode = 'viewer'"
					:class="['px-4 py-2 rounded', viewMode === 'viewer' ? 'bg-blue-600 text-white' : 'bg-gray-200']"
				>
					Data Viewer
				</button>
				<button 
					@click="viewMode = 'api-viewer'"
					:class="['px-4 py-2 rounded', viewMode === 'api-viewer' ? 'bg-blue-600 text-white' : 'bg-gray-200']"
				>
					API Data Viewer
				</button>
			</div>
			<OrderSyncSources v-if="viewMode === 'sources'" @updateStep="updateStep" />
			<DynamicLeadViewer v-else-if="viewMode === 'viewer'" />
			<APIDataViewer v-else-if="viewMode === 'api-viewer'" />
		</div>
		<OrderSyncSourceForm v-else :sourceData="selectedSource" @updateStep="updateStep" />
	</div>
</template>

<script setup>
import { ref } from "vue";
import OrderSyncSources from "./OrderSyncSources.vue";
import OrderSyncSourceForm from "./OrderSyncSourceForm.vue";
import DynamicLeadViewer from "./DynamicLeadViewer.vue";
import APIDataViewer from "./APIDataViewer.vue";

const step = ref("list");
const selectedSource = ref(null);
const viewMode = ref("sources");

function updateStep(newStep, data = null) {
	step.value = newStep;
	selectedSource.value = data;
}
</script>

