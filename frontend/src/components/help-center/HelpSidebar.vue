

<template>
  <div class="help-sidebar-content">
    <nav>
      <!-- EXPANDED MODE -->
      <ul v-if="!collapsed">
        <li v-for="section in filteredSections" :key="section.name">
          <div
            class="section-title"
            :class="{ active: isSectionActive(section) }"
            @click.prevent="toggleSection(section.name)"
          >
            <div class="section-header">
              <FeatherIcon
                :name="
                  openSection === section.name
                    ? 'chevron-down'
                    : 'chevron-right'
                "
                class="arrow"
              />
              <span>{{ section.name }}</span>
            </div>
          </div>
          <ul v-show="search || openSection === section.name">
            <li v-for="article in section.children" :key="article.path">
              <router-link
                :to="article.path"
                class="sidebar-link"
                :class="{ 'router-link-active': route.path === article.path }"
              >
                <FeatherIcon :name="article.icon" class="icon" />
                <span>{{ article.name }}</span>
              </router-link>
            </li>
          </ul>
        </li>
      </ul>

      <!-- COLLAPSED MODE: one icon per section -->
      <ul v-else class="collapsed-menu">
        <li v-for="section in sections" :key="section.name">
          <div
            class="sidebar-link collapsed-link"
            :class="{ 'router-link-active': isSectionActive(section) }"
            :title="section.name"
            @click="handleCollapsedClick(section)"
          >
            <FeatherIcon :name="section.children[0].icon" class="icon" />
          </div>
        </li>
      </ul>

      <p v-if="!collapsed && filteredSections.length === 0" class="no-results">
        No articles found
      </p>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const emit = defineEmits(['update:collapsed'])
const props = defineProps({
  search: { type: String, default: '' },
  collapsed: Boolean,
})
function toggleSection(sectionName) {
  // Toggle open/close
  openSection.value = openSection.value === sectionName ? null : sectionName
}
const openSection = ref(null)

const sections = [
  {
    name: 'Introduction',
    children: [
      { name: 'Introduction', path: '/help-center/introduction', icon: 'book' },
      { name: 'Setting up', path: '/help-center/setting-up', icon: 'settings' },
    ],
  },
  {
    name: 'Settings',
    children: [
      { name: 'Settings Overview',path: '/help-center/settings', icon: 'sliders'},
      { name: 'Profile', path: '/help-center/settings/profile', icon: 'user' },
      { name: 'Customization', path: '/help-center/settings/home-actions',icon: 'home'},
      { name: 'Integrations', path: '/help-center/settings/integrations', icon: 'link'},
      { name: 'System Configuration', path: '/help-center/settings/system-configuration', icon: 'settings'},
      {  name: 'User Management', path: '/help-center/settings/user-management',icon: 'users'},
      {name: 'Email Settings', path: '/help-center/settings/email-settings', icon: 'mail'},
      {name: 'Automation & Rules', path: '/help-center/settings/automation-rules', icon: 'zap'},
    ],
  },
 {
    name: 'Masters',
    children: [
      { name: 'Leads', path: '/help-center/masters/lead', icon: 'user-check' },
      { name: 'Deals', path: '/help-center/masters/deal', icon: 'briefcase' },
      { name: 'Contacts', path: '/help-center/masters/contact', icon: 'users' },
      { name: 'Organizations', path: '/help-center/masters/organization',icon: 'briefcase'},
      { name: 'Notes', path: '/help-center/masters/note', icon: 'file-text' },
      { name: 'Tasks', path: '/help-center/masters/task',icon: 'check-square'},
      {  name: 'Calendar',  path: '/help-center/masters/calendar',icon: 'calendar'},
      {name: 'Call Logs',path: '/help-center/masters/call-log',icon: 'phone'},
      {name: 'Lead History',path: '/help-center/masters/leadhistory',icon: 'clock'},
    ],
  },

  {
    name: 'Capturing Leads',
    children: [
      { name: 'Web Form',  path: '/help-center/capturing-leads/web-form', icon: 'globe'},
      { name: 'Custom Scripts', path: '/help-center/capturing-leads/custom-scripts',icon: 'code'},
    ],
  },
  {
    name: 'Other Features',
    children: [
    { name: 'View',  path: '/help-center/features/view', icon: 'eye'},
    { name: 'Customization', path: '/help-center/features/customization',icon: 'edit-3'},
    { name: 'Notification', path: '/help-center/features/notification', icon: 'bell'},
    ],
  },
  {
    name: 'IP CRM Mobile',
    children: [
      {
        name: 'Mobile App Installation',
        path: '/help-center/mobile/installation',
        icon: 'smartphone',
      },
    ],
  },
]

function handleCollapsedClick(section) {
  const active = getActiveSection(route.path)

  emit('update:collapsed', false)

  if (active && active.name === section.name) {
   
    openSection.value = active.name
  } else {
   
    openSection.value = section.name
    router.push(section.children[0].path)
  }
}

function getActiveSection(path) {
  return sections.find((s) => s.children.some((c) => c.path === path)) || null
}

// Keep active section always open on route change
watch(
  () => route.path,
  (path) => {
    const active = getActiveSection(path)
    if (active) openSection.value = active.name
  },
  { immediate: true },
)

function isSectionActive(section) {
  return section?.children.some((child) => child.path === route.path)
}

const filteredSections = computed(() => {
  if (!props.search) return sections
  const query = props.search.toLowerCase()
  return sections
    .map((section) => {
      const matchedChildren = section.children.filter((a) =>
        a.name.toLowerCase().includes(query),
      )
      if (
        section.name.toLowerCase().includes(query) ||
        matchedChildren.length > 0
      ) {
        return {
          ...section,
          children: matchedChildren.length ? matchedChildren : section.children,
        }
      }
      return null
    })
    .filter(Boolean)
})
</script>

<style scoped>
.help-sidebar-content ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 20px;
  font-size: 13px;
  color: #374151;
  text-decoration: none;
  border-left: 3px solid transparent;
  transition: all 0.2s ease;
}
.sidebar-link:hover {
  background: #eef2ff;
}
.router-link-active {
  background: #eef2ff;
  border-left: 3px solid #f074dc;
  font-weight: 500;
}
.router-link-active .icon {
  color: #f074dc;
}
.icon {
  width: 18px;
  height: 18px;
  color: #6b7280;
}
.section-title {
  padding: 10px 20px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}
.section-title:hover {
  background: #f3f4f6;
}
.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
}
.section-title.active {
  background: #eef2ff;
  border-left: 3px solid #f074dc;
}
.section-title.active .arrow {
  color: #f074dc;
}
.arrow {
  width: 14px;
  height: 14px;
}
.help-sidebar-content ul ul .sidebar-link {
  padding-left: 40px;
}
.help-sidebar-content ul ul {
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.collapsed-menu {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding-top: 10px;
  width: 100%; 
}
.collapsed-link {
  width: 100%;
  height: 40px;
  display: flex; 
  align-items: center; 
  justify-content: center;
  cursor: pointer; 
  border-radius: 10px;
}
.collapsed-link:hover {
  background: #eef2ff;
}
.collapsed-link.router-link-active {
  background: #eef2ff;
  border-left: none !important;
}
.collapsed-link.router-link-active .icon {
  color: #f074dc;
}
.no-results {
  padding: 10px;
  font-size: 13px;
  color: #9ca3af;
}
.help-sidebar-content {
  pointer-events: auto; 
  width: 100%;
}
</style>