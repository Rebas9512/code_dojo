import { lazy, Suspense, type ReactNode, useEffect, useState } from 'react'
import { api, type LessonSection, type LessonStep, type PlaygroundResult } from '../api'
import type { Theme } from '../theme'
import { CodeEditor } from './LazyCodeEditor'
import { InspectData } from './InspectData'
import { Markdown } from './Markdown'

import type { ExampleOutput } from './WorkbenchPanel'
import type { TablePreview } from '../sql/client'
const SqlTableView = lazy(() => import('../sql/SqlTableView'))

/** 示例代码：可以改、可以运行，只看输出不判对错。 */
function ExampleStep({ step, theme, problemId, runStatus, onOutput }: { problemId: string; step: Extract<LessonStep, { code: string }>; theme: Theme; runStatus?: ReactNode; onOutput: (out: ExampleOutput) => void }) {
  const [code, setCode] = useState(step.code)
  const [out, setOut] = useState<PlaygroundResult | null>(null)
  const [running, setRunning] = useState(false)
  const [table, setTable] = useState<TablePreview | null>(null)
  const [preparing, setPreparing] = useState(false)
  const isSql = !!step.db
  const run = async () => {
    if (running) return
    setRunning(true)
    try {
      setTable(null)
      setOut(null)
      if (isSql) {
        setPreparing(true)
        const client = await import('../sql/client')
        await client.prepare()
        setPreparing(false)
        const { actual } = await client.query({ setup: step.setup!, sql: code })
        setTable(actual)
        onOutput({ table: actual, stdout: '' })
      } else {
        const result = await api.playground(code, step.stdin ?? '', problemId)
        setOut(result)
        onOutput(result)
      }
    } catch (e) {
      onOutput({ stdout: '', error: (e as Error).message })
      setOut({ status: 'system_error', stdout: '', error: (e as Error).message, time_ms: 0 })
    } finally {
      setPreparing(false)
      setRunning(false)
    }
  }
  const lines = code.split('\n').length
  return (
    <div className="lesson-example">
      <div className="example-editor" style={{ height: Math.min(Math.max(lines, 2), 18) * 22 + 24 }}>
        <CodeEditor
          value={code}
          onChange={setCode}
          language={isSql ? 'pgsql' : 'python'}
          theme={theme}
          bare={false}
          onRun={run}
          compact
        />
      </div>
      <div className="example-actions">
        {running && runStatus}
        {preparing && <span className="faint" role="status">正在准备数据库…</span>}
        <button className="secondary" onClick={run} disabled={running} title="运行（光标在示例里时 Ctrl+Enter）">
          {running ? '运行中' : '运行'}
        </button>
        {code !== step.code && (
          <button className="ghost" disabled={running} onClick={() => {
              setCode(step.code)
              setTable(null)
              setOut(null)
            }}>
            恢复示例
          </button>
        )}
      </div>
      {table && <Suspense fallback={null}><SqlTableView table={table} label="运行结果" /></Suspense>}
      {out && (
        <pre className={`io example-output ${out.status === 'ok' ? '' : 'tone-fail'}`}>
          {out.stdout}
          {out.error ? (out.stdout ? '\n' : '') + out.error : ''}
          {!out.stdout && !out.error ? '（没有输出）' : ''}
        </pre>
      )}
      {step.md && <Markdown>{step.md}</Markdown>}
    </div>
  )
}

/** 小测：单选，选错可以再选，选对后显示解释。 */
function QuizStep({ step }: { step: Extract<LessonStep, { type: 'quiz' }> }) {
  const [picked, setPicked] = useState<number[]>([])
  const solved = picked.includes(step.answer)
  return (
    <div className="lesson-quiz">
      <div className="quiz-q">
        <span className="faint">小测</span>
        <Markdown>{step.q}</Markdown>
      </div>
      <ol className="quiz-options">
        {step.options.map((o, i) => {
          const state = !picked.includes(i) ? '' : i === step.answer ? 'is-right' : 'is-wrong'
          return (
            <li key={i}>
              <button className={`quiz-option ${state}`} disabled={solved} onClick={() => setPicked((p) => [...p, i])}>
                <Markdown>{o}</Markdown>
              </button>
            </li>
          )
        })}
      </ol>
      {picked.length > 0 && !solved && <p className="tone-fail quiz-feedback">不对，再想想。</p>}
      {solved && step.explain && (
        <div className="quiz-explain">
          <Markdown>{step.explain}</Markdown>
        </div>
      )}
    </div>
  )
}

function Section({ sec, theme, problemId, runStatus, onOutput }: { problemId: string; sec: LessonSection; theme: Theme; runStatus?: ReactNode; onOutput: (out: ExampleOutput) => void }) {
  const body =
    sec.steps.length > 0 ? (
      sec.steps.map((st, i) =>
        st.type === 'read' ? (
          <Markdown key={i}>{st.md}</Markdown>
        ) : st.type === 'example' && 'data' in st ? (
          <div key={i}><InspectData block={st.data} lesson />{st.md && <Markdown>{st.md}</Markdown>}</div>
        ) : st.type === 'example' ? (
          <ExampleStep key={i} step={st} theme={theme} problemId={problemId} runStatus={runStatus} onOutput={onOutput} />
        ) : (
          <QuizStep key={i} step={st} />
        ),
      )
    ) : sec.card ? (
      <Markdown>{sec.card}</Markdown>
    ) : (
      <p className="faint">这个知识点的课还没写。</p>
    )
  if (sec.new) {
    return (
      <section className="lesson-section is-new">
        <h2>
          <span className="accent">新</span> {sec.name}
        </h2>
        {body}
      </section>
    )
  }
  return (
    <details className="lesson-section">
      <summary>{sec.name}</summary>
      {body}
    </details>
  )
}

/** 一道题的"课"：本题新知识展开在最前，用到的已学知识折叠在后面。 */
export function LessonView({ problemId, theme, runStatus, onOutput }: { problemId: string; theme: Theme; runStatus?: ReactNode; onOutput: (out: ExampleOutput) => void }) {
  const [sections, setSections] = useState<LessonSection[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    setSections(null)
    api
      .problemLesson(problemId)
      .then((r) => setSections(r.sections))
      .catch((e: Error) => setError(e.message))
  }, [problemId])

  if (error) return <p className="tone-fail">{error}</p>
  if (!sections) return null
  if (sections.length === 0) return <p className="faint">这道题没有标注知识点。</p>
  const used = sections.filter((s) => !s.new)
  return (
    <div className="lesson-view">
      {sections
        .filter((s) => s.new)
        .map((s) => (
          <Section key={s.skill} sec={s} theme={theme} problemId={problemId} runStatus={runStatus} onOutput={onOutput} />
        ))}
      {used.length > 0 && (
        <div className="lesson-used">
          <p className="faint lesson-used-title">用到的已学知识</p>
          {used.map((s) => (
            <Section key={s.skill} sec={s} theme={theme} problemId={problemId} runStatus={runStatus} onOutput={onOutput} />
          ))}
        </div>
      )}
    </div>
  )
}
