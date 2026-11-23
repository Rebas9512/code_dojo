import assert from 'node:assert/strict'
import test from 'node:test'
import { PGlite } from '@electric-sql/pglite'
import { compareCheck, compareStates, compareTables } from '../src/sql/compare.ts'
import { checkScript, lessonTable, runScript, checkQuery, explainError, inDataset, queryTable, runStatement } from '../src/sql/engine.ts'

const table = (rows, types = [23], columns = types.map(() => '列')) => ({ rows, types, columns })

test('不比列名，numeric、整数和浮点使用相对与绝对容差', () => {
  assert.equal(compareTables(table([['1000000.5'], ['0.0000008']], [1700], ['甲']),
    table([[1000000], [0]], [701], ['乙']), true), null)
  assert.match(compareTables(table([[0.000002]]), table([[0]]), true).message, /值不同/)
  assert.match(compareTables(table([['2']], [25]), table([[2]]), true).message, /值不同/)
})
test('NULL、ISO 日期和时间戳', () => {
  const rows = [[null, '2024-02-29', '2024-02-29 12:30:00']]
  assert.equal(compareTables(table(rows, [25, 1082, 1114]),
    table([[null, '2024-02-29', '2024-02-29T12:30:00']], [25, 1082, 1114]), true), null)
  assert.match(compareTables(table([[null]]), table([['NULL']], [25]), true).message, /值不同/)
})
test('忽略行序时保留重复行，错误位置对应原始行', () => {
  const a = table([[2], [3], [2]])
  assert.equal(compareTables(a, table([[3], [2], [2]]), false), null)
  const diff = compareTables(a, table([[3], [2], [3]]), false)
  assert.equal(diff.actualRow, 2)
  assert.equal(diff.expectedRow, 0)
})
test('列数、行数与排序错误分别提示', () => {
  assert.match(compareTables(table([]), table([], [23, 23]), false).message, /列数不同/)
  assert.match(compareTables(table([]), table([[1]]), false).message, /行数不同/)
  assert.match(compareTables(table([[2], [1]]), table([[1], [2]]), true).message, /顺序不同/)
})
test('只准单条查询，注释与引号里的分号和关键词属于内容', () => {
  for (const sql of ['DROP TABLE t', 'INSERT INTO t VALUES(1)', 'UPDATE t SET n=2', 'BEGIN', 'COMMIT',
    'SELECT 1; SELECT 2', 'SELECT 1;;'])
    assert.throws(() => checkQuery(sql))
  checkQuery(`/* 一 /* 二 */ */ WITH t AS (SELECT 'drop;''update' AS "into") SELECT $$a;b$$ FROM t; -- ;`)
})
test('真实引擎保留同名列和英文错误，事务结束后数据可重新建表', async () => {
  const db = await PGlite.create()
  try {
    const setup = ['CREATE TABLE books(n integer); INSERT INTO books VALUES(1)']
    await assert.rejects(inDataset(db, setup, tx => queryTable(tx, 'SELECT nope FROM books')),
      e => explainError(e).includes('column "nope" does not exist\n列不存在'))
    for (const sql of ['WITH w AS (DELETE FROM books RETURNING *) SELECT * FROM w', 'SELECT 1 INTO t',
      'WITH w AS (SELECT 1) UPDATE books SET n=9', 'SELECT n FROM books FOR UPDATE']) {
      await assert.rejects(inDataset(db, setup, tx => queryTable(tx, sql)),
        e => /只允许|语法错误/.test(explainError(e)))
    }
    assert.deepEqual((await inDataset(db, setup, tx => queryTable(tx, 'SELECT n AS update FROM books'))).rows, [[1]])
    for (const sql of ['SELECT n,n FROM books', 'WITH t AS (SELECT n FROM books) SELECT n,n FROM t;']) {
      assert.deepEqual(await inDataset(db, setup, tx => queryTable(tx, sql)), table([[1, 1]], [23, 23], ['n', 'n']))
    }
    for (const [sql, hint] of [['SELECT 1 + )', '第 12 个字符'], ['SELECT n FROM abc', '表不存在'],
      ['SELECT n, sum(n) FROM books', 'GROUP BY'], ["SELECT 'oops'::int", '类型不匹配']]) {
      await assert.rejects(inDataset(db, setup, tx => queryTable(tx, sql)), e => explainError(e).includes(hint))
    }
  } finally { await db.close() }
})

test('与内容侧 verify_sql 共用的比较样例', async () => {
  const { readFile } = await import('node:fs/promises')
  const examples = JSON.parse(await readFile(new URL('./sql-comparisons.json', import.meta.url), 'utf8'))
  for (const c of examples)
    assert.equal(!compareTables(table(c.a, c.types), table(c.b, c.types), c.ordered), c.equal, c.name)
})

test('修改后的表按最终状态比较，能圈出多删、多留的重复行', () => {
  const expected = table([[8], [4], [8], [7]])
  const actual = table([[4], [8]])
  assert.deepEqual(compareStates(actual, expected, false).missingRows, [2, 3])
  assert.deepEqual(compareStates(expected, actual, false).extraRows, [2, 3])
  assert.equal(compareStates(table([]), table([]), true), null)
  assert.equal(compareStates(table([[4], [8]]), table([[8], [4]]), false), null)
})

test('修改语句读最终状态、报告影响行数，每次从原表开始', async () => {
  const db = await PGlite.create()
  const setup = ['CREATE TABLE t(n int); INSERT INTO t VALUES (2), (5)']
  const exercise = { mode: 'dml', check_query: 'SELECT n FROM t ORDER BY n' }
  const run = sql => inDataset(db, setup, tx => runStatement(tx, sql, exercise), 'dml')
  try {
    for (const [sql, rows, affected] of [
      ['WITH old AS (SELECT min(n) AS n FROM t) DELETE FROM t USING old WHERE t.n = old.n RETURNING 99', [[5]], 1],
      ['UPDATE t SET n=n+10', [[12], [15]], 2],
      ['INSERT INTO t VALUES (7), (9)', [[2], [5], [7], [9]], 2],
      ['DELETE FROM t WHERE false', [[2], [5]], 0],
      ['DELETE FROM t', [], 2],
    ]) {
      const result = await run(sql)
      assert.deepEqual(result.actual.rows, rows)
      assert.equal(result.affectedRows, affected)
    }
    for (const sql of ['DROP TABLE t', 'TRUNCATE t', 'ALTER TABLE t ADD q int', 'COMMIT', 'ROLLBACK',
      'BEGIN', 'SELECT 1', 'WITH w AS (SELECT 1) SELECT * FROM w',
      'WITH w AS (DELETE FROM t RETURNING *) SELECT * FROM w', 'DELETE FROM t; INSERT INTO t VALUES (2)'])
      await assert.rejects(run(sql), /只允许一条|只能运行一条/)
    const broken = 'WITH w AS (SELECT 1 + ) DELETE FROM t'
    await assert.rejects(run(broken), e => explainError(e).includes(`第 ${broken.indexOf(')') + 1} 个字符`))
    assert.deepEqual((await run('/* ; */ UPDATE t SET n=3 WHERE n=2; -- ;')).actual.rows, [[3], [5]])
  } finally { await db.close() }
})

test('多语句示例显示末表，脚本检查分别回滚并定位失败项', async () => {
  const db = await PGlite.create()
  const sql = "CREATE TABLE t(email text UNIQUE); INSERT INTO t VALUES ('a')"
  const checks = [{ label: '重复', probe: "INSERT INTO t VALUES ('a')", expect: 'error' },
    { label: '新增', probe: "INSERT INTO t VALUES ('b')", expect: 'ok' },
    { label: '名单', query: 'SELECT email FROM t' }]
  const run = script => inDataset(db, [], tx => runScript(tx, script, checks), 'script')
  try {
    const a = table([[1], [2]]), b = table([[2], [1]])
    assert.equal(compareCheck(checks[2], a, b), null)
    assert.match(compareCheck({ ...checks[2], ordered: true }, a, b).message, /顺序/)
    const expected = await run(sql)
    assert.deepEqual(expected[2].rows, [['a']])
    const actual = await run(sql.replace(' UNIQUE', ''))
    assert.deepEqual(checks.map((c, i) => !!compareCheck(c, actual[i], expected[i])), [true, false, false])
    const missing = await run('CREATE TABLE other(n int)')
    assert.match(missing[2].error, /does not exist/)
    assert.ok(compareCheck(checks[2], missing[2], expected[2]))
    const example = () => inDataset(db, [], tx => lessonTable(tx, sql + '; SELECT * FROM t'), 'script')
    assert.deepEqual(await example(), await example())
    assert.deepEqual((await example()).rows, [['a']])
    for (const command of ['BEGIN', 'COMMIT', 'END', 'ROLLBACK', 'SAVEPOINT x', 'START TRANSACTION', 'ABORT'])
      assert.throws(() => checkScript(sql + '; /* 注释 */ ' + command), /事务控制/)
    const fn = 'CREATE FUNCTION f(n int) RETURNS int LANGUAGE SQL BEGIN ATOMIC SELECT CASE WHEN n>0 THEN 1 ELSE 0 END; END;'
    const scalar = await inDataset(db, [], tx => lessonTable(tx, fn + 'SELECT f(2)'), 'script')
    assert.deepEqual(scalar.rows, [[1]])
    assert.throws(() => checkScript(fn + 'COMMIT'), /事务控制/)
    checkScript("SELECT '; COMMIT', $$; BEGIN$$; -- ROLLBACK\nSELECT 1")
  } finally { await db.close() }
})
