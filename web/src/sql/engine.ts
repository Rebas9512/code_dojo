import type { PGlite, Results, Transaction } from '@electric-sql/pglite'
import type { CheckValue, SqlCheck, SqlTable } from './compare'

const raw = (value: string) => value
// 与内容校验器一致：让 PostgreSQL 输出日期和 numeric，避免 JS 日期转换损失精度。
export const parsers = { 1082: raw, 1114: raw, 1184: raw, 1083: raw, 1700: raw, 1186: raw }

// 屏蔽字符串、带引号的标识符及注释。交给 PostgreSQL 的仍是原文。
export function structuralSql(sql: string) {
  const token = /--[^\r\n]*|\/\*|\$(?:[\p{L}_][\p{L}\p{N}_]*)?\$|[eE]'(?:\\[\s\S]|''|[^'])*'|'(?:''|[^'])*'|"(?:""|[^"])*"|[\p{L}_][\p{L}\p{N}_$]*/gu
  let masked = '', start = 0
  for (let m; (m = token.exec(sql));) {
    let end = token.lastIndex
    if (m[0] === '/*') {
      let depth = 1
      const delim = /\/\*|\*\//g
      delim.lastIndex = end
      for (let d; depth && (d = delim.exec(sql));) {
        depth += d[0] === '/*' ? 1 : -1
        end = delim.lastIndex
      }
      if (depth) throw new Error('注释缺少结尾 */。')
    } else if (m[0].startsWith('$')) {
      const close = sql.indexOf(m[0], end)
      if (close < 0) throw new Error('字符串缺少结尾的美元引号。')
      end = close + m[0].length
    } else if (/^[\p{L}_][\p{L}\p{N}_$]*$/u.test(m[0])) continue
    masked += sql.slice(start, m.index) + (m[0].startsWith('--') || m[0] === '/*' ? ' ' : '?')
    start = token.lastIndex = end
  }
  return masked + sql.slice(start)
}

function singleStatement(sql: string) {
  const shape = structuralSql(sql).trim().replace(/;$/, '').trim()
  if (shape.includes(';')) throw new Error('一次只能运行一条 SQL 语句，分号只能放在末尾。')
  return shape
}

export function checkQuery(sql: string) {
  const shape = singleStatement(sql)
  if (!/^(?:\(\s*)*(select|with)\b/i.test(shape))
    throw new Error('只允许一条 SELECT 或 WITH 查询，不能修改数据或控制事务。')
  return shape
}

export interface SqlExercise {
  mode?: 'dml'
  check_query?: string
}

async function prefixedQuery<T>(tx: Transaction, prefix: string, sql: string) {
  try {
    return await tx.query<T>(prefix + sql)
  } catch (error) {
    const e = error as Error & { position?: string }
    if (e.position) e.position = String(Math.max(1, Number(e.position) - prefix.length))
    throw error
  }
}

export async function inDataset<T>(db: PGlite, setup: string[], run: (tx: Transaction) => Promise<T>, mode?: 'dml' | 'script') {
  return db.transaction(async tx => {
    await tx.exec("SET LOCAL TIME ZONE 'UTC'; SET LOCAL statement_timeout = '2s'")
    for (const script of setup) await tx.exec(script)
    if (!mode) await tx.exec('SET TRANSACTION READ ONLY')
    const result = await run(tx)
    await tx.rollback()
    return result
  })
}

export async function runStatement(tx: Transaction, sql: string, exercise: SqlExercise):
  Promise<{ actual: SqlTable; affectedRows?: number }> {
  if (exercise.mode !== 'dml') return { actual: await queryTable(tx, sql) }
  if (!exercise.check_query?.trim()) throw new Error('修改类题需要 check_query 读取修改后的表。')
  checkQuery(exercise.check_query)
  const shape = singleStatement(sql)
  const allowed = '修改类题只允许一条 DELETE、UPDATE 或 INSERT 语句，可以用 WITH 开头。'
  if (/^with\b/i.test(shape)) {
    // 只查看计划，由 PostgreSQL 识别 WITH 后的主语句，不会预先执行修改。
    const plan = await prefixedQuery<{ 'QUERY PLAN': [{ Plan: { Operation?: string } }] }>(tx, 'EXPLAIN (FORMAT JSON) ', sql)
    const operation = plan.rows[0]['QUERY PLAN'][0].Plan.Operation
    if (!['Delete', 'Update', 'Insert'].includes(operation ?? '')) throw new Error(allowed)
  } else if (!/^(delete|update|insert)\b/i.test(shape)) throw new Error(allowed)

  const result = await tx.query(sql, [], { rowMode: 'array' })
  await tx.exec('SET TRANSACTION READ ONLY')
  return { actual: await queryTable(tx, exercise.check_query), affectedRows: result.affectedRows }
}

export async function queryTable(tx: Transaction, sql: string): Promise<SqlTable> {
  checkQuery(sql)
  // 扩展查询协议与 PostgreSQL 的游标语法再检查一次，只允许一条返回行的查询。
  await prefixedQuery(tx, 'DECLARE dojo_result NO SCROLL CURSOR FOR ', sql)
  const result = await tx.query<unknown[]>('FETCH ALL FROM dojo_result', [], { rowMode: 'array', parsers })
  await tx.exec('CLOSE dojo_result')
  return resultTable(result)
}

function resultTable(result: Results<unknown[]>): SqlTable {
  return {
    columns: result.fields.map(f => f.name), types: result.fields.map(f => f.dataTypeID),
    rows: result.rows.map(row => row.map(v => {
      if (typeof v === 'bigint') return Number(v)
      if (v instanceof Uint8Array) return Array.from(v, b => b.toString(16).padStart(2, '0')).join('')
      return v
    })),
  }
}

// 保留原文交给 PostgreSQL，只识别会接管外层事务的命令。
export function checkScript(sql: string) {
  const control = /^(?:begin|commit|end|abort|rollback|savepoint|release|start\s+transaction|prepare\s+transaction)\b/i
  let bodyDepth = 0
  for (const part of structuralSql(sql).split(';')) {
    const start = part.trimStart()
    if (!bodyDepth && control.test(start))
      throw new Error('事务由判题器管理，请移除脚本中的事务控制语句。')
    // SQL 函数的 BEGIN ATOMIC ... END 内部也可用分号，END 在这里是函数体的结尾。
    if (bodyDepth || /^create\s+(?:or\s+replace\s+)?(?:function|procedure)\b/i.test(start)) {
      for (const [word] of start.toUpperCase().matchAll(/\bBEGIN\s+ATOMIC\b|\bCASE\b|\bEND\b/g)) {
        if (word.startsWith('BEGIN') || (bodyDepth && word === 'CASE')) bodyDepth++
        else if (bodyDepth && word === 'END') bodyDepth--
      }
    }
  }
}

export async function lessonTable(tx: Transaction, sql: string) {
  checkScript(sql)
  const results = await tx.exec(sql, { rowMode: 'array', parsers })
  const last = results.at(-1)
  return last ? resultTable(last as Results<unknown[]>) : { columns: [], types: [], rows: [] }
}

export async function runScript(tx: Transaction, sql: string, checks: SqlCheck[]) {
  checkScript(sql)
  await tx.exec(sql)
  const values: CheckValue[] = []
  for (const check of checks) {
    if ('probe' in check) checkScript(check.probe)
    await tx.exec('SAVEPOINT dojo_check')
    try {
      if ('query' in check) values.push(await queryTable(tx, check.query))
      else {
        await tx.query(check.probe)
        values.push({ outcome: 'ok' })
      }
    } catch (error) {
      values.push({ outcome: 'error', error: (error as Error).message })
    }
    await tx.exec('ROLLBACK TO dojo_check; RELEASE dojo_check')
  }
  return values
}

export function explainError(error: unknown) {
  const e = error as { message?: string; code?: string; position?: string }
  const hints: Record<string, string> = {
    '42703': '列不存在，请对照表结构检查列名。', '42P01': '表不存在，请检查 FROM 后的表名或别名。',
    '42601': `语法错误${e.position ? '，请检查第 ' + e.position + ' 个字符附近' : '，请检查查询的写法'}。`,
    '42803': '未聚合的列需要出现在 GROUP BY 中。', '57014': '超时，请缩小查询范围或检查递归条件。',
    '42804': '类型不匹配，请检查两边的数据类型。', '42883': '找不到匹配的函数或运算符，请检查数据类型。',
    '22P02': '类型不匹配，请检查输入值能否转换。', '42846': '这两种类型不能直接转换。',
  }
  const message = e.message || String(error)
  if (/data-modifying statements|SELECT \.\.\. INTO is not allowed|read-only transaction/i.test(message))
    return message + '\n只允许读取数据的查询。'
  return e.code ? message + '\n' + (hints[e.code] || '请对照表结构和题意检查这条查询。') : message
}
