import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// 开发时 /api 转发到本机 FastAPI（cd server && uv run uvicorn app.main:app --port 8000）；
// 用 CODE_DOJO_API 可以指向别的后端（比如测试用的样例题库实例）
const api = process.env.CODE_DOJO_API ?? 'http://127.0.0.1:8000'

export default defineConfig({
  worker: { format: 'es' },
  optimizeDeps: { exclude: ['@electric-sql/pglite'] },
  build: {
    // 分片字体始终独立缓存，只请求页面实际用到的字形。
    assetsInlineLimit: path => /\.woff2?$/.test(path) ? false : undefined,
  },
  plugins: [react(), {
    name: 'noto-family-name',
    enforce: 'pre',
    transform(css, id) {
      // Fontsource 在可变字体族名后加 Variable，站内字体栈统一使用正式族名。
      if (id.endsWith('/@fontsource-variable/noto-sans-sc/index.css')) {
        return css.replaceAll("'Noto Sans SC Variable'", "'Noto Sans SC'")
      }
    },
  }],
  server: {
    host: '127.0.0.1',
    port: 5173,
    proxy: { '/api': api },
  },
})
