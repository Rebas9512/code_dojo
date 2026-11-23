import { lazy, Suspense, type ReactNode } from 'react'
import type { JudgeResult, Mode } from '../api'
import type { TablePreview } from '../sql/client'
import { Icon, Separator, type WorkbenchLayout } from './WorkbenchLayout'
import { ResultPanel } from './ResultPanel'

const SqlTableView = lazy(() => import('../sql/SqlTableView'))
export type PanelTab = '测试结果' | '输出' | '问题'
export type ExampleOutput = { stdout: string; error?: string | null; table?: TablePreview }
export type Attempt = { r: JudgeResult; kind: 'run' | 'submit'; source: string }

export function diagnostics(attempt: Attempt | null, error: string | null) {
  const messages = new Set<string>()
  if (error) messages.add(error)
  if (attempt?.r.error) messages.add(attempt.r.error)
  for (const c of attempt?.r.cases ?? []) if (c.error) messages.add(c.error)
  return [...messages]
}

function Trace({ message, source, sql, jump }: {
  message: string; source: string; sql: boolean; jump?: (line: number) => void
}) {
  return <pre className="trace">{message.split('\n').map((text, i) => {
    const match = text.match(/^(?:第\s*(\d+)\s*行(?:语法错误|，在|：)|\s*File "[^"]*user\.py", line (\d+))/)
    const offset = sql && text.match(/第\s*(\d+)\s*个字符/)
    const line = match ? Number(match[1] || match[2]) : offset ? source.slice(0, Number(offset[1]) - 1).split('\n').length : 0
    return <span key={i}>{line && jump ? <button title={'跳到第 ' + line + ' 行'} onClick={() => jump(line)}>{text}</button> : text}{'\n'}</span>
  })}</pre>
}

export function WorkbenchPanel({ layout, tab, setTab, attempt, problems, sql, mode, names, output, jump, busy }: {
  layout: WorkbenchLayout; tab: PanelTab; setTab: (t: PanelTab) => void; attempt: Attempt | null
  problems: string[]; sql: boolean; mode: Mode; names: string[]; output: ExampleOutput | null
  jump?: (line: number) => void; busy: boolean
}) {
  let body: ReactNode
  if (tab === '测试结果') {
    body = busy ? <p className="panel-empty">正在判题…</p> : attempt
      ? <ResultPanel result={attempt.r} kind={attempt.kind} sql={sql} mode={mode} paramNames={names} />
      : <p className="panel-empty">{problems[0] || '运行或提交后查看测试结果。'}</p>
  } else if (tab === '问题') {
    body = problems.length ? problems.map((msg, i) => <Trace key={i} message={msg} source={attempt?.source || ''} sql={sql} jump={jump} />)
      : <p className="panel-empty">没有报错。</p>
  } else {
    const logs = attempt?.r.cases.flatMap((c, i) => {
      const text = c.stdout || (mode === 'stdio' && typeof c.actual === 'string' ? c.actual : '')
      return text ? [<div key={i}><small>用例 {i + 1}</small><pre>{text}</pre></div>] : []
    }) ?? []
    body = <div className="panel-output">{logs}
      {output && <div><small>课 · 示例</small>{output.table
        ? <Suspense fallback={null}><SqlTableView label="运行结果" table={output.table} /></Suspense>
        : <pre>{[output.stdout, output.error].filter(Boolean).join('\n') || '（没有输出）'}</pre>}</div>}
      {!logs.length && !output && <p className="panel-empty">暂无输出。</p>}
    </div>
  }
  return <section className="wb-panel" aria-label="底部面板">
    <Separator label="调整底部面板高度" side="bottom" size={layout.bottom} />
    <header className="panel-tabs">{(['测试结果', '输出', '问题'] as const).map(name =>
      <button key={name} aria-pressed={name === tab} onClick={() => setTab(name)}>
        {name}{name === '问题' && problems.length > 0 && <small>{problems.length}</small>}
      </button>)}
      <button className="icon-btn" title="收起底部面板（Ctrl+J）" onClick={() => layout.setPanel(false)}><Icon name="close" /></button>
    </header><div className="panel-body">{body}</div>
  </section>
}
