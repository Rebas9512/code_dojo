import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// 开发时 /api 转发到本机 FastAPI（cd server && uv run uvicorn app.main:app --port 8000）；
// 用 CODE_DOJO_API 可以指向别的后端（比如测试用的样例题库实例）
const api = process.env.CODE_DOJO_API ?? 'http://127.0.0.1:8000'

export default defineConfig({
  worker: { format: 'es' },
  optimizeDeps: { exclude: ['@electric-sql/pglite'] },
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    port: 5173,
    proxy: { '/api': api },
  },
})
