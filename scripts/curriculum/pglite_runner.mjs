// 在 PGlite（浏览器里用的同一个 PostgreSQL 18 引擎）上执行 SQL，给 verify_sql.py 用。
//
// 输入（stdin，JSON）：[{ "key": "...", "setup": ["建表 / 数据脚本", ...], "queries": { "名字": "SELECT ..." } }]
// 输出（stdout，JSON）：[{ "key": "...", "setupError": null | "...",
//                          "results": { "名字": { "ok": true, "columns": [...], "types": [...], "rows": [[...]] }
//                                                | { "ok": false, "error": "..." } } }]
// 每个 job 用一个全新的数据库实例；同一个 job 里的查询都是只读的 SELECT，按顺序在同一实例上执行。
// 日期、时间、numeric 一律按 PostgreSQL 的文本形式返回，避免 JS Date 的时区换算；比较在 Python 侧做。
import { PGlite } from "@electric-sql/pglite";

const RAW = (v) => v;
const parsers = { 1082: RAW, 1114: RAW, 1184: RAW, 1083: RAW, 1700: RAW, 1186: RAW };

async function readStdin() {
  const chunks = [];
  for await (const c of process.stdin) chunks.push(c);
  return Buffer.concat(chunks).toString("utf8");
}

function plain(v) {
  if (typeof v === "bigint") return Number(v);
  if (v instanceof Date) return v.toISOString();
  if (v instanceof Uint8Array) return Buffer.from(v).toString("hex");
  return v;
}

const jobs = JSON.parse(await readStdin());
const out = [];
for (const job of jobs) {
  const db = await PGlite.create({ parsers });
  const res = { key: job.key, setupError: null, results: {} };
  try {
    for (const script of job.setup) await db.exec(script);
  } catch (e) {
    res.setupError = String(e.message || e);
  }
  if (!res.setupError) {
    for (const [name, sql] of Object.entries(job.queries)) {
      try {
        const r = await db.query(sql, [], { rowMode: "array", parsers });
        res.results[name] = {
          ok: true,
          columns: r.fields.map((f) => f.name),
          types: r.fields.map((f) => f.dataTypeID),
          rows: r.rows.map((row) => row.map(plain)),
        };
      } catch (e) {
        res.results[name] = { ok: false, error: String(e.message || e) };
      }
    }
  }
  await db.close();
  out.push(res);
}
process.stdout.write(JSON.stringify(out));
