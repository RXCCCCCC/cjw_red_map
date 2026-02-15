import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import cesium from 'vite-plugin-cesium'
import Components from 'unplugin-vue-components/vite'
import { VantResolver } from '@vant/auto-import-resolver'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [
    vue(),
    cesium(),
    Components({
      resolvers: [VantResolver()],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@zip.js/zip.js/lib/zip-no-worker.js': '@zip.js/zip.js',
    },
  },
  optimizeDeps: {
    exclude: ['@cesium/engine'],
    esbuildOptions: {
      supported: {
        'top-level-await': true,
      },
    },
    include: [
      'mersenne-twister', 
      'urijs', 
      'grapheme-splitter',
      'pako',
      'protobufjs/minimal',
      'bitmap-sdf',
      'earcut',
      'lerc',
    ],
  },
  build: {
    commonjsOptions: {
      transformMixedEsModules: true,
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/tiles': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/uploads': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/recorder': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    },
  },
})
