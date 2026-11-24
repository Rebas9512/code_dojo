import { api, type CaseResult, type JudgeResult } from '../api'
import { previewTable, type CheckReport, type Difference, type SqlTable } from './compare'
import type { Job } from './worker'

export type TablePreview = SqlTable & { rowCount: number }
interface Reply {
  checks?: CheckReport[]
  affectedRows?: number
  actual?: TablePreview
  difference?: Difference
  error?: string
  timeout?: boolean
}

let worker: Worker | null = null
let queue = Promise.resolve()

function exchange(job: Job | null): Promise<Reply> {
  worker ??= new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' })
  const active = worker
  return new Promise((resolve, reject) => {
    function stop(error: Error) {
      window.clearTimeout(timer)
      active.terminate()
      worker = null
      reject(error)
    }
    const limit = job?.timeoutMs ?? 2000
    let timer = window.setTimeout(() => stop(new Error('准备数据库超时，请重试。')), 30000)
    active.onerror = e => stop(new Error(e.message || '数据库加载失败，请重试。'))
    active.onmessage = ({ data }) => {
      window.clearTimeout(timer)
      // WebAssembly 长查询可能阻塞 Worker 的事件循环，由主线程负责最终截断。
      if (data.executing) timer = window.setTimeout(() => stop(new Error(`超时：查询超过 ${limit / 1000} 秒。`)), limit + 200)
      else if (data.comparing) timer = window.setTimeout(() => stop(new Error('比较结果超时。')), 30000)
      else if (!job && data.error) stop(new Error(data.error))
      else resolve(data)
    }
    active.postMessage(job)
  })
}

function enqueue<T>(fn: () => Promise<T>) {
  const result = queue.then(fn)
  queue = result.then(() => {}, () => {})
  return result
}

export function prepare() {
  return enqueue(async () => {
    if (!worker) {
      await exchange(null)
    }
  })
}

async function execute(job: Job) {
  await prepare()
  const reply = await enqueue(() => exchange(job))
  if (reply.error) throw new Error(reply.timeout ? '超时：' + reply.error : reply.error)
  return reply
}

export async function runProject(job: Extract<Job, { mode: 'script' }>) {
  return (await execute(job)).checks!
}

export async function runExample(setup: string[], sql: string) {
  const reply = await execute({ setup, sql, mode: 'lesson' })
  return reply.actual!
}

export async function grade(id: string, sql: string, kind: 'run' | 'submit'): Promise<JudgeResult> {
  const plan = await api.sqlCases(id, kind === 'submit' ? 'all' : 'sample')
  const cases: CaseResult[] = []
  for (const i of plan.datasets.keys()) {
    let job: Job
    let expected: unknown
    if (plan.mode === 'script') {
      const data = plan.datasets[i]
      job = { sql, setup: data.setup, mode: 'script', cte: plan.cte, checks: plan.checks, expected: data.expected }
      expected = { labels: plan.checks.map(c => c.label) }
    } else {
      const data = plan.datasets[i]
      job = { sql, setup: data.setup, expected: data.expected, ordered: plan.ordered,
        tolerance: plan.tolerance, mode: plan.mode, check_query: plan.check_query }
      expected = previewTable(data.expected)
    }
    const start = performance.now()
    let status: CaseResult['status'] = 'passed', error = null
    let actual: TablePreview | { checks: CheckReport[] } | null = null, difference: Difference | undefined
    let affectedRows: number | undefined
    try {
      const result = await execute(job)
      actual = result.checks ? { checks: result.checks } : result.actual!
      affectedRows = result.affectedRows
      difference = result.difference
      if (difference || result.checks?.some(check => check.difference)) status = 'wrong_answer'
    } catch (e) {
      error = (e as Error).message
      status = error.startsWith('超时') ? 'timeout' : 'runtime_error'
    }
    cases.push({ expected, actual, difference, status, error, hidden: plan.datasets[i].hidden, time_ms: Math.round(performance.now() - start),
      input: {}, stdout: '', affected_rows: affectedRows })
  }
  return { cases, verdict: cases.find(c => c.status !== 'passed')?.status ?? 'accepted' }
}
