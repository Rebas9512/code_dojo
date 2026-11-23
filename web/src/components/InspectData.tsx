import { memo, useState, type ReactNode } from 'react'
import type { DataBlock } from '../api'
import './inspect.css'

type Cell = string | null
type View = '表格' | 'CSV' | 'JSON'

// 保留引号里的逗号、换行和双引号。只有没加引号的空字段表示缺失。
function parseCsv(text: string): Cell[][] {
  const rows: Cell[][] = []
  let row: Cell[] = []
  let value = ''
  let quoted = false
  let inQuotes = false
  const endCell = () => {
    row.push(!quoted && value === '' ? null : value)
    value = ''
    quoted = false
  }
  for (let i = 0; i < text.length; i++) {
    const ch = text[i]
    if (inQuotes) {
      if (ch !== '"') {
        value += ch
      } else if (text[i + 1] === '"') {
        value += '"'
        i++
      } else {
        inQuotes = false
      }
    } else if (ch === ',') {
      endCell()
    } else if (ch === '\r' || ch === '\n') {
      if (ch === '\r' && text[i + 1] === '\n') i++
      endCell()
      rows.push(row)
      row = []
    } else if (quoted) {
      throw new Error('右引号后应当是逗号或换行。')
    } else if (ch === '"' && !value) {
      quoted = true
      inQuotes = true
    } else {
      value += ch
    }
  }
  if (inQuotes) throw new Error('有一个字段缺少右引号。')
  if (row.length || value || quoted) {
    endCell()
    rows.push(row)
  }
  if (!rows.length) throw new Error('请先写一行表头。')
  const bad = rows.findIndex((r) => r.length !== rows[0].length)
  if (bad >= 0) throw new Error(`第 ${bad + 1} 条记录与表头的列数不同。`)
  return rows
}

function toObjects(rows: Cell[][]) {
  const [header, ...body] = rows
  if (header.some((v) => !v) || new Set(header).size !== header.length)
    throw new Error('切换到 JSON 前，请给每列一个不同的非空列名。')
  return body.map((row) => Object.fromEntries(header.map((name, i) => [name!, row[i]])))
}

function Table({ rows }: { rows: Cell[][] }) {
  const cell = (v: Cell) => v === null ? <span className="missing-value">空</span> : v === '' ? '""' : v
  return <table className="data-table">
    <thead><tr>{rows[0].map((v, i) => <th scope="col" key={i}>{cell(v)}</th>)}</tr></thead>
    <tbody>{rows.slice(1).map((row, i) => <tr key={i}>
      {row.map((v, j) => <td key={j}>{cell(v)}</td>)}
    </tr>)}</tbody>
  </table>
}

// 只按 JSON 的括号分段，跳过字符串中的括号，保留原文的缩进、引号和数字写法。
interface JsonContainer { start: string; end: string; parts: JsonPart[] }
type JsonPart = string | JsonContainer
function jsonParts(text: string) {
  const root: JsonPart[] = []
  const stack = [root]
  const tokens = text.match(/"(?:\\.|[^"\\])*"|[{}\[\],:]|[^"{}\[\],:]+/g) ?? []
  for (const token of tokens) {
    const parts = stack[stack.length - 1]
    if (token === '{' || token === '[') {
      const group = { start: token, end: token === '{' ? '}' : ']', parts: [] as JsonPart[] }
      parts.push(group)
      stack.push(group.parts)
    } else if (token === '}' || token === ']') stack.pop()
    else parts.push(token)
  }
  return root
}

function JsonGroup({ group }: { group: JsonContainer }) {
  const [open, setOpen] = useState(true)
  return <><button className="json-fold" aria-expanded={open} title={open ? '折叠' : '展开'}
    aria-label={open ? '折叠 JSON' : '展开 JSON'} onClick={() => setOpen(!open)}>{group.start}{open ? '' : '…'}</button>
    {open && renderParts(group.parts)}{group.end}</>
}

function renderParts(parts: JsonPart[]): ReactNode {
  return parts.map((p, i) => typeof p === 'string' ? p : <JsonGroup key={i} group={p} />)
}

function entries(container: JsonContainer): JsonPart[][] {
  const result: JsonPart[][] = [[]]
  for (const part of container.parts) {
    if (part === ',') result.push([])
    else if (typeof part !== 'string' || part.trim()) result[result.length - 1].push(part)
  }
  return result[0].length ? result : []
}

function original(part: JsonPart): string {
  return typeof part === 'string' ? part.trim() : part.start + part.parts.map(original).join('') + part.end
}

// 只解码文字。保留 7.0 的小数点、长编号的全部数字，以及嵌套 JSON 的值。
function csvCell(part: JsonPart): Cell {
  const raw = original(part)
  if (raw === 'null') return null
  return raw.startsWith('"') ? JSON.parse(raw) : raw
}

function jsonToCsv(text: string): string {
  const root = jsonParts(text.trim())[0]
  const items = typeof root === 'object' && root.start === '[' ? entries(root).map(([item]) => item) : [root]
  const records = items.map((item) => {
    if (typeof item === 'string' || item.start !== '{') return new Map([['值', csvCell(item)]])
    return new Map(entries(item).map(([key, , value]) => [JSON.parse(original(key)) as string, csvCell(value)]))
  })
  const keys = [...new Set(records.flatMap((r) => [...r.keys()]))]
  if (!keys.length) keys.push('值')
  const quote = (value: Cell) => {
    if (value === null) return ''
    return value === '' || /[",\n\r]/.test(value) ? '"' + value.replaceAll('"', '""') + '"' : value
  }
  return [keys, ...records.map((row) => keys.map((key) => row.get(key) ?? null))]
    .map((row) => row.map(quote).join(',') + '\n').join('')
}

function Values({ text }: { text: string }) {
  const array = jsonParts(text.trim())[0] as JsonContainer
  const values = entries(array)
  return <ul className="inspect-values">{values.map((v, i) => <li key={i}>{renderParts(v)}</li>)}</ul>
}

function LessonTable({ block }: { block: DataBlock }) {
  const [csv, setCsv] = useState(() => block.kind === 'json' ? jsonToCsv(block.content) : block.content)
  const [view, setView] = useState<View>(block.kind === 'json' ? 'JSON' : block.kind === 'csv' ? 'CSV' : '表格')
  let body
  if (view === 'CSV') {
    body = <textarea className="inspect-csv" aria-label="编辑 CSV" spellCheck={false} value={csv}
      rows={Math.min(14, Math.max(3, csv.trimEnd().split(/\r\n|[\r\n]/).length + 1))}
      onChange={(e) => setCsv(e.target.value)} />
  } else {
    try {
      const rows = parseCsv(csv)
      body = view === '表格' ? <Table rows={rows} /> : <pre>{JSON.stringify(toObjects(rows), null, 2)}</pre>
    } catch (err) {
      body = <p className="tone-fail" role="status">{(err as Error).message}</p>
    }
  }
  return <><div className="data-views" role="group" aria-label="数据视图">
    {(['表格', 'CSV', 'JSON'] as const).map((name) => <button key={name} aria-pressed={name === view}
      onClick={() => setView(name)}>{name}</button>)}
  </div>{body}</>
}

function BlockContent({ block, lesson }: { block: DataBlock; lesson: boolean }) {
  if (block.kind === 'schema') {
    return <table className="data-table"><thead><tr>
      {['列名', '类型', '可为空', '主键'].map((h) => <th scope="col" key={h}>{h}</th>)}
    </tr></thead><tbody>{block.columns?.map((c, i) => <tr key={i}>
      <td>{c.name}</td><td>{c.type}</td><td>{c.nullable ? '是' : '否'}</td><td>{c.primary_key ? '是' : '否'}</td>
    </tr>)}</tbody></table>
  }
  if (block.kind === 'values') return <Values text={block.content} />
  if (lesson) return <LessonTable block={block} />
  if (block.kind === 'json') return <pre>{renderParts(jsonParts(block.content))}</pre>
  if (block.kind === 'csv') return <ol className="numbered-csv">
    {block.content.replace(/(?:\r\n|[\r\n])$/, '').split(/\r\n|[\r\n]/).map((line, i) => <li key={i}>{line || '\u00a0'}</li>)}
  </ol>
  return <Table rows={parseCsv(block.content)} />
}

export const InspectData = memo(function InspectData({ block, lesson = false }: { block: DataBlock; lesson?: boolean }) {
  return <figure className="inspect-data">
    {block.title && <figcaption>{block.title}</figcaption>}
    <div className="data-scroll"><BlockContent block={block} lesson={lesson} /></div>
  </figure>
})
