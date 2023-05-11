import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from "vite-plugin-pwa";


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: "autoUpdate",
      devOptions: {
        enabled: true,
      },
      manifest: {
        name: "Assistant",
        short_name: "my assistant",
        start_url: "/",
        display: "standalone",
        background_color: "#ffffff",
        lang: "en",
        scope: "/",
        theme_color: "#000000",
        description: "An assistant",
        orientation: "portrait",
        categories: ["ai"],
        icons: [
          {
            src: "/assistant.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "/assistant.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "any",
          },
        ],
      },
    }),
  ],
});





