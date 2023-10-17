import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteSingleFile } from "vite-plugin-singlefile"


const entryPoint = './index_PiniaORM_complex.html'
const sourceFiles = './src_PiniaORM_complex'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    viteSingleFile()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL(sourceFiles, import.meta.url))
    },
    build: {
      rollupOptions: {
        input: {
          app: entryPoint,
        },
      },
    },
    server: {
      open: entryPoint,
    },


  }
})
