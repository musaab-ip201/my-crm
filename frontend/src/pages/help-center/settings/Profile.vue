<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">Profile</h1>

      <p class="mb-6 leading-relaxed">
        Manage your personal information and preferences to customize your IP CRM experience. Keep your profile up-to-date for better collaboration with your team.
      </p>

      <img
        src="@/assets/settings-profile.png"
        class="rounded-lg shadow-md mb-8 w-full object-contain"
        alt="IP CRM Profile Settings"
      />

      <h2 id="personal-info" class="text-2xl font-semibold mt-10 mb-4">Personal Information</h2>
      <p class="mb-4 leading-relaxed">
        Update your name, email address, and profile picture. This information is visible to other users in your organization.
      </p>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Full name and display name</li>
        <li>Email address for notifications</li>
        <li>Profile picture for easy identification</li>
        <li>Contact number for team communication</li>
      </ul>

      <h2 id="password" class="text-2xl font-semibold mt-10 mb-4">Password Management</h2>
      <p class="mb-4 leading-relaxed">
        Change your password regularly to maintain account security. Use a strong password with a mix of letters, numbers, and special characters. Click <strong>Change Password</strong> in the top right of the Profile page to update it.
      </p>

      <h2 id="timezone" class="text-2xl font-semibold mt-10 mb-4">Timezone Settings</h2>
      <p class="mb-4 leading-relaxed">
        Set your local timezone to ensure accurate timestamps for call logs, meetings, and task reminders. This is crucial for teams working across different time zones.
      </p>

      <h2 id="preferences" class="text-2xl font-semibold mt-10 mb-4">User Preferences</h2>
      <p class="mb-4 leading-relaxed">
        Customize your interface language, date format, and other display preferences to match your working style.
      </p>

      <h2 id="how-to-update" class="text-2xl font-semibold mt-10 mb-4">How to Update Your Profile</h2>
      <ol class="list-decimal ml-6 mb-6 space-y-2">
        <li>Click your avatar or name at the top of the sidebar to open Settings.</li>
        <li>Navigate to <strong>Settings → Profile</strong>.</li>
        <li>Update your <strong>First</strong> or <strong>Last name</strong> if needed.</li>
        <li>Click <strong>Edit profile photo</strong> to update your avatar image.</li>
        <li>Enter a new password in the password field to change it.</li>
        <li>Click <strong>Update</strong> to apply all changes.</li>
      </ol>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
        <p class="text-sm text-blue-800 dark:text-blue-200">
          <strong>Tip:</strong> Your profile picture and name appear in the activity timeline of every lead and deal you interact with, so keeping them accurate helps your team identify who did what.
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
