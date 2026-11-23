// 从 SQL 线的共享库导出书店 CSV。用 PostgreSQL 的 COPY 保留日期、引号及空值。
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { PGlite } from '@electric-sql/pglite'

const input = new URL('../../problems/sql/_db/bookstore/', import.meta.url)
const output = new URL('../../problems/wrangle/_data/bookstore/', import.meta.url)
const db = await PGlite.create()
const quoteName = name => '"' + name.replaceAll('"', '""') + '"'

try {
  for (const file of ['schema.sql', 'seed.sql']) {
    await db.exec(await readFile(new URL(file, input), 'utf8'))
  }
  await mkdir(output, { recursive: true })
  const { rows } = await db.query(`
    SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename
  `)
  for (const { tablename } of rows) {
    const table = quoteName(tablename)
    // 按列位置排序，表增加列或出现复合主键时也能稳定复现。
    const { fields } = await db.query(`SELECT * FROM ${table} LIMIT 0`)
    const order = fields.map((_, i) => i + 1).join(', ')
    const { blob } = await db.query(
      `COPY (SELECT * FROM ${table} ORDER BY ${order}) TO '/dev/blob' WITH (FORMAT csv, HEADER)`
    )
    await writeFile(new URL(tablename + '.csv', output), new Uint8Array(await blob.arrayBuffer()))
  }
} finally {
  await db.close()
}
