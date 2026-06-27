/**
 * Separate Vite build for order_sync_components.js
 *
 * Produces an IIFE at: order_integration/public/js/order_sync_components.js
 *
 * Uses the frappe-ui lucideIcons plugin to resolve ~icons/lucide/* virtual
 * imports that frappe-ui components depend on internally.
 *
 * Build: yarn build:components
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { lucideIcons } from './node_modules/frappe-ui/vite/lucideIcons.js'

export default defineConfig({
  plugins: [
    vue(),
    ...lucideIcons(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  define: {
    'process.env.NODE_ENV': '"production"',
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
  },
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/order_sync_entry.js'),
      name: 'OrderSyncComponents',
      fileName: () => 'order_sync_components.js',
      formats: ['iife'],
    },
    outDir: path.resolve(__dirname, '../../js'),
    emptyOutDir: false,
    minify: true,
    rollupOptions: {
      output: {
        inlineDynamicImports: true,
      },
    },
  },
})
