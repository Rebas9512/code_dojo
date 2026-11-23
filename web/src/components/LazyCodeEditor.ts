import { lazy } from 'react'

// 看数据作答和数据课无需下载 Monaco。代码题由路由已有的 Suspense 等待编辑器加载。
export const CodeEditor = lazy(() => import('./CodeEditor').then(({ CodeEditor }) => ({ default: CodeEditor })))
