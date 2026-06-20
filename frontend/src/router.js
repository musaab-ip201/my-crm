import { createRouter, createWebHistory } from 'vue-router'
import { usersStore } from '@/stores/users'
import { sessionStore } from '@/stores/session'
import { viewsStore } from '@/stores/views'

const handleMobileView = (componentName) => {
  return window.innerWidth < 768 ? `Mobile${componentName}` : componentName
}

const routes = [
  {
    path: '/',
    name: 'Home',
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: () => import('@/pages/MobileNotification.vue'),
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/pages/Dashboard.vue'),
  },
  {
    path: '/call-center-test',
    name: 'CallCenterTest',
    component: () => import('@/pages/CallCenterTest.vue'),
  },
  {
    alias: '/leads',
    path: '/leads/view/:viewType?',
    name: 'Leads',
    component: () => import('@/pages/Leads.vue'),
  },
  {
    path: '/leads/:leadId',
    name: 'Lead',
    component: () => import(`@/pages/${handleMobileView('Lead')}.vue`),
    props: true,
  },
  {
    alias: '/deals',
    path: '/deals/view/:viewType?',
    name: 'Deals',
    component: () => import('@/pages/Deals.vue'),
  },
  {
    path: '/deals/:dealId',
    name: 'Deal',
    component: () => import(`@/pages/${handleMobileView('Deal')}.vue`),
    props: true,
  },
  {
    alias: '/notes',
    path: '/notes/view/:viewType?',
    name: 'Notes',
    component: () => import('@/pages/Notes.vue'),
  },
  {
    alias: '/tasks',
    path: '/tasks/view/:viewType?',
    name: 'Tasks',
    component: () => import('@/pages/Tasks.vue'),
  },
  {
    alias: '/contacts',
    path: '/contacts/view/:viewType?',
    name: 'Contacts',
    component: () => import('@/pages/Contacts.vue'),
  },
  {
    path: '/contacts/:contactId',
    name: 'Contact',
    component: () => import(`@/pages/${handleMobileView('Contact')}.vue`),
    props: true,
  },
  {
    alias: '/organizations',
    path: '/organizations/view/:viewType?',
    name: 'Organizations',
    component: () => import('@/pages/Organizations.vue'),
  },
  {
    path: '/organizations/:organizationId',
    name: 'Organization',
    component: () => import(`@/pages/${handleMobileView('Organization')}.vue`),
    props: true,
  },
  {
    alias: '/call-logs',
    path: '/call-logs/view/:viewType?',
    name: 'Call Logs',
    component: () => import('@/pages/CallLogs.vue'),
  },
  {
    path: '/auto-dialer',
    name: 'AutoDialerQueue',
    component: () => import('@/pages/AutoDialerQueue.vue'),
  },
  {
    path: '/lead-history',
    name: 'LeadHistory',
    component: () => import('@/pages/LeadHistory.vue'),
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: () => import('@/pages/Calendar.vue'),
  },
  {
    path: '/data-import',
    name: 'DataImportList',
    component: () => import('@/pages/DataImport.vue'),
  },
  {
    path: '/data-import/doctype/:doctype',
    name: 'NewDataImport',
    component: () => import('@/pages/DataImport.vue'),
    props: true,
  },
  {
    path: '/data-import/:importName',
    name: 'DataImport',
    component: () => import('@/pages/DataImport.vue'),
    props: true,
  },
  {
    path: '/welcome',
    name: 'Welcome',
    component: () => import('@/pages/Welcome.vue'),
  },
  {
    path: '/:invalidpath',
    name: 'Invalid Page',
    component: () => import('@/pages/InvalidPage.vue'),
  },
  {
    path: '/not-permitted',
    name: 'Not Permitted',
    component: () => import('@/pages/NotPermitted.vue'),
  },
  {
    path: '/contact-support',
    name: 'ContactSupport',
    component: () => import('@/pages/ContactSupport.vue'),
    meta: { fullPage: true },
  },
  {
    path: '/help-center',
    component: () => import('@/pages/help-center/HelpCenter.vue'),
    children: [
      {
        path: '',
        redirect: '/help-center/introduction',
      },

      // Introduction
      {
        path: 'introduction',
        name: 'HelpIntroduction',
        component: () => import('@/pages/help-center/introduction/Introduction.vue'),
      },
      {
        path: 'setting-up',
        name: 'HelpSettingUp',
        component: () => import('@/pages/help-center/introduction/SettingUp.vue'),
      },

      // Settings
      {
        path: 'settings',
        name: 'HelpSettings',
        component: () => import('@/pages/help-center/settings/Settings.vue'),
      },
      {
        path: 'settings/profile',
        name: 'HelpProfile',
        component: () => import('@/pages/help-center/settings/Profile.vue'),
      },
      {
        path: 'settings/system-configuration',
        name: 'HelpSystemConfiguration',
        component: () => import('@/pages/help-center/settings/SystemConfiguration.vue'),
      },
      {
        path: 'settings/user-management',
        name: 'HelpUserManagement',
        component: () => import('@/pages/help-center/settings/UserManagement.vue'),
      },
      {
        path: 'settings/email-settings',
        name: 'HelpEmailSettings',
        component: () => import('@/pages/help-center/settings/EmailSettings.vue'),
      },
      {
        path: 'settings/automation-rules',
        name: 'HelpAutomationRules',
        component: () => import('@/pages/help-center/settings/AutomationRules.vue'),
      },
      {
        path: 'settings/home-actions',
        name: 'HelpHomeActions',
        component: () => import('@/pages/help-center/settings/HomeActions.vue'),
      },
      {
        path: 'settings/integrations',
        name: 'HelpInviteUsers',
        component: () => import('@/pages/help-center/settings/Integrations.vue'),
      },

      // Masters
      {
        path: 'masters/lead',
        name: 'HelpLead',
        component: () => import('@/pages/help-center/masters/Lead.vue'),
      },
      {
        path: 'masters/leadhistory',
        name: 'HelpLeadHistory',
        component: () => import('@/pages/help-center/masters/LeadHistory.vue'),
      },
      {
        path: 'masters/calendar',
        name: 'HelpCalendar',
        component: () => import('@/pages/help-center/masters/Calendar.vue'),
      },
      {
        path: 'masters/deal',
        name: 'HelpDeal',
        component: () => import('@/pages/help-center/masters/Deal.vue'),
      },
      {
        path: 'masters/contact',
        name: 'HelpContact',
        component: () => import('@/pages/help-center/masters/Contact.vue'),
      },
      {
        path: 'masters/organization',
        name: 'HelpOrganization',
        component: () => import('@/pages/help-center/masters/Organization.vue'),
      },
      {
        path: 'masters/note',
        name: 'HelpNote',
        component: () => import('@/pages/help-center/masters/Note.vue'),
      },
      {
        path: 'masters/task',
        name: 'HelpTask',
        component: () => import('@/pages/help-center/masters/Task.vue'),
      },
      {
        path: 'masters/call-log',
        name: 'HelpCallLog',
        component: () => import('@/pages/help-center/masters/Calls.vue'),
      },

      // Capturing Leads
      {
        path: 'capturing-leads/custom-scripts',
        name: 'HelpCustomScripts',
        component: () => import('@/pages/help-center/capturing-leads/CustomScripts.vue'),
      },
      {
        path: 'capturing-leads/web-form',
        name: 'HelpWebForm',
        component: () => import('@/pages/help-center/capturing-leads/WebForm.vue'),
      },

      // Other Features
      {
        path: 'features/view',
        name: 'HelpComment',
        component: () => import('@/pages/help-center/features/View.vue'),
      },
      {
        path: 'features/notification',
        name: 'HelpNotification',
        component: () => import('@/pages/help-center/features/Notification.vue'),
      },
      {
        path: 'features/customization',
        name: 'HelpCustomization',
        component: () => import('@/pages/help-center/features/Customization.vue'),
      },

      // Mobile
      {
        path: 'mobile',
        redirect: '/help-center/mobile/installation',
      },
      {
        path: 'mobile/installation',
        name: 'HelpMobileInstallation',
        component: () => import('@/pages/help-center/mobile/Installation.vue'),
      },
    ],
  },
]

let router = createRouter({
  history: createWebHistory('/crm'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const { isLoggedIn } = sessionStore()
  const { users, isWebsiteUser } = usersStore()
  if (to.name === 'ContactSupport' || to.path.includes('contact-support')) {
    next() 
    return // Stop executing the rest of the function
  }


  if (isLoggedIn && !users.fetched) {
    try {
      await users.promise
    } catch (error) {
      console.error('Error loading users', error)
    }
  }

  if (isLoggedIn && to.name !== 'Not Permitted' && isWebsiteUser()) {
    next({ name: 'Not Permitted' })
  } else if (to.name === 'Home' && isLoggedIn) {
    const { views, getDefaultView } = viewsStore()
    await views.promise

    let defaultView = getDefaultView()
    if (!defaultView) {
      next({ name: 'Leads' })
      return
    }

    let { route_name, type, name, is_standard } = defaultView
    route_name = route_name || 'Leads'

    if (name && !is_standard) {
      next({
        name: route_name,
        params: { viewType: type },
        query: { view: name },
      })
    } else {
      next({ name: route_name, params: { viewType: type } })
    }
  } else if (!isLoggedIn) {
    window.location.href = '/login?redirect-to=/crm'
  } else if (to.matched.length === 0) {
    next({ name: 'Invalid Page' })
  } else if (['Deal', 'Lead'].includes(to.name) && !to.hash) {
    let storageKey = to.name === 'Deal' ? 'lastDealTab' : 'lastLeadTab'
    const activeTab = localStorage.getItem(storageKey) || 'activity'
    const hash = '#' + activeTab
    next({ ...to, hash })
  } else {
    next()
  }
})

export default router