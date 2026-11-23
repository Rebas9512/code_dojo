import { lazy, Suspense, useEffect, useState } from 'react'
import type { FullCaseResult, JudgeResult, Mode } from '../api'
import { Markdown } from './Markdown'
import { VERDICT_NAME, verdictTone } from '../labels'

import type { TablePreview } from '../sql/client'
const SqlTableView = lazy(() => import('../sql/SqlTableView'))

interface Props {
  sql?: boolean
  result: JudgeResult
  kind: 'run' | 'submit'
  mode: Mode
  paramNames: string[]
}

function show(v: unknown): string {
  return JSON.stringify(v)
}

function FunctionInput({ args, names }: { args: unknown[]; names: string[] }) {
  return (
    <pre className="io">
      {args.map((a, i) => `${names[i] ?? `参数${i + 1}`} = ${show(a)}`).join('\n')}
    </pre>
  )
}

function ClassCase({ c }: { c: FullCaseResult }) {
  const ops = (c.input.ops as string[]) ?? []
  const args = (c.input.args as unknown[][]) ?? []
  const expected = (c.expected as unknown[]) ?? []
  const actual = (c.actual as unknown[] | null) ?? []
  return (
    <table className="ops">
      <tbody>
        {ops.map((op, i) => {
          const call = `${i === 0 ? op : `.${op}`}(${(args[i] ?? []).map(show).join(', ')})`
          const mismatch = c.actual !== null && i > 0 && show(expected[i]) !== show(actual[i])
          return (
            <tr key={i} className={mismatch ? 'mismatch' : undefined}>
              <td className="call">{call}</td>
              <td>{i === 0 ? '' : show(expected[i])}</td>
              <td>{i === 0 || c.actual === null ? '' : show(actual[i])}</td>
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}

function CaseDetail({ c, mode, names }: { c: FullCaseResult; mode: Mode; names: string[] }) {
  const tone = verdictTone(c.status)
  return (
    <div className="case-detail">
      {mode === 'class' ? (
        <>
          <div className="row-label">调用 · 期望 · 实际</div>
          <ClassCase c={c} />
        </>
      ) : mode === 'predict' ? (
        <>
          <div className="row-label">你的答案</div>
          <pre className="io">{String(c.actual ?? '')}</pre>
          {c.status !== 'passed' && (
            <>
              <div className="row-label">实际输出</div>
              <pre className="io">{String(c.expected ?? '')}</pre>
            </>
          )}
        </>
      ) : (
        <div className="case-fields">
          <div><div className="row-label">输入</div>
            {mode === 'stdio' ? <pre className="io">{String(c.input.stdin ?? '')}</pre> :
              <FunctionInput args={(c.input.args as unknown[]) ?? []} names={names} />}
          </div>
          <div><div className="row-label">期望</div>
            <pre className="io">{mode === 'stdio' ? String(c.expected ?? '') : show(c.expected)}</pre>
          </div>
          {c.status !== 'runtime_error' && c.status !== 'timeout' && c.status !== 'skipped' &&
            <div><div className="row-label">实际</div>
              <pre className={`io ${tone === 'fail' ? 'tone-fail' : ''}`}>
                {mode === 'stdio' ? String(c.actual ?? '') : show(c.actual)}
              </pre>
            </div>}
        </div>
      )}
      {c.error && (
        <>
          <div className="row-label">报错</div>
          <pre className="io tone-fail">{c.error}</pre>
        </>
      )}
      {c.stdout && (
        <>
          <div className="row-label">print 输出</div>
          <pre className="io">{c.stdout}</pre>
        </>
      )}
    </div>
  )
}

export function ResultPanel({ result, kind, mode, paramNames, sql }: Props) {
  const firstBad = Math.max(0, result.cases.findIndex((c) => c.status !== 'passed'))
  const [selected, setSelected] = useState(firstBad)
  useEffect(() => setSelected(firstBad), [result, firstBad])

  const tone = verdictTone(result.verdict)
  if (mode === 'inspect') {
    const feedback = result.misconception
    return <section className="result inspect-result" aria-live="polite">
      <strong className={`verdict tone-${tone}`}>{result.verdict === 'accepted' ? '答对了' : '答错了'}</strong>
      {feedback && <p><strong>{feedback.name}</strong> · {feedback.line}</p>}
      {result.explain && <Markdown>{result.explain}</Markdown>}
    </section>
  }
  const c = result.cases[selected]
  return (
    <section className="result" aria-live="polite">
      <header className="result-head">
        <strong className={`verdict tone-${tone}`}>{VERDICT_NAME[result.verdict]}</strong>
        {result.total !== undefined && (
          <span className="muted">
            {result.passed}/{result.total}
            {kind === 'run' ? ' 样例' : ''}
          </span>
        )}
        {c && c.time_ms > 0 && mode !== 'predict' && <span className="faint">{c.time_ms} ms</span>}
        {mode === 'dml' && c?.affected_rows != null && <span className="muted">影响了 {c.affected_rows} 行</span>}
        {(sql || result.cases.length > 1) && (
          <nav className="case-tabs">
            {result.cases.map((cr, i) => (
              <button
                key={i}
                className={`case-tab tone-${verdictTone(cr.status)} ${i === selected ? 'is-active' : ''}`}
                onClick={() => setSelected(i)}
                title={cr.hidden ? '隐藏用例' : '样例'}
              >
                {cr.hidden ? `·${i + 1}` : i + 1}
              </button>
            ))}
          </nav>
        )}
      </header>
      {result.error && <pre className="io tone-fail">{result.error}</pre>}
      {c?.preview && <div className="case-detail case-fields">
        {([['输入', c.input], ['期望', c.expected], ['实际', c.actual], ['差异', c.difference],
           ['报错', c.error], ['输出', c.stdout]] as const).filter(([, v]) => v != null && v !== '').map(([label, v]) =>
          <div key={label}><div className="row-label">{label}</div>
            <pre className="io">{typeof v === 'string' ? v : show(v)}</pre></div>)}
      </div>}
      {c && !c.preview && sql && <Suspense fallback={null}><div className="case-detail">
        {c.difference && <p className="tone-fail">{c.difference.message}</p>}
        {c.error && <pre className="io tone-fail">{c.error}</pre>}
        <div className="sql-results">
          {c.actual != null && <SqlTableView label={mode === 'dml' ? '修改后的表' : '你的结果'} table={c.actual as TablePreview}
            markedRows={c.difference?.extraRows}
            row={c.difference?.actualRow} column={c.difference?.column} />}
          <SqlTableView label={mode === 'dml' ? '期望的表' : '期望结果'} table={c.expected as TablePreview}
            markedRows={c.difference?.missingRows}
            row={c.difference?.expectedRow} column={c.difference?.column} />
        </div>
      </div></Suspense>}
      {c && !c.preview && !sql && <CaseDetail c={c} mode={mode} names={paramNames} />}
    </section>
  )
}
