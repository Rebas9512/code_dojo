import { useEffect, useState } from 'react'
import Editor, { DiffEditor } from '@monaco-editor/react'
import { api, type StandardAnswer } from '../api'
import { monaco } from '../monaco'
import type { Theme } from '../theme'
import { Markdown } from './Markdown'

const readingOptions: monaco.editor.IStandaloneEditorConstructionOptions = {
  readOnly: true, domReadOnly: true, automaticLayout: true,
  fontFamily: "'JetBrains Mono Variable', 'Noto Sans SC', monospace", fontSize: 13, lineHeight: 21,
  minimap: { enabled: false }, folding: false, glyphMargin: false, lineNumbersMinChars: 2,
  lineDecorationsWidth: 6, renderLineHighlight: 'none', scrollBeyondLastLine: false,
  padding: { top: 8, bottom: 8 }, scrollbar: { alwaysConsumeMouseWheel: false, useShadows: false },
}
const compareOptions: monaco.editor.IStandaloneDiffEditorConstructionOptions = {
  // 左栏常常只有四五百像素宽：不够宽时改为上下行内对比，代码不必折行。
  ...readingOptions, originalEditable: false, renderSideBySide: true, useInlineViewWhenSpaceIsLimited: true,
  renderSideBySideInlineBreakpoint: 700,
  enableSplitViewResizing: false, renderOverviewRuler: false, renderMarginRevertIcon: false,
  renderGutterMenu: false, lineNumbers: 'off', diffWordWrap: 'on',
  originalAriaLabel: '我的代码', modifiedAriaLabel: '标准写法',
}

export default function StandardAnswerView({ id, code, theme }: { id: string; code: string; theme: Theme }) {
  const [answer, setAnswer] = useState<StandardAnswer | null>(null)
  const [error, setError] = useState('')
  const [comparing, setComparing] = useState(false)
  useEffect(() => {
    let current = true
    api.standard(id).then(value => { if (current) setAnswer(value) })
      .catch((err: Error) => { if (current) setError(err.message) })
    return () => { current = false }
  }, [id])
  if (error) return <p className="tone-fail" role="alert">{error}</p>
  if (!answer) return <p className="muted" role="status">正在读取参考答案…</p>

  const language = answer.language === 'sql' ? 'pgsql' : 'python'
  const editorTheme = `dojo-${theme}`
  const lines = answer.code.trimEnd().split('\n').length
  return <div className="standard-answer">
    {answer.has_notes && <Markdown>{answer.notes_md}</Markdown>}
    <section aria-label="标准写法">
      <h2>标准写法</h2>
      <div className="standard-code">
        <Editor height={Math.min(lines, 20) * 21 + 30} value={answer.code} language={language}
          theme={editorTheme} options={{ ...readingOptions, ariaLabel: '标准写法' }} loading={null} />
      </div>
    </section>
    <button className="secondary" aria-expanded={comparing} onClick={() => setComparing(open => !open)}>
      {comparing ? '收起对比' : '和我的代码对比'}
    </button>
    {comparing && <section className="standard-diff" aria-label="代码对比">
      <p className="diff-labels">从我的代码到标准写法：红色是要去掉的，绿色是要加上的</p>
      <DiffEditor height={Math.min(20, Math.max(7, lines, code.split('\n').length)) * 21 + 30}
        original={code} modified={answer.code} language={language} theme={editorTheme} options={compareOptions} loading={null} />
    </section>}
    {answer.advanced_md && <Markdown>{answer.advanced_md}</Markdown>}
  </div>
}
