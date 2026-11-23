import type { TablePreview } from './client'
import './table.css'

export default function SqlTableView({ table, label, row, column, markedRows }: {
  table: TablePreview; label: string; row?: number; column?: number; markedRows?: number[]
}) {
  return <div className="sql-scroll"><table className="sql-table">
    <caption>{label} · 共 {table.rowCount} 行{table.rowCount > 50 && '（显示前 50 行）'}</caption>
    <thead><tr>{table.columns.map((name, i) => <th key={i} scope="col">{name}</th>)}</tr></thead>
    <tbody>{table.rows.map((cells, i) => <tr key={i}>{cells.map((v, j) =>
      <td key={j} className={markedRows?.includes(i) || (i === row && column === j) ? 'sql-difference' : undefined}>
        {v === null ? <span className="faint">NULL</span> : typeof v === 'object' ? JSON.stringify(v) : String(v)}
      </td>)}</tr>)}</tbody>
  </table></div>
}
