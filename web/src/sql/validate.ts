import { checkQuery, checkScript, explainError, inDataset, queryTable, runScript, runStatement, structuralSql } from './engine.ts'
import { compareCheck, compareTables, type SqlCheck } from './compare.ts'

import type { PGlite } from '@electric-sql/pglite'
import type { SqlExercise } from './engine.ts'

export interface Validation extends Omit<SqlExercise, 'mode'> {
  mode?: 'dml' | 'query' | 'script'
  checks?: SqlCheck[]
  datasets: string[][]
  solution?: string
  ordered?: boolean
  answers?: Record<string, string>
  wrong?: string[]
  starter?: string
  preview?: boolean
  requiredTables?: string[]
}

function requireOrderBy(sql: string, label: string) {
  if (!/\border\s+by\b/i.test(checkQuery(sql))) throw new Error(label + '缺少 ORDER BY')
}

export async function validate(db: PGlite, job: Validation) {
  const { datasets, solution = '', ordered = false, wrong = [], starter, preview, requiredTables, check_query } = job
  const mode = job.mode === 'query' ? undefined : job.mode
  const exercise: SqlExercise = { mode: mode === 'dml' ? mode : undefined, check_query }
  let context = ''
  try {
    const tables: unknown[] = [], detected = new Set<number>()
    if (mode === 'dml' && !check_query?.trim()) throw new Error('修改类题需要 check_query')
    if (mode !== 'dml' && check_query != null) throw new Error('check_query 只用于修改类题')
    if (mode === 'script' && !job.checks?.length) throw new Error('脚本题需要非空的 checks')
    if (mode !== 'script' && job.checks?.length) throw new Error('checks 只用于脚本题')
    const readSql = mode === 'dml' ? check_query : solution
    if (mode !== 'script' && ordered) {
      requireOrderBy(readSql!, mode === 'dml' ? 'ordered 题的检查查询' : 'ordered 题的参考解')
      if (mode !== 'dml') {
        for (const [label, sql] of Object.entries(job.answers ?? {})) requireOrderBy(sql, label)
      }
    }
    for (const [i, setup] of datasets.entries()) {
      context = `数据集 ${i + 1}，建表`
      if (requiredTables && mode === 'script') setup.forEach(checkScript)
      if (requiredTables && mode !== 'script') {
        if (!requiredTables.length) throw new Error('数据集需要表名')
        const statements = setup.flatMap(script => structuralSql(script).split(';')).map(s => s.trim()).filter(Boolean)
        if (statements.some(s => !/^(create\s+table|insert\s+into)\b/i.test(s)))
          throw new Error('附加题的数据脚本只能用 CREATE TABLE 和 INSERT INTO')
      }
      const table = await inDataset(db, setup, async tx => {
        if (requiredTables) {
          const catalog = await tx.query<{ tablename: string }>("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
          for (const name of requiredTables) {
            if (!catalog.rows.some(r => r.tablename === name)) throw new Error('数据集缺少表 ' + name)
          }
        }
        if (preview) {
          const catalog = await tx.query<{ table_name: string; column_name: string; data_type: string }>("SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' ORDER BY table_name, ordinal_position")
          const names = [...new Set(catalog.rows.map(r => r.table_name))]
          const samples = []
          for (const name of names) {
            const quoted = '"' + name.replaceAll('"', '""') + '"'
            const rows = await queryTable(tx, 'SELECT * FROM ' + quoted + ' LIMIT 3')
            samples.push({ table: name, columns: catalog.rows.filter(r => r.table_name === name)
              .map(r => [r.column_name, r.data_type]), rows: rows.rows })
          }
          return samples
        }
        context = `数据集 ${i + 1}，参考解`
        if (mode === 'script') {
          const checks = job.checks!
          const expected = await runScript(tx, solution, checks)
          for (const [j, check] of checks.entries()) {
            const value = expected[j]
            if ('query' in check && check.ordered && !/\border\s+by\b/i.test(checkQuery(check.query)))
              throw new Error(check.label + '：有序检查需要 ORDER BY')
            if ('outcome' in value && ('query' in check || value.outcome !== check.expect))
              throw new Error(check.label + '：参考解未通过检查 · ' + (value.error ?? value.outcome))
          }
          return { checks: expected }
        }
        const before = mode === 'dml' ? await queryTable(tx, check_query!) : null
        const { actual: expected } = await runStatement(tx, solution, exercise)
        if (before && !compareTables(before, expected, ordered)) throw new Error('参考解执行前后 check_query 的结果相同')
        if (!before && !expected.rows.length) throw new Error('参考解结果为空')
        return expected
      }, mode)
      if (Array.isArray(table)) {
        tables.push(table)
        continue
      }
      if ('checks' in table) {
        const checks = job.checks!
        const checkScriptAnswer = async (sql: string) => {
          const actual = await inDataset(db, setup, tx => runScript(tx, sql, checks), 'script')
          return checks.map((check, j) => compareCheck(check, actual[j], table.checks[j])).find(Boolean)
        }
        for (const [label, sql] of Object.entries(job.answers ?? {})) {
          context = `数据集 ${i + 1}，${label}`
          const diff = await checkScriptAnswer(sql)
          if (diff) throw new Error(diff.message)
        }
        const fails = async (sql: string) => {
          try {
            return !!await checkScriptAnswer(sql)
          } catch {
            // 脚本本身执行失败时，同样不能通过这个数据集。
            return true
          }
        }
        for (const [j, sql] of wrong.entries()) {
          if (!detected.has(j) && await fails(sql)) detected.add(j)
        }
        if (i === 0 && starter !== undefined && !await fails(starter))
          throw new Error('改错题初始代码在样例上与参考解相同')
        tables.push(table)
        continue
      }
      // 每份答案从同一份原始数据开始，修改结果不会叠加。
      const candidate = (sql: string) => inDataset(db, setup, tx => runStatement(tx, sql, exercise), mode)
      for (const [label, sql] of Object.entries(job.answers ?? {})) {
        context = `数据集 ${i + 1}，${label}`
        const { actual } = await candidate(sql)
        const diff = compareTables(actual, table, ordered)
        if (diff) throw new Error(diff.message)
      }
      for (const [j, sql] of wrong.entries()) {
        context = `数据集 ${i + 1}，错误写法 ${j + 1}`
        const { actual } = await candidate(sql)
        if (i > 0 && compareTables(actual, table, ordered)) detected.add(j)
      }
      if (starter !== undefined) {
        context = `数据集 ${i + 1}，初始代码`
        const { actual } = await candidate(starter)
        if (i === 0 && !compareTables(actual, table, ordered)) throw new Error('改错题初始代码在样例上与参考解相同')
      }
      tables.push(table)
    }
    context = ''
    for (const j of wrong.keys()) {
      if (!detected.has(j)) throw new Error(`${mode === 'script' ? '' : '隐藏'}数据集没有抓住第 ${j + 1} 段错误写法`)
    }
    return { tables }
  } catch (error) {
    return { error: (context ? context + '：' : '') + explainError(error) }
  }
}
