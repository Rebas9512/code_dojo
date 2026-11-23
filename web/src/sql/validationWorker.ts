import { PGlite } from '@electric-sql/pglite'
import { parsers } from './engine'
import { validate, type Validation } from './validate'

self.onmessage = async ({ data }: MessageEvent<Validation>) => {
  const db = await PGlite.create({ parsers })
  try {
    self.postMessage(await validate(db, data))
  } finally {
    await db.close()
  }
}
