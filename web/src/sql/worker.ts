import { PGlite } from '@electric-sql/pglite'
import { compareCheck, compareStates, compareTables, previewCheck, previewTable, type CheckValue, type SqlCheck, type SqlTable } from './compare'
import { explainError, inDataset, lessonTable, parsers, runScript, runStatement } from './engine'

interface Input { setup: string[]; sql: string; timeoutMs?: number }
export type Job = Input & (
  { mode: 'script'; cte?: string; checks: SqlCheck[]; expected: { checks: CheckValue[] } } |
  { mode?: 'dml' | 'lesson'; expected?: SqlTable; ordered?: boolean; tolerance?: number; check_query?: string }
)

let db: PGlite
self.onmessage = async ({ data }: MessageEvent<Job | null>) => {
  try {
    if (!db) db = await PGlite.create({ parsers })
    if (!data) {
      self.postMessage({ done: true })
      return
    }
    const mode = data.mode === 'lesson' ? 'script' : data.mode
    if (data.timeoutMs) self.postMessage({ executing: true })
    const reply = await inDataset(db, data.setup, async tx => {
      if (!data.timeoutMs) self.postMessage({ executing: true })
      if (data.mode === 'script') {
        const actual = await runScript(tx, data.sql, data.checks, data.cte)
        self.postMessage({ comparing: true })
        return { checks: data.checks.map((check, i) => ({
          label: check.label, actual: previewCheck(actual[i]), expected: previewCheck(data.expected.checks[i]),
          difference: compareCheck(check, actual[i], data.expected.checks[i]),
        })) }
      }
      if (data.mode === 'lesson') return { actual: previewTable(await lessonTable(tx, data.sql)) }
      const { actual, affectedRows } = await runStatement(tx, data.sql, { mode: data.mode, check_query: data.check_query })
      self.postMessage({ comparing: true })
      const compare = data.mode === 'dml' ? compareStates : compareTables
      const difference = data.expected ? compare(actual, data.expected, !!data.ordered, data.tolerance) : null
      return { actual: previewTable(actual), affectedRows, difference }
    }, mode, data.timeoutMs)
    self.postMessage(reply)
  } catch (e) {
    self.postMessage({ error: explainError(e), timeout: (e as { code?: string }).code === '57014' })
  }
}
