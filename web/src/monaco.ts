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

// 颜色和 styles.css 的 OKLCH 色板一一对应（换算成十六进制，Monaco 只认这个）
const palette = {
  dark: {
    bg: '#191714', text: '#e5e1da', faint: '#6c6863', line: '#33302c', sel: '#3b342a', accent: '#e8b45e',
    comment: '#7e8275', kw: '#e5b28a', str: '#9dc494', num: '#f1aa92', fn: '#dacda9',
  },
  light: {
    bg: '#f9f6f2', text: '#2a2520', faint: '#8a8580', line: '#dbd7d2', sel: '#e9dcc8', accent: '#b46d10',
    comment: '#6f7461', kw: '#944e21', str: '#3b723e', num: '#a24b36', fn: '#4d4122',
  },
}

for (const [name, c] of Object.entries(palette)) {
  const strip = (hex: string) => hex.slice(1)
  monaco.editor.defineTheme(`dojo-${name}`, {
    base: name === 'dark' ? 'vs-dark' : 'vs',
    inherit: true,
    rules: [
      { token: '', foreground: strip(c.text) },
      { token: 'comment', foreground: strip(c.comment), fontStyle: 'italic' },
      { token: 'keyword', foreground: strip(c.kw) },
      { token: 'string', foreground: strip(c.str) },
      { token: 'number', foreground: strip(c.num) },
      { token: 'identifier', foreground: strip(c.text) },
      { token: 'type', foreground: strip(c.fn) },
      { token: 'predefined', foreground: strip(c.fn) },
      { token: 'operator', foreground: strip(c.text) },
    ],
    colors: {
      'editor.background': c.bg,
      'editor.foreground': c.text,
      'editorLineNumber.foreground': c.faint,
      'editorLineNumber.activeForeground': c.text,
      'editor.lineHighlightBackground': c.bg,
      'editor.lineHighlightBorder': c.line,
      'editor.selectionBackground': c.sel,
      'editorCursor.foreground': c.accent,
      'editorIndentGuide.background1': c.line,
      'editorIndentGuide.activeBackground1': c.faint,
      'editorWhitespace.foreground': c.line,
      'editorWidget.background': c.bg,
      'editorWidget.border': c.line,
      'scrollbarSlider.background': `${c.line}aa`,
      'scrollbarSlider.hoverBackground': c.line,
    },
  })
}

export { monaco }
