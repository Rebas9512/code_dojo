import { createRoot } from 'react-dom/client'
import '@fontsource-variable/noto-sans-sc'
import '@fontsource-variable/jetbrains-mono'
import './styles.css'
import { App } from './App'

// 不用 StrictMode：开发时它会让每个副作用跑两遍，切题时题目、对话和附加题都要重复请求。
createRoot(document.getElementById('root')!).render(<App />)

if (document.querySelector('meta[name="code-dojo-desktop"]')) void import('./sql/desktop')
