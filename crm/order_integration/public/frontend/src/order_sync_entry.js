/**
 * Entry point for the order_sync_components IIFE bundle.
 *
 * Bundles Vue + frappe-ui + OrderSyncing components into one self-contained
 * IIFE. The lucideIcons vite plugin resolves all ~icons/lucide/* imports.
 *
 * Exposes on window:
 *   window.__OrderSyncSourcePage  — Vue component definition
 *   window.__OrderSyncCreateApp   — factory that creates a mounted-ready app
 */
import { createApp, h } from 'vue'
import {
  FrappeUI,
  Button,
  Badge,
  Switch,
  Dropdown,
  Tabs,
  FormControl,
  FeatherIcon,
  Input,
  ErrorMessage,
} from 'frappe-ui'
import OrderSyncSourcePage from './OrderSyncing/OrderSyncSourcePage.vue'
import APIDataViewer from './OrderSyncing/APIDataViewer.vue'

window.__OrderSyncSourcePage = OrderSyncSourcePage
window.__APIDataViewer = APIDataViewer

window.__OrderSyncCreateApp = function (component) {
  const app = createApp({ render: () => h(component) })
  app.use(FrappeUI)
  // Register commonly used frappe-ui components explicitly as globals
  app.component('Button', Button)
  app.component('Badge', Badge)
  app.component('Switch', Switch)
  app.component('Dropdown', Dropdown)
  app.component('Tabs', Tabs)
  app.component('FormControl', FormControl)
  app.component('FeatherIcon', FeatherIcon)
  app.component('Input', Input)
  app.component('ErrorMessage', ErrorMessage)
  return app
}
