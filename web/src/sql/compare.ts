// 列名仅用于显示。保留原始下标，让忽略行序的比较也能指出结果表里的位置。
export interface SqlTable {
  columns: string[]
  types: number[]
  rows: unknown[][]
}

export interface Difference {
  message: string
  actualRow?: number
  expectedRow?: number
  column?: number
  missingRows?: number[]
  extraRows?: number[]
}

const numericTypes = new Set([20, 21, 23, 700, 701, 1700])

function normalize(value: unknown, type: number): unknown {
  if (typeof value !== 'string') return value
  if (numericTypes.has(type)) return Number(value)
  if (type === 1114 || type === 1184) return value.replace(' ', 'T')
  return value
}

function equal(a: unknown, b: unknown, tolerance: number): boolean {
  if (a === b) return true
  if (typeof a === 'number' && typeof b === 'number') {
    return Number.isFinite(a) && Number.isFinite(b) &&
      Math.abs(a - b) <= tolerance * Math.max(1, Math.abs(a), Math.abs(b))
  }
  // 内容校验器用 Python 值作比较，布尔值分别等于整数 0、1。
  if (typeof a === 'boolean' && typeof b === 'number') return Number(a) === b
  if (typeof b === 'boolean' && typeof a === 'number') return Number(b) === a
  // PostgreSQL 的数组和 JSON 字段也按值比较。
  if (a && b && typeof a === 'object' && typeof b === 'object') {
    const left = Object.entries(a), right = Object.entries(b)
    return Array.isArray(a) === Array.isArray(b) && left.length === right.length &&
      left.every(([k, v]) => Object.hasOwn(b, k) && equal(v, (b as Record<string, unknown>)[k], 0))
  }
  return false
}

function sortValue(v: unknown): [number, string | number] {
  if (v === null) return [0, '']
  if (typeof v === 'number') return [1, Number(v.toFixed(6))]
  if (typeof v === 'boolean') return [2, v ? 'True' : 'False']
  return [2, typeof v === 'object' ? JSON.stringify(v) : String(v)]
}

function indexed(table: SqlTable, sort: boolean) {
  const rows = table.rows.map((row, index) => ({ index, cells: row.map((v, i) => normalize(v, table.types[i])) }))
  if (sort) rows.sort((a, b) => {
    for (let i = 0; i < a.cells.length; i++) {
      const [ka, va] = sortValue(a.cells[i]), [kb, vb] = sortValue(b.cells[i])
      if (ka !== kb) return ka - kb
      if (va !== vb) return va < vb ? -1 : 1
    }
    return 0
  })
  return rows
}

export function compareTables(actual: SqlTable, expected: SqlTable, ordered: boolean, tolerance = 1e-6): Difference | null {
  if (actual.columns.length !== expected.columns.length)
    return { message: `列数不同：你的结果有 ${actual.columns.length} 列，期望 ${expected.columns.length} 列。` }
  if (actual.rows.length !== expected.rows.length)
    return { message: `行数不同：你的结果有 ${actual.rows.length} 行，期望 ${expected.rows.length} 行。` }
  const a = indexed(actual, !ordered), b = indexed(expected, !ordered)
  for (let i = 0; i < a.length; i++) {
    const col = a[i].cells.findIndex((v, j) => !equal(v, b[i].cells[j], tolerance))
    if (col < 0) continue
    const orderOnly = ordered && !compareTables(actual, expected, false, tolerance)
    return {
      message: orderOnly ? `顺序不同：从第 ${i + 1} 行开始，请检查 ORDER BY。` :
        `你的第 ${a[i].index + 1} 行、第 ${col + 1} 列与期望第 ${b[i].index + 1} 行的值不同。`,
      actualRow: a[i].index, expectedRow: b[i].index, column: col,
    }
  }
  return null
}

export function compareStates(actual: SqlTable, expected: SqlTable, ordered: boolean, tolerance = 1e-6) {
  const diff = compareTables(actual, expected, ordered, tolerance)
  if (!diff || actual.columns.length !== expected.columns.length || actual.rows.length === expected.rows.length) return diff
  // 标出预览中应当保留或多出的行。每个匹配只消耗一次，重复行也按份数核对。
  const missing = actual.rows.length < expected.rows.length
  const [larger, smaller] = missing ? [expected, actual] : [actual, expected]
  const available = indexed(smaller, false)
  const used = new Set<number>()
  const unmatched: number[] = []
  larger.rows.slice(0, 50).forEach((row, index) => {
    const cells = row.map((v, i) => normalize(v, larger.types[i]))
    const match = available.findIndex(r => !used.has(r.index) && cells.every((v, j) => equal(v, r.cells[j], tolerance)))
    if (match < 0) unmatched.push(index)
    else used.add(match)
  })
  return missing ? { ...diff, missingRows: unmatched } : { ...diff, extraRows: unmatched }
}

export type SqlCheck = { label: string; query: string; ordered?: boolean } |
  { label: string; result: true; ordered?: boolean } |
  { label: string; probe: string; expect: 'ok' | 'error' }
export type CheckValue = SqlTable | { outcome: 'ok' | 'error'; error?: string }

export function compareCheck(check: SqlCheck, actual: CheckValue, expected: CheckValue): Difference | null {
  if ('probe' in check && 'outcome' in actual)
    return actual.outcome === check.expect ? null : { message: check.expect === 'error' ? '应当被拒绝，实际被接受' : '应当被接受，实际被拒绝' }
  if (!('probe' in check) && 'rows' in actual && 'rows' in expected)
    return compareStates(actual, expected, !!check.ordered)
  return { message: '检查查询执行失败' }
}

export function previewTable(table: SqlTable) {
  return { ...table, rows: table.rows.slice(0, 50), rowCount: table.rows.length }
}

export function previewCheck(value: CheckValue) {
  return 'rows' in value ? previewTable(value) : value
}

export interface CheckReport {
  label: string
  actual: ReturnType<typeof previewCheck>
  expected: ReturnType<typeof previewCheck>
  difference: Difference | null
}
