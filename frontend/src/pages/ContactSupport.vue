<template>
 <div
  class="min-h-screen flex items-start sm:items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200 px-3 sm:px-4 py-6 overflow-y-auto"
>
    <div
  class="bg-white p-4 sm:p-6 md:p-8 rounded-2xl shadow-xl w-full max-w-lg mx-auto transition-all duration-300 my-4 sm:my-6"
>
      <!-- Header -->
      <div class="text-center mb-6">
        <h1 class="text-3xl font-bold text-gray-800">Contact Support</h1>
        <p class="text-gray-500 text-sm mt-1">We're here to help you</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="submitForm" novalidate class="space-y-2 sm:space-y-3">
        <div>
          <label class="label">Name</label>
          <input
            v-model="name"
            type="text"
            placeholder="Enter your name"
            class="input"
          />
        </div>

        <div>
          <label class="label">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="Enter your email"
            class="input"
          />
        </div>

        <div>
          <label class="label">Your Issue</label>
          <textarea
            v-model="message"
            rows="3"
            placeholder="Describe your issue..."
            class="input resize-none"
          ></textarea>
        </div>

        <button
          class="btn flex items-center justify-center gap-2"
          :disabled="loading"
        >
          <span v-if="!loading">Submit</span>
          <span v-else class="loader"></span>
        </button>
      </form>

      <p class="text-xs text-gray-400 text-center mt-6">
        Support team usually replies within 24 hours
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { call } from 'frappe-ui'

const name = ref('')
const email = ref('')
const message = ref('')
const loading = ref(false)

const showToast = (msg, type = 'error') => {
  if (window.frappe && window.frappe.show_alert) {
    window.frappe.show_alert(
      {
        message: msg,
        indicator: type === 'success' ? 'green' : 'red',
      },
      4
    )
    return
  }

  const toast = document.createElement('div')
  toast.className = `custom-toast ${type}`
  toast.textContent = msg

  document.body.appendChild(toast)

  setTimeout(() => {
    toast.classList.add('show')
  }, 10)

  setTimeout(() => {
    toast.classList.remove('show')
    setTimeout(() => toast.remove(), 300)
  }, 3500)
}

const showError = (msg) => showToast(msg, 'error')
const showSuccess = (msg) => showToast(msg, 'success')  

/* email validation*/
const isValidEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}

/*space check*/
const isEmptyOrSpaces = (value) => {
  return !value || value.trim().length === 0
}

const submitForm = async () => {


  /* validations */
  if (isEmptyOrSpaces(name.value)) {
   showError('Name is required')
    return
  }

  if (isEmptyOrSpaces(email.value)) {
   showError('Email is required')
    return
  }

  if (!isValidEmail(email.value)) {
showError('Please enter a valid email address')
    return
  }

  if (isEmptyOrSpaces(message.value)) {
   showError('Message cannot be empty')
    return
  }
  loading.value = true

  try {
    const res = await call('crm.api.contact_support.contact_support', {
      name: name.value.trim(),
      email: email.value.trim(),
      message: message.value.trim(),
    })

    
    if (res && res.status === 'success') {
     showSuccess(
  'Your request has been submitted successfully! Our team will contact you soon.'
)

      name.value = ''
      email.value = ''
      message.value = ''
    } else {
     showError('Something went wrong')
    }
  } catch (err) {
    console.error('ERROR:', err)
    showError('Session expired or server error. Please refresh.')
  } finally {
    loading.value = false
  }
}
</script>
<style>

* {
  box-sizing: border-box;
}

body {
  overflow-x: hidden;
}

/* INPUT */

.input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  transition: all 0.2s ease;
  outline: none;
  font-size: 15px;
  background: #fff;
}

.input:focus {
  border-color: #d946ef;
  box-shadow: 0 0 0 3px rgba(217, 70, 239, 0.2);
}

/* LABEL */

.label {
  display: block;
  font-size: 14px;
  margin-bottom: 5px;
  color: #374151;
  font-weight: 500;
}

/* BUTTON */

.btn {
  width: 100%;
  background: linear-gradient(135deg, #f472b6, #d946ef);
  color: white;
  padding: 12px;
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  min-height: 46px;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 15px rgba(217, 70, 239, 0.3);
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* LOADER */

.loader {
  width: 18px;
  height: 18px;
  border: 2px solid white;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* TOAST */

.custom-toast {
  position: fixed;
  top: 24px;
  right: 24px;
  background: #fff;
  color: #374151;
  padding: 14px 18px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  font-size: 14px;
  font-weight: 500;
  z-index: 9999;
  opacity: 0;
  transform: translateY(-12px);
  transition: all 0.25s ease;
  min-width: 260px;
  max-width: 420px;
}
.custom-toast.show {
  opacity: 1;
  transform: translateY(0);
}

.custom-toast.error {
  border-left: 4px solid #ef4444;
}

.custom-toast.success {
  border-left: 4px solid #22c55e;
}

/* ANIMATION */

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* MOBILE */

@media (max-width: 768px) {

  .input {
    font-size: 14px;
    padding: 11px;
  }

  .btn {
    font-size: 14px;
    padding: 11px;
  }

  .label {
    font-size: 13px;
  }

  .custom-toast {
    left: 16px;
    right: 16px;
    top: 16px;
    width: auto;
    max-width: unset;
    font-size: 13px;
    padding: 12px 14px;
  }
}

</style>

