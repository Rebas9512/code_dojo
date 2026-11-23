import { PGlite } from '@electric-sql/pglite'
import { compareStates, compareTables, type SqlTable } from './compare'
import { explainError, inDataset, parsers, runStatement, type SqlExercise } from './engine'

export interface Job extends SqlExercise {
  setup: string[]
  sql: string
  expected?: SqlTable
  ordered?: boolean
  tolerance?: number
}

function preview(table: SqlTable) {
  return { ...table, rows: table.rows.slice(0, 50), rowCount: table.rows.length }
}

let db: PGlite
self.onmessage = async ({ data }: MessageEvent<Job | null>) => {
  try {
    if (!db) db = await PGlite.create({ parsers })
    if (!data) {
      self.postMessage({ done: true })
      return
    }
    const { actual, affectedRows } = await inDataset(db, data.setup, tx => {
      self.postMessage({ executing: true })
      return runStatement(tx, data.sql, data)
    }, data.mode)
    self.postMessage({ comparing: true })
    const compare = data.mode === 'dml' ? compareStates : compareTables
    const difference = data.expected ? compare(actual, data.expected, !!data.ordered, data.tolerance) : null
    self.postMessage({ actual: preview(actual), affectedRows, difference })
  } catch (e) {
    self.postMessage({ error: explainError(e), timeout: (e as { code?: string }).code === '57014' })
  }
}
