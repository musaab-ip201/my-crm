<template>
  <div class="flex">
    <div class="help-content flex-1 max-w-4xl mx-auto px-2 text-gray-800 dark:text-gray-200">
      <h1 class="text-3xl font-bold mb-6">User Management</h1>

      <p class="mb-6 leading-relaxed">
        Manage who has access to IP CRM and control what each person can do. Access via <strong>Settings → User Management</strong>. You can view existing users, add users already in the system, or send email invites to new ones.
      </p>

      <!-- USERS -->
      <h2 id="users" class="text-2xl font-semibold mt-10 mb-4">Users</h2>

      <img
        src="@/assets/usermgmt-users.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Users list in IP CRM"
      />

      <p class="mb-4 leading-relaxed">
        The Users page shows all team members who currently have access to IP CRM. Each user is listed with their name, email, and assigned role.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Buttons & Actions on the Users Page</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>+ New</strong> (top right, black button) — opens the Add Existing User dialog to add a user already in the system</li>
        <li><strong>Search user</strong> — search bar to quickly find a user by name or email</li>
        <li><strong>All</strong> (dropdown, top right of list) — filter users by role — All, Admin, Manager, or Sales User</li>
        <li><strong>Role badge</strong> (e.g. Sales User) — shows the current role of each user. Click the dropdown arrow next to it to change the role</li>
        <li><strong>Role options</strong> — Admin, Manager, Sales User. A checkmark shows the currently assigned role</li>
        <li><strong>... (three dots)</strong> — additional options for that user such as removing them from the CRM</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Roles Explained</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Admin</strong> — full access to all settings, data, and reports across the entire CRM</li>
        <li><strong>Manager</strong> — can manage team members, view all leads and deals, and access reports</li>
        <li><strong>Sales User</strong> — can work on leads and deals and create private views and reports</li>
      </ul>

      <!-- ADD NEW -->
      <h2 id="add-new" class="text-2xl font-semibold mt-10 mb-4">Add New User</h2>

      <img
        src="@/assets/usermgmt-addnew.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Add Existing User dialog"
      />

      <p class="mb-4 leading-relaxed">
        The <strong>Add Existing User</strong> dialog lets you add someone who already has an account in the system to IP CRM. They will be granted access using their current credentials — no new password needed.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Fields in the Dialog</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Users</strong> — enter the email address of the existing system user (e.g. john@doe.com)</li>
        <li><strong>Role</strong> — select the role to assign — Sales User, Manager, or Admin. A description of what each role can do is shown below the dropdown</li>
        <li><strong>Add</strong> (bottom right button) — confirms and adds the user with the selected role</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Add an Existing User</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Go to <strong>Settings → User Management → Users</strong></li>
        <li>Click <strong>+ New</strong> in the top right</li>
        <li>Enter the user's email address in the <strong>Users</strong> field</li>
        <li>Select their <strong>Role</strong> from the dropdown</li>
        <li>Click <strong>Add</strong> to grant them access</li>
      </ul>

      <!-- INVITE USERS -->
      <h2 id="invite-users" class="text-2xl font-semibold mt-10 mb-4">Invite Users</h2>

      <img
        src="@/assets/usermgmt-invite.png"
        class="rounded-lg shadow-md mb-8 w-full max-h-[500px] object-contain"
        alt="Send Invites to Users"
      />

      <p class="mb-4 leading-relaxed">
        The <strong>Send Invites</strong> page lets you invite new people to IP CRM by email. They will receive a link to create their account and set a password. You can invite multiple users at once.
      </p>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">Fields on the Invite Page</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li><strong>Invite by email</strong> — enter one or more email addresses. Separate multiple addresses with a comma (e.g. user1@example.com, user2@example.com)</li>
        <li><strong>Invite as</strong> — select the role for all invited users — Sales User, Manager, or Admin. A description of the role is shown below</li>
        <li><strong>Send Invites</strong> (top right button) — sends the invitation emails to all addresses entered</li>
        <li><strong>Pending Invites</strong> — shows invitations that have been sent but not yet accepted. Each pending invite shows the email and assigned role. Click <strong>✕</strong> to cancel a pending invite</li>
      </ul>

      <h3 class="text-lg font-semibold mt-6 mb-2 text-gray-700 dark:text-gray-300">How to Invite a New User</h3>
      <ul class="list-disc ml-6 mb-6 space-y-2 marker:text-pink-500">
        <li>Go to <strong>Settings → User Management → Invite User</strong></li>
        <li>Enter the email address(es) in the <strong>Invite by email</strong> field — separate multiple with commas</li>
        <li>Select the <strong>Role</strong> from the <strong>Invite as</strong> dropdown</li>
        <li>Click <strong>Send Invites</strong></li>
        <li>The invited user will receive an email with a link to set up their account</li>
        <li>Once they log in, go to Users and assign them to their Shift, Department, and Team</li>
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
