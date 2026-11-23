// 复用内存数据库，每份数据和答案在独立事务里执行并回滚。
import { PGlite } from '@electric-sql/pglite'
import { inDataset, lessonTable, parsers, queryTable } from '../../web/src/sql/engine.ts'
import { validateSql } from '../../server/app/validate_sql.mjs'

const chunks = []
for await (const chunk of process.stdin) chunks.push(chunk)
const jobs = JSON.parse(Buffer.concat(chunks))
const db = await PGlite.create({ parsers })
const out = []
for (const job of jobs) {
  if (job.validation) {
    out.push({ key: job.key, ...await validateSql(db, job.validation) })
    continue
  }
  const lesson = 'example' in job.queries
  const item = { key: job.key, results: {}, setupError: null }
  try {
    await inDataset(db, job.setup, async tx => {
      for (const [name, sql] of Object.entries(job.queries)) {
        await tx.exec('SAVEPOINT dojo_answer')
        try {
          const table = lesson ? await lessonTable(tx, sql) : await queryTable(tx, sql)
          item.results[name] = { ok: true, ...table }
        } catch (error) {
          item.results[name] = { ok: false, error: error.message }
        }
        await tx.exec('ROLLBACK TO dojo_answer; RELEASE dojo_answer')
      }
    }, lesson ? 'script' : undefined)
  } catch (error) {
    item.setupError = error.message
  }
  out.push(item)
}
await db.close()
process.stdout.write(JSON.stringify(out))
