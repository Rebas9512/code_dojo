// 固定题的 MySQL 原稿由两个题库校验入口共用，参考解和典型错解沿用通用校验。
import { inDataset, queryTable } from '../../web/src/sql/engine.ts'
import { validate } from '../../web/src/sql/validate.ts'

export async function validateSql(db, job) {
  if (job.starter_dialect !== 'mysql') return validate(db, job)
  const { starter, ...exercise } = job
  const result = await validate(db, exercise)
  if (result.error) return result

  return inDataset(db, job.datasets[0], async tx => {
    try {
      await queryTable(tx, starter)
    } catch (error) {
      // SQLSTATE 来自 PostgreSQL。空查询等由运行器拒绝的输入不能充当方言报错。
      if (error.code) return { ...result, starterError: error.message }
      return { error: '样例初始查询：' + error.message }
    }
    return { error: 'MySQL 初始查询在样例上成功执行，预期 PostgreSQL 报错' }
  })
}
