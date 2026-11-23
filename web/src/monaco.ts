// Monaco 本地打包（不走 CDN）：只引入核心 API、编辑器功能、Python 和 PostgreSQL 两种语言。
import * as monaco from 'monaco-editor/editor'
import 'monaco-editor/features/register.all'
import 'monaco-editor/languages/definitions/python/register'
import 'monaco-editor/languages/definitions/pgsql/register'
import EditorWorker from 'monaco-editor/editor/editor.worker?worker'
import { loader } from '@monaco-editor/react'

;(globalThis as unknown as { MonacoEnvironment: unknown }).MonacoEnvironment = {
  getWorker: () => new EditorWorker(),
}
loader.config({ monaco })

// 保留 Monaco 的语言着色，只让编辑区底色与工作区一致。
monaco.editor.defineTheme('dojo-dark', {
  base: 'vs-dark', inherit: true, rules: [], colors: { 'editor.background': '#1f1f1f' },
})
monaco.editor.defineTheme('dojo-light', {
  base: 'vs', inherit: true, rules: [], colors: { 'editor.background': '#ffffff' },
})

export { monaco }
