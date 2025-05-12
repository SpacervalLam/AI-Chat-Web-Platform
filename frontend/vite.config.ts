import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': '/src'
    }
  },
  server: {
    host: true,       // 监听所有地址，包括 IPv4/IPv6
    port: 6626,
    open: true,       // 启动时自动打开浏览器
    proxy: {
      '/chat': 'http://localhost:8000',
    },
  },
    css: {
    postcss: './postcss.config.cjs',
  },
})
