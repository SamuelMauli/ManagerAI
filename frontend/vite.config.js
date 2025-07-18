import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, 
    port: 5173,
    watch: {
      usePolling: true,
    },
  },
  // ---- END OF FIX ----
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})