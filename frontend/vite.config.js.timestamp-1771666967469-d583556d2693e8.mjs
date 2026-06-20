// vite.config.js
import { defineConfig } from "file:///mnt/d/frappe/ipshopy-bench/apps/crm/frontend/node_modules/vite/dist/node/index.js";
import vue from "file:///mnt/d/frappe/ipshopy-bench/apps/crm/frontend/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import vueJsx from "file:///mnt/d/frappe/ipshopy-bench/apps/crm/frontend/node_modules/@vitejs/plugin-vue-jsx/dist/index.mjs";
import path from "path";
import { VitePWA } from "file:///mnt/d/frappe/ipshopy-bench/apps/crm/frontend/node_modules/vite-plugin-pwa/dist/index.js";
var __vite_injected_original_dirname = "/mnt/d/frappe/ipshopy-bench/apps/crm/frontend";
var vite_config_default = defineConfig(async ({ mode }) => {
  const isDev = mode === "development";
  const config = {
    plugins: [
      vue(),
      vueJsx(),
      VitePWA({
        registerType: "autoUpdate",
        devOptions: {
          enabled: true
        },
        manifest: {
          display: "standalone",
          name: "Frappe CRM",
          short_name: "Frappe CRM",
          start_url: "/crm",
          description: "Modern & 100% Open-source CRM tool to supercharge your sales operations",
          icons: [
            {
              src: "/assets/crm/manifest/manifest-icon-192.maskable.png",
              sizes: "192x192",
              type: "image/png",
              purpose: "any"
            },
            {
              src: "/assets/crm/manifest/manifest-icon-192.maskable.png",
              sizes: "192x192",
              type: "image/png",
              purpose: "maskable"
            },
            {
              src: "/assets/crm/manifest/manifest-icon-512.maskable.png",
              sizes: "512x512",
              type: "image/png",
              purpose: "any"
            },
            {
              src: "/assets/crm/manifest/manifest-icon-512.maskable.png",
              sizes: "512x512",
              type: "image/png",
              purpose: "maskable"
            }
          ]
        }
      })
    ],
    resolve: {
      alias: {
        "@": path.resolve(__vite_injected_original_dirname, "src")
      }
    },
    optimizeDeps: {
      include: [
        "feather-icons",
        "tailwind.config.js",
        "prosemirror-state",
        "prosemirror-view",
        "lowlight",
        "interactjs"
      ]
    },
    server: {
      fs: {
        allow: [path.resolve(__vite_injected_original_dirname, "..")]
      }
    }
  };
  const frappeui = await importFrappeUIPlugin(isDev, config);
  config.plugins.unshift(
    frappeui({
      frappeProxy: true,
      lucideIcons: true,
      jinjaBootData: true,
      buildConfig: {
        indexHtmlPath: "../crm/www/crm.html",
        emptyOutDir: true,
        sourcemap: true
      }
    })
  );
  return config;
});
async function importFrappeUIPlugin(isDev, config) {
  if (isDev) {
    try {
      const fs = await import("node:fs");
      const localVitePluginPath = path.resolve(__vite_injected_original_dirname, "../frappe-ui/vite");
      if (fs.existsSync(localVitePluginPath)) {
        const module2 = await import("../frappe-ui/vite");
        console.info("Local frappe-ui vite plugin found, using local plugin");
        config.resolve.alias = getAliases(config);
        return module2.default;
      } else {
        console.warn("Local frappe-ui vite plugin not found, using npm package");
      }
    } catch (error) {
      console.warn(
        "Local frappe-ui not found, falling back to npm package:",
        error.message
      );
    }
  }
  const module = await import("file:///mnt/d/frappe/ipshopy-bench/apps/crm/frontend/node_modules/frappe-ui/vite/index.js");
  return module.default;
}
function getAliases(config) {
  return {
    ...config.resolve.alias,
    "frappe-ui/tailwind": path.resolve(
      __vite_injected_original_dirname,
      "../frappe-ui/tailwind/preset.js"
    ),
    "frappe-ui/style.css": path.resolve(
      __vite_injected_original_dirname,
      "../frappe-ui/src/style.css"
    ),
    "frappe-ui/frappe": path.resolve(__vite_injected_original_dirname, "../frappe-ui/frappe/index.js"),
    "frappe-ui": path.resolve(__vite_injected_original_dirname, "../frappe-ui/src/index.ts")
  };
}
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvbW50L2QvZnJhcHBlL2lwc2hvcHktYmVuY2gvYXBwcy9jcm0vZnJvbnRlbmRcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIi9tbnQvZC9mcmFwcGUvaXBzaG9weS1iZW5jaC9hcHBzL2NybS9mcm9udGVuZC92aXRlLmNvbmZpZy5qc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vbW50L2QvZnJhcHBlL2lwc2hvcHktYmVuY2gvYXBwcy9jcm0vZnJvbnRlbmQvdml0ZS5jb25maWcuanNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJ1xuaW1wb3J0IHZ1ZSBmcm9tICdAdml0ZWpzL3BsdWdpbi12dWUnXG5pbXBvcnQgdnVlSnN4IGZyb20gJ0B2aXRlanMvcGx1Z2luLXZ1ZS1qc3gnXG5pbXBvcnQgcGF0aCBmcm9tICdwYXRoJ1xuaW1wb3J0IHsgVml0ZVBXQSB9IGZyb20gJ3ZpdGUtcGx1Z2luLXB3YSdcblxuLy8gaHR0cHM6Ly92aXRlanMuZGV2L2NvbmZpZy9cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyhhc3luYyAoeyBtb2RlIH0pID0+IHtcbiAgY29uc3QgaXNEZXYgPSBtb2RlID09PSAnZGV2ZWxvcG1lbnQnXG4gIGNvbnN0IGNvbmZpZyA9IHtcbiAgICBwbHVnaW5zOiBbXG4gICAgICB2dWUoKSxcbiAgICAgIHZ1ZUpzeCgpLFxuICAgICAgVml0ZVBXQSh7XG4gICAgICAgIHJlZ2lzdGVyVHlwZTogJ2F1dG9VcGRhdGUnLFxuICAgICAgICBkZXZPcHRpb25zOiB7XG4gICAgICAgICAgZW5hYmxlZDogdHJ1ZSxcbiAgICAgICAgfSxcbiAgICAgICAgbWFuaWZlc3Q6IHtcbiAgICAgICAgICBkaXNwbGF5OiAnc3RhbmRhbG9uZScsXG4gICAgICAgICAgbmFtZTogJ0ZyYXBwZSBDUk0nLFxuICAgICAgICAgIHNob3J0X25hbWU6ICdGcmFwcGUgQ1JNJyxcbiAgICAgICAgICBzdGFydF91cmw6ICcvY3JtJyxcbiAgICAgICAgICBkZXNjcmlwdGlvbjpcbiAgICAgICAgICAgICdNb2Rlcm4gJiAxMDAlIE9wZW4tc291cmNlIENSTSB0b29sIHRvIHN1cGVyY2hhcmdlIHlvdXIgc2FsZXMgb3BlcmF0aW9ucycsXG4gICAgICAgICAgaWNvbnM6IFtcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgc3JjOiAnL2Fzc2V0cy9jcm0vbWFuaWZlc3QvbWFuaWZlc3QtaWNvbi0xOTIubWFza2FibGUucG5nJyxcbiAgICAgICAgICAgICAgc2l6ZXM6ICcxOTJ4MTkyJyxcbiAgICAgICAgICAgICAgdHlwZTogJ2ltYWdlL3BuZycsXG4gICAgICAgICAgICAgIHB1cnBvc2U6ICdhbnknLFxuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgc3JjOiAnL2Fzc2V0cy9jcm0vbWFuaWZlc3QvbWFuaWZlc3QtaWNvbi0xOTIubWFza2FibGUucG5nJyxcbiAgICAgICAgICAgICAgc2l6ZXM6ICcxOTJ4MTkyJyxcbiAgICAgICAgICAgICAgdHlwZTogJ2ltYWdlL3BuZycsXG4gICAgICAgICAgICAgIHB1cnBvc2U6ICdtYXNrYWJsZScsXG4gICAgICAgICAgICB9LFxuICAgICAgICAgICAge1xuICAgICAgICAgICAgICBzcmM6ICcvYXNzZXRzL2NybS9tYW5pZmVzdC9tYW5pZmVzdC1pY29uLTUxMi5tYXNrYWJsZS5wbmcnLFxuICAgICAgICAgICAgICBzaXplczogJzUxMng1MTInLFxuICAgICAgICAgICAgICB0eXBlOiAnaW1hZ2UvcG5nJyxcbiAgICAgICAgICAgICAgcHVycG9zZTogJ2FueScsXG4gICAgICAgICAgICB9LFxuICAgICAgICAgICAge1xuICAgICAgICAgICAgICBzcmM6ICcvYXNzZXRzL2NybS9tYW5pZmVzdC9tYW5pZmVzdC1pY29uLTUxMi5tYXNrYWJsZS5wbmcnLFxuICAgICAgICAgICAgICBzaXplczogJzUxMng1MTInLFxuICAgICAgICAgICAgICB0eXBlOiAnaW1hZ2UvcG5nJyxcbiAgICAgICAgICAgICAgcHVycG9zZTogJ21hc2thYmxlJyxcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgXSxcbiAgICAgICAgfSxcbiAgICAgIH0pLFxuICAgIF0sXG4gICAgcmVzb2x2ZToge1xuICAgICAgYWxpYXM6IHtcbiAgICAgICAgJ0AnOiBwYXRoLnJlc29sdmUoX19kaXJuYW1lLCAnc3JjJyksXG4gICAgICB9LFxuICAgIH0sXG4gICAgb3B0aW1pemVEZXBzOiB7XG4gICAgICBpbmNsdWRlOiBbXG4gICAgICAgICdmZWF0aGVyLWljb25zJyxcbiAgICAgICAgJ3RhaWx3aW5kLmNvbmZpZy5qcycsXG4gICAgICAgICdwcm9zZW1pcnJvci1zdGF0ZScsXG4gICAgICAgICdwcm9zZW1pcnJvci12aWV3JyxcbiAgICAgICAgJ2xvd2xpZ2h0JyxcbiAgICAgICAgJ2ludGVyYWN0anMnLFxuICAgICAgXSxcbiAgICB9LFxuICAgIHNlcnZlcjoge1xuICAgICAgZnM6IHtcbiAgICAgICAgYWxsb3c6IFtwYXRoLnJlc29sdmUoX19kaXJuYW1lLCAnLi4nKV0sXG4gICAgICB9LFxuICAgIH0sXG4gIH1cblxuICBjb25zdCBmcmFwcGV1aSA9IGF3YWl0IGltcG9ydEZyYXBwZVVJUGx1Z2luKGlzRGV2LCBjb25maWcpXG4gIGNvbmZpZy5wbHVnaW5zLnVuc2hpZnQoXG4gICAgZnJhcHBldWkoe1xuICAgICAgZnJhcHBlUHJveHk6IHRydWUsXG4gICAgICBsdWNpZGVJY29uczogdHJ1ZSxcbiAgICAgIGppbmphQm9vdERhdGE6IHRydWUsXG4gICAgICBidWlsZENvbmZpZzoge1xuICAgICAgICBpbmRleEh0bWxQYXRoOiAnLi4vY3JtL3d3dy9jcm0uaHRtbCcsXG4gICAgICAgIGVtcHR5T3V0RGlyOiB0cnVlLFxuICAgICAgICBzb3VyY2VtYXA6IHRydWUsXG4gICAgICB9LFxuICAgIH0pLFxuICApXG5cbiAgcmV0dXJuIGNvbmZpZ1xufSlcblxuYXN5bmMgZnVuY3Rpb24gaW1wb3J0RnJhcHBlVUlQbHVnaW4oaXNEZXYsIGNvbmZpZykge1xuICBpZiAoaXNEZXYpIHtcbiAgICB0cnkge1xuICAgICAgLy8gQ2hlY2sgaWYgbG9jYWwgZnJhcHBlLXVpIGhhcyB0aGUgdml0ZSBwbHVnaW4gZmlsZVxuICAgICAgY29uc3QgZnMgPSBhd2FpdCBpbXBvcnQoJ25vZGU6ZnMnKVxuICAgICAgY29uc3QgbG9jYWxWaXRlUGx1Z2luUGF0aCA9IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICcuLi9mcmFwcGUtdWkvdml0ZScpXG5cbiAgICAgIGlmIChmcy5leGlzdHNTeW5jKGxvY2FsVml0ZVBsdWdpblBhdGgpKSB7XG4gICAgICAgIGNvbnN0IG1vZHVsZSA9IGF3YWl0IGltcG9ydCgnLi4vZnJhcHBlLXVpL3ZpdGUnKVxuICAgICAgICBjb25zb2xlLmluZm8oJ0xvY2FsIGZyYXBwZS11aSB2aXRlIHBsdWdpbiBmb3VuZCwgdXNpbmcgbG9jYWwgcGx1Z2luJylcbiAgICAgICAgY29uZmlnLnJlc29sdmUuYWxpYXMgPSBnZXRBbGlhc2VzKGNvbmZpZylcbiAgICAgICAgcmV0dXJuIG1vZHVsZS5kZWZhdWx0XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBjb25zb2xlLndhcm4oJ0xvY2FsIGZyYXBwZS11aSB2aXRlIHBsdWdpbiBub3QgZm91bmQsIHVzaW5nIG5wbSBwYWNrYWdlJylcbiAgICAgIH1cbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgY29uc29sZS53YXJuKFxuICAgICAgICAnTG9jYWwgZnJhcHBlLXVpIG5vdCBmb3VuZCwgZmFsbGluZyBiYWNrIHRvIG5wbSBwYWNrYWdlOicsXG4gICAgICAgIGVycm9yLm1lc3NhZ2UsXG4gICAgICApXG4gICAgfVxuICB9XG4gIC8vIEZhbGwgYmFjayB0byBucG0gcGFja2FnZSBpZiBsb2NhbCBpbXBvcnQgZmFpbHNcbiAgY29uc3QgbW9kdWxlID0gYXdhaXQgaW1wb3J0KCdmcmFwcGUtdWkvdml0ZScpXG4gIHJldHVybiBtb2R1bGUuZGVmYXVsdFxufVxuXG5mdW5jdGlvbiBnZXRBbGlhc2VzKGNvbmZpZykge1xuICByZXR1cm4ge1xuICAgIC4uLmNvbmZpZy5yZXNvbHZlLmFsaWFzLFxuICAgICdmcmFwcGUtdWkvdGFpbHdpbmQnOiBwYXRoLnJlc29sdmUoXG4gICAgICBfX2Rpcm5hbWUsXG4gICAgICAnLi4vZnJhcHBlLXVpL3RhaWx3aW5kL3ByZXNldC5qcycsXG4gICAgKSxcbiAgICAnZnJhcHBlLXVpL3N0eWxlLmNzcyc6IHBhdGgucmVzb2x2ZShcbiAgICAgIF9fZGlybmFtZSxcbiAgICAgICcuLi9mcmFwcGUtdWkvc3JjL3N0eWxlLmNzcycsXG4gICAgKSxcbiAgICAnZnJhcHBlLXVpL2ZyYXBwZSc6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICcuLi9mcmFwcGUtdWkvZnJhcHBlL2luZGV4LmpzJyksXG4gICAgJ2ZyYXBwZS11aSc6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICcuLi9mcmFwcGUtdWkvc3JjL2luZGV4LnRzJyksXG4gIH1cbn1cbiJdLAogICJtYXBwaW5ncyI6ICI7QUFBeVQsU0FBUyxvQkFBb0I7QUFDdFYsT0FBTyxTQUFTO0FBQ2hCLE9BQU8sWUFBWTtBQUNuQixPQUFPLFVBQVU7QUFDakIsU0FBUyxlQUFlO0FBSnhCLElBQU0sbUNBQW1DO0FBT3pDLElBQU8sc0JBQVEsYUFBYSxPQUFPLEVBQUUsS0FBSyxNQUFNO0FBQzlDLFFBQU0sUUFBUSxTQUFTO0FBQ3ZCLFFBQU0sU0FBUztBQUFBLElBQ2IsU0FBUztBQUFBLE1BQ1AsSUFBSTtBQUFBLE1BQ0osT0FBTztBQUFBLE1BQ1AsUUFBUTtBQUFBLFFBQ04sY0FBYztBQUFBLFFBQ2QsWUFBWTtBQUFBLFVBQ1YsU0FBUztBQUFB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
