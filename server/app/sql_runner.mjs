// 后端与 verify_bank 共用这个入口，依赖来自内容侧已锁定的 PGlite。
import { createRequire } from 'node:module'
import { parsers } from '../../web/src/sql/engine.ts'
import { validate } from '../../web/src/sql/validate.ts'

const require = createRequire(new URL('../../scripts/curriculum/package.json', import.meta.url))
const { PGlite } = require('@electric-sql/pglite')
const chunks = []
for await (const chunk of process.stdin) chunks.push(chunk)
const job = JSON.parse(Buffer.concat(chunks))
const db = await PGlite.create({ parsers })
try {
  process.stdout.write(JSON.stringify(await validate(db, job)))
} finally {
  await db.close()
}
