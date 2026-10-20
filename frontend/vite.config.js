import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [
    vue(),
    // 使っている Vuetify のコンポーネントだけを import します。
    vuetify({ autoImport: true })
  ],
  base: '/the-my-mind/',
  // compose や GitHub Actions が渡す VUE_APP_BACKEND_BASE_URL を、 import.meta.env から読めるようにします。
  envPrefix: 'VUE_APP_',
  server: {
    host: '0.0.0.0',
    port: 8080,
    strictPort: true
  },
  test: {
    environment: 'happy-dom',
    server: {
      deps: {
        // Vuetify は CSS を import するので、 Vite で変換してから読み込みます。
        inline: ['vuetify']
      }
    }
  }
})
