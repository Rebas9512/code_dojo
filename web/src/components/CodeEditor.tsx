import { forwardRef, useEffect, useImperativeHandle, useRef } from 'react'
import Editor, { type OnMount } from '@monaco-editor/react'
import { monaco } from '../monaco'
import type { Theme } from '../theme'

type EditorOptions = monaco.editor.IStandaloneEditorConstructionOptions

// 裸写模式：关掉一切"替你写"的功能，只保留按上一行缩进
const BARE: EditorOptions = {
  quickSuggestions: false,
  suggestOnTriggerCharacters: false,
  wordBasedSuggestions: 'off',
  parameterHints: { enabled: false },
  autoClosingBrackets: 'never',
  autoClosingQuotes: 'never',
  autoClosingOvertype: 'never',
  autoSurround: 'never',
  hover: { enabled: 'off' },
  snippetSuggestions: 'none',
  inlineSuggest: { enabled: false },
  tabCompletion: 'off',
  acceptSuggestionOnEnter: 'off',
  autoIndent: 'keep',
}

const ASSISTED: EditorOptions = {
  quickSuggestions: true,
  suggestOnTriggerCharacters: true,
  wordBasedSuggestions: 'currentDocument',
  parameterHints: { enabled: true },
  autoClosingBrackets: 'languageDefined',
  autoClosingQuotes: 'languageDefined',
  autoClosingOvertype: 'auto',
  autoSurround: 'languageDefined',
  hover: { enabled: 'on' },
  snippetSuggestions: 'inline',
  acceptSuggestionOnEnter: 'on',
  autoIndent: 'full',
}

const BASE: EditorOptions = {
  fontFamily: "'JetBrains Mono Variable', 'JetBrains Mono', monospace",
  fontSize: 15,
  lineHeight: 24,
  fontLigatures: false,
  minimap: { enabled: false },
  scrollBeyondLastLine: false,
  renderLineHighlight: 'line',
  tabSize: 4,
  insertSpaces: true,
  detectIndentation: false,
  padding: { top: 16, bottom: 16 },
  glyphMargin: false,
  folding: false,
  lineNumbersMinChars: 3,
  lineDecorationsWidth: 12,
  overviewRulerLanes: 0,
  hideCursorInOverviewRuler: true,
  smoothScrolling: false,
  cursorBlinking: 'solid',
  cursorSmoothCaretAnimation: 'off',
  scrollbar: { verticalScrollbarSize: 10, horizontalScrollbarSize: 10, useShadows: false },
  automaticLayout: true,
  contextmenu: false,
}

interface Props {
  value: string
  onChange: (v: string) => void
  language: 'python' | 'pgsql'
  theme: Theme
  bare: boolean
  readOnly?: boolean
  onRun?: () => void
  onSubmit?: () => void
  /** 紧凑模式：课里的小示例用，字号小、不抢焦点 */
  compact?: boolean
}

const COMPACT: EditorOptions = {
  fontSize: 14,
  lineHeight: 22,
  padding: { top: 8, bottom: 8 },
  lineNumbersMinChars: 2,
  scrollbar: { vertical: 'hidden', horizontal: 'auto', alwaysConsumeMouseWheel: false, useShadows: false },
}

export interface CodeEditorHandle {
  /** 把当前代码里唯一出现的 oldText 换成 newText（oldText 为空则接在末尾），可以 Ctrl+Z 撤销，并标出 AI 写入的行。找不到或不唯一返回 false。 */
  applyEdit(oldText: string, newText: string): boolean
}

export const CodeEditor = forwardRef<CodeEditorHandle, Props>(function CodeEditor(
  { value, onChange, language, theme, bare, readOnly, onRun, onSubmit, compact = false },
  ref,
) {
  // 快捷键回调放进 ref：Monaco 的命令只在挂载时注册一次
  const handlers = useRef({ onRun, onSubmit })
  handlers.current = { onRun, onSubmit }
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null)
  const aiMarks = useRef<monaco.editor.IEditorDecorationsCollection | null>(null)

  useImperativeHandle(ref, () => ({
    applyEdit(oldText, newText) {
      const editor = editorRef.current
      const model = editor?.getModel()
      if (!editor || !model) return false
      const text = model.getValue()
      let at: number
      let len = 0
      let insert = newText
      if (!oldText) {
        // old 为空：接在末尾追加
        at = text.length
        if (text && !text.endsWith('\n')) insert = '\n' + newText
      } else {
        at = text.indexOf(oldText)
        len = oldText.length
        if (at < 0 || text.indexOf(oldText, at + 1) >= 0) return false
      }
      const start = model.getPositionAt(at)
      const end = model.getPositionAt(at + len)
      editor.pushUndoStop()
      editor.executeEdits('ai-tutor', [
        { range: new monaco.Range(start.lineNumber, start.column, end.lineNumber, end.column), text: insert },
      ])
      editor.pushUndoStop()
      const newEnd = model.getPositionAt(at + insert.length)
      const firstLine = insert.startsWith('\n') ? start.lineNumber + 1 : start.lineNumber
      aiMarks.current ??= editor.createDecorationsCollection()
      aiMarks.current.append([
        {
          range: new monaco.Range(firstLine, 1, newEnd.lineNumber, 1),
          options: { isWholeLine: true, className: 'ai-line', linesDecorationsClassName: 'ai-line-gutter' },
        },
      ])
      editor.revealLineInCenterIfOutsideViewport(start.lineNumber)
      editor.focus()
      return true
    },
  }))

  const onMount: OnMount = (editor) => {
    editorRef.current = editor
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => handlers.current.onRun?.())
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter, () =>
      handlers.current.onSubmit?.(),
    )
    if (!compact) editor.focus()
  }

  useEffect(() => {
    editorRef.current?.updateOptions({ ...(bare ? BARE : ASSISTED), readOnly: !!readOnly })
  }, [bare, readOnly])

  return (
    <Editor
      value={value}
      onChange={(v) => onChange(v ?? '')}
      language={language}
      theme={`dojo-${theme}`}
      options={{ ...BASE, ...(compact ? COMPACT : {}), ...(bare ? BARE : ASSISTED), readOnly: !!readOnly }}
      onMount={onMount}
      loading={null}
    />
  )
})
